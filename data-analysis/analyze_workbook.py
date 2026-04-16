from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK_PATH = ROOT / "EI-Stats-Review-ALL-data.xlsx"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def is_year(value: Any) -> bool:
    if value is None:
        return False
    try:
        year = int(float(value))
    except (ValueError, TypeError):
        return False
    return 1800 <= year <= 2100


def to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def normalized_label(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return "" if text.lower() == "nan" else text


def detect_year_header_row(df: pd.DataFrame) -> int | None:
    best_row = None
    best_score = -1.0
    for idx in range(len(df)):
        row = df.iloc[idx].tolist()
        year_values = [int(float(v)) for v in row if is_year(v) and int(float(v)) <= 2035]
        unique_years = sorted(set(year_values))
        year_count = len(unique_years)

        if year_count < 5:
            continue

        if unique_years[-1] - unique_years[0] > 250:
            continue

        diffs = [unique_years[i + 1] - unique_years[i] for i in range(len(unique_years) - 1)]
        consecutive_ratio = (
            sum(1 for d in diffs if d == 1) / len(diffs) if diffs else 0.0
        )

        # 年份行通常是连续年份序列，连续比例越高可信度越高。
        score = year_count + consecutive_ratio * 10
        if score > best_score:
            best_score = score
            best_row = idx

    if best_score < 5:
        return None
    return best_row


def analyze_sheet(sheet_name: str, workbook_path: Path) -> dict[str, Any]:
    df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=None, engine="openpyxl")
    row_count, col_count = df.shape

    header_row = detect_year_header_row(df)
    years: list[int] = []
    year_col_idx: list[int] = []

    if header_row is not None:
        for col_idx, value in enumerate(df.iloc[header_row].tolist()):
            if is_year(value):
                year = int(float(value))
                years.append(year)
                year_col_idx.append(col_idx)

    years = sorted(set(years))
    first_year = min(years) if years else None
    last_year = max(years) if years else None

    entity_rows: list[dict[str, Any]] = []
    top_latest: list[dict[str, Any]] = []

    if header_row is not None and year_col_idx:
        data_start = header_row + 1
        latest_col_idx = None

        if last_year is not None:
            for col_idx in year_col_idx:
                value = df.iloc[header_row, col_idx]
                if is_year(value) and int(float(value)) == last_year:
                    latest_col_idx = col_idx
                    break

        for ridx in range(data_start, row_count):
            label = normalized_label(df.iat[ridx, 0] if col_count > 0 else None)
            if not label:
                continue
            if "growth rate" in label.lower() or label.lower() == "share":
                continue

            numeric_points = 0
            for col_idx in year_col_idx:
                numeric = to_float(df.iat[ridx, col_idx])
                if numeric is not None:
                    numeric_points += 1

            if numeric_points == 0:
                continue

            latest_value = None
            if latest_col_idx is not None:
                latest_value = to_float(df.iat[ridx, latest_col_idx])

            entity_rows.append(
                {
                    "entity": label,
                    "numeric_points": numeric_points,
                    "latest_value": latest_value,
                }
            )

        if last_year is not None:
            sortable = [
                {"entity": e["entity"], "value": e["latest_value"]}
                for e in entity_rows
                if e["latest_value"] is not None
            ]
            sortable.sort(key=lambda x: x["value"], reverse=True)
            top_latest = sortable[:5]

    header_text = " ".join(normalized_label(v) for v in df.head(4).fillna("").values.flatten())

    return {
        "sheet_name": sheet_name,
        "rows": row_count,
        "cols": col_count,
        "header_row_index": header_row,
        "year_count": len(years),
        "first_year": first_year,
        "last_year": last_year,
        "entity_row_count": len(entity_rows),
        "sample_entities": [e["entity"] for e in entity_rows[:10]],
        "top_entities_latest_year": top_latest,
        "has_growth_info": "Growth rate per annum" in header_text,
        "has_share_info": "Share" in header_text,
    }


def summarize_categories(sheet_names: list[str]) -> dict[str, int]:
    category_count: dict[str, int] = {}
    for name in sheet_names:
        if " - " in name:
            category = name.split(" - ", 1)[0].strip()
        else:
            category = name.strip()
        category_count[category] = category_count.get(category, 0) + 1
    return dict(sorted(category_count.items(), key=lambda x: (-x[1], x[0])))


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    workbook = pd.ExcelFile(WORKBOOK_PATH, engine="openpyxl")
    sheet_names = workbook.sheet_names

    sheet_summaries = [analyze_sheet(name, WORKBOOK_PATH) for name in sheet_names]

    sheets_with_year = [s for s in sheet_summaries if s["first_year"] is not None]
    earliest_year = min((s["first_year"] for s in sheets_with_year), default=None)
    latest_year = max((s["last_year"] for s in sheets_with_year), default=None)

    workbook_summary = {
        "workbook": WORKBOOK_PATH.name,
        "sheet_count": len(sheet_names),
        "earliest_year": earliest_year,
        "latest_year": latest_year,
        "category_distribution": summarize_categories(sheet_names),
        "sheets_with_year_data": len(sheets_with_year),
        "sheets_without_year_data": len(sheet_names) - len(sheets_with_year),
    }

    (OUTPUT_DIR / "workbook_summary.json").write_text(
        json.dumps(workbook_summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    (OUTPUT_DIR / "sheet_summary.json").write_text(
        json.dumps(sheet_summaries, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    pd.DataFrame(sheet_summaries).to_csv(OUTPUT_DIR / "sheet_summary.csv", index=False)

    print("分析完成")
    print(f"输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
