"""Turn a small API-style order payload into shareable CSV and Markdown reports."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "orders.json"
OUTPUT_DIR = ROOT / "output"


def load_orders() -> list[dict]:
    with INPUT_FILE.open(encoding="utf-8") as file:
        orders = json.load(file)
    if not isinstance(orders, list):
        raise ValueError("orders.json must contain a JSON list")
    return orders


def write_paid_orders(orders: list[dict]) -> list[dict]:
    paid_orders = [order for order in orders if order["status"] == "paid"]
    with (OUTPUT_DIR / "paid_orders.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["order_id", "customer", "amount", "created_at"])
        writer.writeheader()
        writer.writerows({"order_id": order["order_id"], "customer": order["customer"], "amount": f'{order["amount"]:.2f}', "created_at": order["created_at"]} for order in paid_orders)
    return paid_orders


def write_summary(orders: list[dict], paid_orders: list[dict]) -> None:
    status_counts = Counter(order["status"] for order in orders)
    paid_total = sum(order["amount"] for order in paid_orders)
    lines = ["# 订单处理报告", "", f"- 原始订单数：{len(orders)}", f"- 已支付订单数：{len(paid_orders)}", f"- 已支付总金额：{paid_total:.2f}", "", "## 按状态统计", "", "| 状态 | 数量 |", "| --- | ---: |"]
    lines.extend(f"| {status} | {count} |" for status, count in sorted(status_counts.items()))
    lines.extend(["", "## 产物", "", "- `paid_orders.csv`：只保留已支付订单，适合交给表格或财务流程。", "- `summary.md`：适合贴进 issue、日报或部署记录。"])
    (OUTPUT_DIR / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    orders = load_orders()
    paid_orders = write_paid_orders(orders)
    write_summary(orders, paid_orders)
    print(f"Processed {len(orders)} orders; wrote reports to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
