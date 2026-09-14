"""Turn API-check JSON into reviewable CSV and Markdown artifacts."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "check_results.json"
OUTPUT_DIR = ROOT / "output"
CSV_PATH = OUTPUT_DIR / "api_check_dashboard.csv"
MARKDOWN_PATH = OUTPUT_DIR / "api_check_dashboard.md"


def classify(status_code: int) -> str:
    """Return a human-actionable result instead of a bare status code."""
    if 200 <= status_code < 400:
        return "正常"
    if 400 <= status_code < 500:
        return "请求需要检查"
    return "需要处理"


def load_results() -> list[dict[str, object]]:
    raw_results = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    required_fields = {
        "environment",
        "checked_at",
        "name",
        "url",
        "status_code",
        "duration_ms",
        "message",
    }
    if not isinstance(raw_results, list):
        raise ValueError("check_results.json 的最外层必须是数组。")

    for index, result in enumerate(raw_results, start=1):
        if not isinstance(result, dict) or required_fields - result.keys():
            raise ValueError(f"第 {index} 条检查结果缺少必要字段。")
        if not isinstance(result["status_code"], int):
            raise ValueError(f"第 {index} 条 status_code 必须是整数。")
        if not isinstance(result["duration_ms"], (int, float)):
            raise ValueError(f"第 {index} 条 duration_ms 必须是数字。")
    return raw_results


def write_csv(rows: list[dict[str, object]]) -> None:
    fieldnames = [
        "environment",
        "checked_at",
        "name",
        "status_code",
        "duration_ms",
        "result",
        "message",
        "url",
    ]
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]]) -> None:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["environment"])].append(row)

    lines = ["# API 检查对比报告", "", "## 结论", ""]
    for environment, environment_rows in grouped.items():
        problem_count = sum(row["result"] != "正常" for row in environment_rows)
        average_ms = sum(float(row["duration_ms"]) for row in environment_rows) / len(environment_rows)
        conclusion = "需要跟进" if problem_count else "正常"
        lines.append(
            f"- **{environment}**：{conclusion}；{len(environment_rows)} 项检查，"
            f"{problem_count} 项非正常，平均耗时 {average_ms:.1f} ms。"
        )

    lines.extend([
        "",
        "## 明细",
        "",
        "| 环境 | 检查项 | 状态码 | 耗时 | 结论 | 说明 |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['environment']} | {row['name']} | {row['status_code']} | "
            f"{float(row['duration_ms']):.1f} ms | {row['result']} | {row['message']} |"
        )

    lines.extend([
        "",
        "## 下一步",
        "",
        "- 先处理所有“需要处理”的业务接口；健康检查正常不代表业务链路正常。",
        "- 复查耗时明显高于同类环境的接口，并结合服务日志定位原因。",
        "",
    ])
    MARKDOWN_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    INPUT_PATH.exists() or (_ for _ in ()).throw(FileNotFoundError(INPUT_PATH))
    OUTPUT_DIR.mkdir(exist_ok=True)
    rows = []
    for result in load_results():
        row = dict(result)
        row["result"] = classify(int(row["status_code"]))
        rows.append(row)
    write_csv(rows)
    write_markdown(rows)
    print(f"已生成 {CSV_PATH.relative_to(ROOT)} 和 {MARKDOWN_PATH.relative_to(ROOT)}（{len(rows)} 条检查结果）。")


if __name__ == "__main__":
    main()
