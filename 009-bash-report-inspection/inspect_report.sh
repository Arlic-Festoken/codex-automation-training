#!/usr/bin/env bash
set -euo pipefail

# 在 Windows 上请用 Git Bash 或 WSL 运行本脚本。
REPORT_DIR="${1:-../008-data-processing-order-report/output}"

if [[ ! -d "$REPORT_DIR" ]]; then
  echo "找不到报告目录: $REPORT_DIR" >&2
  echo "请先运行 008-data-processing-order-report/build_report.py，或把目录作为第一个参数传入。" >&2
  exit 1
fi

echo "== 报告目录 =="
printf '路径: %s\n\n' "$REPORT_DIR"

echo "== 文件清单（大小、修改时间） =="
find "$REPORT_DIR" -maxdepth 1 -type f -printf '%TY-%Tm-%Td %TH:%TM  %10s bytes  %f\n' | sort

echo
echo "== 汇总信息 =="
SUMMARY_FILE="$REPORT_DIR/summary.md"
if [[ -f "$SUMMARY_FILE" ]]; then
  grep -E '原始订单数|已支付订单数|已支付总金额' "$SUMMARY_FILE" || true
else
  echo "未找到 summary.md"
fi

echo
echo "== CSV 数据行数 =="
CSV_FILE="$REPORT_DIR/paid_orders.csv"
if [[ -f "$CSV_FILE" ]]; then
  data_rows=$(tail -n +2 "$CSV_FILE" | wc -l | tr -d ' ')
  printf 'paid_orders.csv: %s 条已支付订单\n' "$data_rows"
else
  echo "未找到 paid_orders.csv"
fi
