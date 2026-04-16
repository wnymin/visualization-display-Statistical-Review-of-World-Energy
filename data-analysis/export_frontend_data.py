from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK_PATH = ROOT / "EI-Stats-Review-ALL-data.xlsx"
OUTPUT_PATH = ROOT / "webapp-vue" / "src" / "data" / "dashboardData.json"

TARGETS = {
    "overview": {
        "TES": {"sheet": "Total Energy Supply (TES) -EJ", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
        "CO2": {"sheet": "CO2 from Energy", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
        "Electricity": {"sheet": "Electricity Generation - TWh", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
    },
    "fossil": {
        "Oil": {"sheet": "Oil Consumption - EJ", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
        "Gas": {"sheet": "Gas Consumption - EJ", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
        "Coal": {"sheet": "Coal Consumption - EJ", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
    },
    "transition": {
        "Renewables": {"sheet": "Renewables Consumption -EJ", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
        "Solar": {"sheet": "Solar Generation - TWh", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
        "Wind": {"sheet": "Wind Generation - TWh", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
        "BESS": {"sheet": "Grid Scale BESS Capacity", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
        "CCUS": {"sheet": "CCUS Capture Capacity", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
    },
    "emissions": {
        "CO2": {"sheet": "CO2 from Energy", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
        "CO2e": {"sheet": "CO2e Emissions ", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Asia Pacific"]},
        "Flaring": {"sheet": "CO2 from Flaring", "labels": ["Total World", "Non-OECD", "of which: OECD", "Total Middle East"]},
    },
}

SUMMARY_SHEETS = [
    "Total Energy Supply (TES) -EJ",
    "CO2 from Energy",
    "Electricity Generation - TWh",
    "Oil Consumption - EJ",
    "Gas Consumption - EJ",
    "Coal Consumption - EJ",
    "Renewables Consumption -EJ",
    "Solar Generation - TWh",
    "Wind Generation - TWh",
    "Grid Scale BESS Capacity",
    "CCUS Capture Capacity",
    "CO2e Emissions ",
    "CO2 from Flaring",
    "Natural Gas Flaring",
]


def is_year(value: Any) -> bool:
    try:
        year = int(float(value))
    except (TypeError, ValueError):
        return False
    return 1800 <= year <= 2100


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return "" if text.lower() == "nan" else text


def detect_header_row(df: pd.DataFrame) -> int:
    best_row = 2
    best_score = -1
    for idx in range(min(len(df), 8)):
        row = df.iloc[idx].tolist()
        years = [int(float(v)) for v in row if is_year(v) and int(float(v)) <= 2035]
        if len(years) < 5:
            continue
        score = len(set(years))
        if score > best_score:
            best_score = score
            best_row = idx
    return best_row


def extract_series(sheet_name: str, label: str) -> dict[str, Any]:
    df = pd.read_excel(WORKBOOK_PATH, sheet_name=sheet_name, header=None, engine="openpyxl")
    header_row = detect_header_row(df)
    header = df.iloc[header_row].tolist()
    years = []
    cols = []
    for idx, value in enumerate(header):
        if is_year(value) and int(float(value)) <= 2035:
            year = int(float(value))
            years.append(year)
            cols.append(idx)
    years = sorted(dict.fromkeys(years))

    label_col = 0
    rows = df.iloc[header_row + 1 :].reset_index(drop=True)
    target_row = None
    for _, row in rows.iterrows():
        current = clean_text(row.iloc[label_col])
        if current == label:
            target_row = row
            break

    if target_row is None:
        return {"label": label, "years": years, "values": [], "unit": clean_text(df.iat[header_row - 1, 0]) if header_row > 0 else ""}

    values = []
    for col in cols:
        val = target_row.iloc[col]
        try:
            values.append(None if pd.isna(val) else float(val))
        except Exception:
            values.append(None)

    unit = clean_text(df.iat[header_row, 0]) if header_row < len(df) else ""
    return {"label": label, "years": years, "values": values, "unit": unit}


def extract_latest_rank(sheet_name: str, limit: int = 8) -> dict[str, Any]:
    df = pd.read_excel(WORKBOOK_PATH, sheet_name=sheet_name, header=None, engine="openpyxl")
    header_row = detect_header_row(df)
    header = df.iloc[header_row].tolist()
    year_cols = []
    years = []
    for idx, value in enumerate(header):
        if is_year(value) and int(float(value)) <= 2035:
            year = int(float(value))
            year_cols.append(idx)
            years.append(year)
    latest_year = max(years)
    latest_col = year_cols[years.index(latest_year)]
    items = []
    for _, row in df.iloc[header_row + 1 :].iterrows():
        label = clean_text(row.iloc[0])
        if not label or label.lower() == "nan":
            continue
        if "growth rate" in label.lower() or label.lower() == "share":
            continue
        try:
            value = row.iloc[latest_col]
            if pd.isna(value):
                continue
            value = float(value)
        except Exception:
            continue
        items.append({"label": label, "value": value})
    items.sort(key=lambda x: x["value"], reverse=True)
    return {"sheet": sheet_name, "year": latest_year, "items": items[:limit]}


def build_section(config: dict[str, dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, item in config.items():
        result[key] = {
            "series": [extract_series(item["sheet"], label) for label in item["labels"]],
            "rank": extract_latest_rank(item["sheet"], 8),
        }
    return result


def main() -> None:
    data = {
        "meta": {
            "title": "世界能源统计可视化",
            "subtitle": "基于 Statistical Review of World Energy 的数据分析面板",
            "source": "Energy Institute",
            "workbook": WORKBOOK_PATH.name,
            "overview": "基于 2024 最新数据与 1965-2024 长序列构建首版仪表盘",
        },
        "sections": {
            "overview": build_section(TARGETS["overview"]),
            "fossil": build_section(TARGETS["fossil"]),
            "transition": build_section(TARGETS["transition"]),
            "emissions": build_section(TARGETS["emissions"]),
        },
        "kpis": {
            "TES": extract_series("Total Energy Supply (TES) -EJ", "Total World"),
            "CO2": extract_series("CO2 from Energy", "Total World"),
            "Electricity": extract_series("Electricity Generation - TWh", "Total World"),
            "Oil": extract_series("Oil Consumption - EJ", "Total World"),
            "Gas": extract_series("Gas Consumption - EJ", "Total World"),
            "Coal": extract_series("Coal Consumption - EJ", "Total World"),
            "Renewables": extract_series("Renewables Consumption -EJ", "Total World"),
            "Solar": extract_series("Solar Generation - TWh", "Total World"),
            "Wind": extract_series("Wind Generation - TWh", "Total World"),
        },
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已生成 {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
