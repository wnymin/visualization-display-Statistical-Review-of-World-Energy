export function formatNumber(value, fractionDigits = 1) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return '暂无数据'
  }

  const absolute = Math.abs(value)
  if (absolute >= 1000) {
    return value.toLocaleString('zh-CN', {
      maximumFractionDigits: 0,
    })
  }

  return value.toLocaleString('zh-CN', {
    minimumFractionDigits: 0,
    maximumFractionDigits: fractionDigits,
  })
}

export function getLatestValue(series) {
  if (!series?.values?.length) {
    return null
  }

  for (let index = series.values.length - 1; index >= 0; index -= 1) {
    const value = series.values[index]
    if (value !== null && value !== undefined && !Number.isNaN(value)) {
      return value
    }
  }

  return null
}

export function getChangeSummary(series, yearsOffset = 10) {
  if (!series?.values?.length) {
    return '暂无变化数据'
  }

  const latestIndex = series.values.length - 1
  const compareIndex = latestIndex - yearsOffset

  if (compareIndex < 0) {
    return '暂无变化数据'
  }

  const latest = series.values[latestIndex]
  const compare = series.values[compareIndex]
  if (latest === null || compare === null || latest === undefined || compare === undefined) {
    return '暂无变化数据'
  }

  const diff = latest - compare
  const percent = compare === 0 ? null : (diff / compare) * 100
  const sign = diff >= 0 ? '+' : ''
  const percentText = percent === null ? '' : `，${sign}${formatNumber(percent, 1)}%`

  return `较${yearsOffset}年前${sign}${formatNumber(diff, 1)}${percentText}`
}

export function createLineOption({
  years,
  series,
  unit,
  subtitle,
  colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#8c564b'],
  area = false,
}) {
  return {
    color: colors,
    animationDuration: 700,
    grid: {
      left: 16,
      right: 20,
      top: 52,
      bottom: 48,
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'line',
      },
      valueFormatter: (value) => `${formatNumber(value, 1)} ${unit}`,
    },
    legend: {
      top: 8,
      textStyle: {
        color: 'inherit',
      },
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100,
      },
      {
        type: 'slider',
        height: 18,
        bottom: 8,
      },
    ],
    xAxis: {
      type: 'category',
      data: years,
      boundaryGap: false,
      axisLine: {
        lineStyle: {
          color: 'rgba(148, 163, 184, 0.5)',
        },
      },
      axisLabel: {
        color: '#64748b',
        hideOverlap: true,
      },
    },
    yAxis: {
      type: 'value',
      name: unit,
      nameLocation: 'end',
      nameTextStyle: {
        color: '#64748b',
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(148, 163, 184, 0.16)',
        },
      },
      axisLabel: {
        color: '#64748b',
        formatter: (value) => formatNumber(value, 0),
      },
    },
    series: series.map((item) => ({
      name: item.label,
      type: 'line',
      showSymbol: false,
      smooth: true,
      connectNulls: true,
      data: item.values,
      areaStyle: area
        ? {
            opacity: 0.08,
          }
        : undefined,
      lineStyle: {
        width: 3,
      },
      emphasis: {
        focus: 'series',
      },
    })),
  }
}

export function createBarOption({ items, unit, title }) {
  return {
    color: ['#f97316'],
    animationDuration: 700,
    grid: {
      left: 96,
      right: 18,
      top: 42,
      bottom: 20,
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      valueFormatter: (value) => `${formatNumber(value, 1)} ${unit}`,
    },
    xAxis: {
      type: 'value',
      name: unit,
      splitLine: {
        lineStyle: {
          color: 'rgba(148, 163, 184, 0.16)',
        },
      },
      axisLabel: {
        color: '#64748b',
        formatter: (value) => formatNumber(value, 0),
      },
    },
    yAxis: {
      type: 'category',
      inverse: true,
      data: items.map((item) => item.label),
      axisLabel: {
        color: '#475569',
        width: 88,
        overflow: 'truncate',
      },
    },
    series: [
      {
        name: title,
        type: 'bar',
        barWidth: 12,
        data: items.map((item) => item.value),
        itemStyle: {
          borderRadius: [0, 10, 10, 0],
        },
      },
    ],
  }
}
