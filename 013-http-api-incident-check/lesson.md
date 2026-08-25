# 013：HTTP / API——用健康检查确认日志里的异常

预计用时：45～55 分钟。你会启动一个本地服务，用 `curl` 和 Python 检查接口，再生成一份能说明“哪里正常、哪里需要处理”的报告。

## 先用大白话说清楚

上一课的日志说订单接口出现过 `500` 和 `503`。但日志只是在告诉你“曾经出过事”，不能证明它此刻是否恢复。HTTP 健康检查就是你主动敲服务的门：请求发出去，服务用状态码和 JSON 回答。

`200` 表示这次请求成功；`404` 多半是地址写错或功能不存在；`5xx` 表示服务端处理失败，常见原因是数据库、上游服务或配置出了问题。一个 `/health` 返回 `200` 只能说明服务还活着，**不代表每个业务接口都正常**。

今天只记住一条排查顺序：先看状态码，再看返回 JSON，最后看耗时和日志。不要只凭“网页能打开”下结论。

## 本次小任务

1. 启动本目录的本地演示 API。
2. 用 `curl` 分别检查 `/health` 与 `/api/orders`。
3. 运行 `check_incident_api.py`，生成 `output/api_check_report.md`。
4. 确认健康检查为 `200`，订单服务为 `503`，报告把订单服务标为“需要处理”。
5. 把 `mock_incident_api.py` 中订单服务的状态改为 `200`，重新运行检查，观察报告如何变化；练习后可改回 `503`。

完成标准：你能解释为什么 `/health` 成功而订单接口仍需处理，并能在报告里指出问题接口、状态码和服务给出的说明。

## 跟着做

第一个 PowerShell 窗口启动服务并保持打开：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习\013-http-api-incident-check"
python .\mock_incident_api.py
```

第二个 PowerShell 窗口检查接口。`-i` 会显示状态行、响应头和正文：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习\013-http-api-incident-check"
curl.exe -i http://127.0.0.1:8013/health
curl.exe -i http://127.0.0.1:8013/api/orders
curl.exe -s -o NUL -w "%{http_code}`n" http://127.0.0.1:8013/api/orders
python .\check_incident_api.py
Get-Content -Encoding UTF8 .\output\api_check_report.md
```

最后在训练仓库根目录只审阅本节文件：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习"
git status --short
git diff -- 013-http-api-incident-check
git add -- 013-http-api-incident-check README.md 总路线.md
git diff --cached
git commit -m "Add HTTP incident check practice"
git push origin main
```

## 命令小抄

| 命令或写法 | 它在做什么 |
| --- | --- |
| `curl.exe -i URL` | 显示 HTTP 状态行、响应头和正文。 |
| `curl.exe -s -o NUL -w "%{http_code}" URL` | 只打印状态码，适合脚本做快速判断。 |
| `urlopen(..., timeout=3)` | Python 标准库发请求，最多等待 3 秒。 |
| `HTTPError` | 服务器确实回了 4xx/5xx；依然可以读取响应体。 |
| `URLError` | 连不上服务、域名不存在等网络层问题。 |

## 真实开发里有什么用

这就是部署后的第一轮排查：健康检查先判断进程是否活着，关键业务接口再判断用户真正能不能用。脚本把状态码、耗时和返回体变成 Markdown 报告，能作为发布记录、故障复盘的起点，也让 `dev-workbench` 从“日志发现异常”走到“主动验证异常”。

下节会进入 Docker：把这套 API 检查放进可复制的运行环境，让别人的电脑也能按同样方式复现。

## 自测

`/health` 返回 `200`，而 `/api/orders` 返回 `503`，你会对同事说“服务正常”吗？请用状态码、接口职责和下一步排查动作回答。

完成后，请在本目录创建 `feedback.txt`，写下一个最容易混淆的点或实际报错。下次练习会先读取它；如果你仍不熟悉状态码或 `curl`，会先针对性复练，而不是直接进入 Docker。
