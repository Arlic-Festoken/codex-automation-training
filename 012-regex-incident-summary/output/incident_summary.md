# dev-workbench 异常摘要

## 结论

- 找到 3 条 WARN / ERROR 记录。
- 状态码分布：429 × 1，500 × 1，503 × 1。

## 事件明细

| 时间 | 级别 | 请求 | 状态码 | 原因 |
| --- | --- | --- | --- | --- |
| 2026-08-21T09:01:03Z | WARN | GET /api/orders (31 ms) | 429 | rate_limited |
| 2026-08-21T09:02:45Z | ERROR | POST /api/orders (1423 ms) | 500 | database_timeout |
| 2026-08-21T09:04:18Z | ERROR | POST /api/orders (911 ms) | 503 | upstream_unavailable |

## 下一步

- 先检查 5xx 是否集中在同一个路径或原因，再决定是否升级为故障。
