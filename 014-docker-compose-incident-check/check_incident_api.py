"""Check the incident API and save a reviewable Markdown report."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ENDPOINTS = [("健康检查", "/health"), ("订单服务", "/api/orders")]


def request_endpoint(url: str) -> dict[str, str | int | float]:
    """Return useful details for successful and HTTP-error responses."""
    started_at = time.perf_counter()
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=3) as response:
            status = response.status
            body = response.read().decode("utf-8")
    except HTTPError as error:
        status = error.code
        body = error.read().decode("utf-8")
    except URLError as error:
        return {
            "status": "连接失败",
            "duration_ms": round((time.perf_counter() - started_at) * 1000, 1),
            "detail": str(error.reason),
        }

    payload = json.loads(body)
    return {
        "status": status,
        "duration_ms": round((time.perf_counter() - started_at) * 1000, 1),
        "detail": str(payload.get("status") or payload.get("error") or "无文字说明"),
    }


def build_report(results: list[dict[str, str | int | float]]) -> str:
    failures = [item for item in results if not isinstance(item["status"], int) or item["status"] >= 400]
    lines = ["# dev-workbench Docker API 检查报告", "", "## 结论", ""]
    lines.append(
        f"- 发现 {len(failures)} 个需要处理的接口；容器能运行不等于每项业务都正常。"
        if failures
        else "- 所有被检查接口都返回成功状态码。"
    )
    lines.extend(["", "## 检查结果", "", "| 名称 | URL | 状态码 | 耗时 | 说明 | 结论 |", "| --- | --- | --- | --- | --- | --- |"])
    for item in results:
        status = item["status"]
        conclusion = "正常" if isinstance(status, int) and status < 400 else "需要处理"
        lines.append(f"| {item['name']} | {item['url']} | {status} | {item['duration_ms']} ms | {item['detail']} | {conclusion} |")
    lines.extend(["", "## 下一步", "", "- 健康检查成功后，仍要按业务接口的状态码检查上游依赖或服务日志。"])
    return "\n".join(lines) + "\n"


def main() -> None:
    base_url = os.environ.get("API_BASE_URL", "http://127.0.0.1:8014").rstrip("/")
    results: list[dict[str, str | int | float]] = []
    for name, path in ENDPOINTS:
        url = base_url + path
        result = request_endpoint(url)
        result.update({"name": name, "url": url})
        results.append(result)

    output_path = Path(__file__).parent / "output" / "api_check_report.md"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(build_report(results), encoding="utf-8")
    print(f"已检查 {len(results)} 个接口，报告已写入：{output_path}")


if __name__ == "__main__":
    main()
