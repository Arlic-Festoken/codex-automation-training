"""Build a small, repeatable status summary for the dev-workbench exercises."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = ROOT / "008-data-processing-order-report" / "output" / "summary.md"
REVIEW_PATH = ROOT / "010-git-report-change-review" / "my_report_review.md"


def read_first_line(path: Path, default: str) -> str:
    """Return the first meaningful line in a file, or a clear fallback."""
    if not path.exists():
        return default
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line.lstrip("- ").strip()
    return default


def git_value(*args: str) -> str:
    """Ask Git for one value without failing when Git cannot answer."""
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", check=False,
    )
    value = result.stdout.strip()
    return value if result.returncode == 0 and value else "无法读取"


def git_status() -> str:
    """Return a readable working-tree status, including a clean tree."""
    result = subprocess.run(
        ["git", "status", "--short"], cwd=ROOT, capture_output=True,
        text=True, encoding="utf-8", check=False,
    )
    if result.returncode != 0:
        return "无法读取"
    own_outputs = {
        "011-python-project-status-summary/output/project_status.md",
        "011-python-project-status-summary/output/project_status_draft.md",
    }
    changes = [
        line for line in result.stdout.splitlines()
        if line[3:].strip().strip('"') not in own_outputs
    ]
    return "\n".join(changes) or "无"


def build_summary() -> str:
    report_overview = read_first_line(REPORT_PATH, "订单报告尚未生成")
    review_overview = read_first_line(REVIEW_PATH, "尚未添加个人报告复盘")
    changed_files = git_status()
    lines = [
        "# dev-workbench 项目状态摘要", "", "## 报告模块", "",
        f"- {report_overview}", "", "## Git 状态", "",
        f"- 当前分支：{git_value('branch', '--show-current')}",
        f"- 生成时最近提交：{git_value('log', '-1', '--oneline')}",
        f"- 未提交改动：{changed_files}",
        "", "## 学习复盘", "", f"- {review_overview}", "", "## 下一步", "",
        "- 为这个脚本添加一条你自己的状态检查，再重新生成本文件。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="生成 dev-workbench 项目状态摘要")
    parser.add_argument("--output", type=Path, default=Path("output/project_status.md"))
    args = parser.parse_args()
    output_path = args.output if args.output.is_absolute() else Path(__file__).parent / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_summary(), encoding="utf-8")
    print(f"已生成 {output_path}")


if __name__ == "__main__":
    main()
