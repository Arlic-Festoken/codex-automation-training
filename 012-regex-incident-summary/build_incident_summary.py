"""Extract warning and error signals from a simple application log."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

LINE_PATTERN = re.compile(
    r"^(?P<time>\S+)\s+(?P<level>WARN|ERROR)\s+"
    r"request_id=(?P<request_id>\S+)\s+method=(?P<method>\S+)\s+"
    r"path=(?P<path>\S+)\s+status=(?P<status>\d{3})\s+"
    r"duration_ms=(?P<duration_ms>\d+)(?:\s+reason=(?P<reason>\S+))?$"
)


def extract_incidents(log_path: Path) -> list[dict[str, str]]:
    """Return structured WARN/ERROR records and skip unrelated lines safely."""
    incidents: list[dict[str, str]] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        match = LINE_PATTERN.match(line)
        if match:
            incidents.append(match.groupdict(default="未提供"))
    return incidents


def build_report(incidents: list[dict[str, str]]) -> str:
    """Build a Markdown incident report from extracted log fields."""
    status_counts = Counter(item["status"] for item in incidents)
    lines = ["# dev-workbench 异常摘要", ""]
    lines.extend(["## 结论", "", f"- 找到 {len(incidents)} 条 WARN / ERROR 记录。"])
    if incidents:
        lines.append("- 状态码分布：" + "，".join(
            f"{status} × {count}" for status, count in sorted(status_counts.items())
        ) + "。")
    lines.extend(["", "## 事件明细", "", "| 时间 | 级别 | 请求 | 状态码 | 原因 |", "| --- | --- | --- | --- | --- |"])
    for item in incidents:
        request = f"{item['method']} {item['path']} ({item['duration_ms']} ms)"
        lines.append(
            f"| {item['time']} | {item['level']} | {request} | "
            f"{item['status']} | {item['reason']} |"
        )
    lines.extend(["", "## 下一步", "", "- 先检查 5xx 是否集中在同一个路径或原因，再决定是否升级为故障。"])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="从日志生成异常摘要")
    parser.add_argument("--log", type=Path, default=Path("sample_logs/app.log"))
    parser.add_argument("--output", type=Path, default=Path("output/incident_summary.md"))
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    log_path = args.log if args.log.is_absolute() else base_dir / args.log
    output_path = args.output if args.output.is_absolute() else base_dir / args.output
    incidents = extract_incidents(log_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_report(incidents), encoding="utf-8")
    print(f"已从 {log_path.name} 提取 {len(incidents)} 条异常记录：{output_path}")


if __name__ == "__main__":
    main()
