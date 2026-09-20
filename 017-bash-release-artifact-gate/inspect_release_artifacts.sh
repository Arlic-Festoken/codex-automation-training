#!/usr/bin/env bash
# Inspect the data artifacts made in lesson 016 before sharing a release report.
# Usage: bash inspect_release_artifacts.sh [report_directory] [--strict]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_DIR="${1:-$SCRIPT_DIR/../016-data-processing-api-check-dashboard}"
STRICT_MODE=false

if [[ "${2:-}" == "--strict" ]] || [[ "${1:-}" == "--strict" ]]; then
  STRICT_MODE=true
  [[ "${1:-}" == "--strict" ]] && REPORT_DIR="$SCRIPT_DIR/../016-data-processing-api-check-dashboard"
fi

JSON_FILE="$REPORT_DIR/check_results.json"
CSV_FILE="$REPORT_DIR/output/api_check_dashboard.csv"
MARKDOWN_FILE="$REPORT_DIR/output/api_check_dashboard.md"

fail() {
  echo "失败：$1" >&2
  exit 1
}

require_file() {
  [[ -f "$1" ]] || fail "找不到 $1。请先进入正确目录并运行第 016 课的 Python 脚本。"
}

require_file "$JSON_FILE"
require_file "$CSV_FILE"
require_file "$MARKDOWN_FILE"

echo "检查目录：$REPORT_DIR"
echo
echo "1/4 JSON 是否是有效数据？"
python -m json.tool "$JSON_FILE" >/dev/null || fail "JSON 格式不合法。"
json_count=$(python -c "import json, sys; print(len(json.load(open(sys.argv[1], encoding='utf-8'))))" "$JSON_FILE")
[[ "$json_count" -gt 0 ]] || fail "JSON 中没有检查记录。"
echo "通过：JSON 有 $json_count 条记录。"

echo
echo "2/4 CSV 列与数据行是否齐全？"
expected_header='environment,checked_at,name,status_code,duration_ms,result,message,url'
actual_header=$(head -n 1 "$CSV_FILE" | sed 's/^\xEF\xBB\xBF//')
[[ "$actual_header" == "$expected_header" ]] || fail "CSV 表头不符合预期：$actual_header"
csv_count=$(tail -n +2 "$CSV_FILE" | grep -c . || true)
[[ "$csv_count" -eq "$json_count" ]] || fail "CSV 有 $csv_count 行，JSON 有 $json_count 条；请重新生成报告。"
echo "通过：CSV 表头正确，数据行与 JSON 一致。"

echo
echo "3/4 Markdown 是否包含结论与明细？"
grep -q '^## 结论$' "$MARKDOWN_FILE" || fail "Markdown 缺少“结论”章节。"
grep -q '^## 明细$' "$MARKDOWN_FILE" || fail "Markdown 缺少“明细”章节。"
grep -q '^## 下一步$' "$MARKDOWN_FILE" || fail "Markdown 缺少“下一步”章节。"
echo "通过：Markdown 的交付章节齐全。"

echo
echo "4/4 是否存在需要处理的接口？"
problem_rows=$(tail -n +2 "$CSV_FILE" | awk -F, '$6 != "正常" {count++} END {print count+0}')
if [[ "$problem_rows" -gt 0 ]]; then
  echo "提示：发现 $problem_rows 条非正常检查；这不是格式错误，但不能把报告写成“全部正常”。"
  tail -n +2 "$CSV_FILE" | awk -F, '$6 != "正常" {print "- " $1 "/" $3 ": HTTP " $4 "（" $6 "）"}'
  if [[ "$STRICT_MODE" == true ]]; then
    echo "严格模式：因存在非正常接口而拒绝通过。" >&2
    exit 2
  fi
else
  echo "通过：没有非正常检查。"
fi

echo
echo "结构巡检完成：JSON、CSV、Markdown 相互一致。"
