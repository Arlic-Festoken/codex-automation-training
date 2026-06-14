# 005 HTTP / API：用 curl 看懂一次接口请求

建议用时：45-60 分钟

## 1. 大白话解释概念

HTTP 可以理解成“客户端和服务器说话的规矩”。

你在浏览器里打开网页、前端调用后端接口、脚本请求 GitHub API，本质上都是一次 HTTP 请求：

- 客户端说：我要访问哪个地址，用什么方法，要不要带数据。
- 服务器回：我处理得怎么样，状态码是多少，返回什么内容。

最常见的几个词：

- URL：接口地址，例如 `http://127.0.0.1:8000/health`
- Method：请求方法，例如 `GET` 是读取，`POST` 是提交
- Status Code：状态码，例如 `200` 成功，`404` 找不到，`500` 服务端出错
- Header：请求或响应的元信息，例如内容类型、认证方式
- Body：真正的数据内容，很多 API 会返回 JSON

真实开发里，不要只看“页面报错了”。你要能问清楚：请求有没有发出去？状态码是多少？返回体里说了什么？这就是 HTTP / API 基本功。

## 2. 小任务

本课用本目录的 `mock_api.py` 启动一个本地接口服务，然后用 `curl` 检查 4 个接口，最后整理成 `api-check-report.md`。

要检查的接口：

| 接口 | 预期含义 |
|---|---|
| `/health` | 服务健康检查 |
| `/api/orders` | 正常业务数据 |
| `/api/orders/slow` | 服务可用但耗时偏高 |
| `/api/missing` | 不存在的接口 |

报告至少包含：

1. 每个接口的 URL、状态码、是否符合预期。
2. `/health` 返回的 JSON 里 `status` 是什么。
3. 哪个接口最需要开发者关注，以及原因。
4. 你对 `200`、`404`、`503` 的一句话理解。

## 3. 命令示例

### 第一步：启动本地 API

打开一个 PowerShell 窗口：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习\005-http-api-health-check"
python .\mock_api.py
```

看到类似下面的输出后，不要关闭这个窗口：

```text
Mock API running at http://127.0.0.1:8000
```

### 第二步：另开一个窗口发请求

先看健康检查返回了什么：

```powershell
curl.exe http://127.0.0.1:8000/health
```

只看状态码，不看正文：

```powershell
curl.exe -s -o NUL -w "%{http_code}`n" http://127.0.0.1:8000/health
curl.exe -s -o NUL -w "%{http_code}`n" http://127.0.0.1:8000/api/missing
```

把响应头也打印出来：

```powershell
curl.exe -i http://127.0.0.1:8000/api/orders
```

把 JSON 保存到文件：

```powershell
curl.exe -s http://127.0.0.1:8000/api/orders -o orders.json
Get-Content .\orders.json
```

### 第三步：用 Python 辅助检查

如果你想少手抄，可以创建 `check_api.py`，从这个骨架开始：

```python
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

endpoints = [
    "http://127.0.0.1:8000/health",
    "http://127.0.0.1:8000/api/orders",
    "http://127.0.0.1:8000/api/orders/slow",
    "http://127.0.0.1:8000/api/missing",
]

for url in endpoints:
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=5) as response:
            body = response.read().decode("utf-8")
            print(response.status, url, body)
    except HTTPError as error:
        body = error.read().decode("utf-8")
        print(error.code, url, body)
```

运行：

```powershell
python .\check_api.py
```

这段代码用的是 Python 标准库，不需要安装第三方包。

## 4. 这个技能在真实开发中有什么用

HTTP / API 基本功会直接用在这些场景里：

- 前后端联调时判断问题在前端、后端还是网络。
- 排查线上接口报错，快速确认状态码和返回体。
- 写健康检查脚本，部署后自动确认服务是否真的可用。
- 调第三方 API 时确认认证、参数、JSON 结构是否正确。
- 给最终项目 `dev-workbench` 增加“API 检查并生成报告”的能力。

这节课和前两节可以串起来：HTTP 请求产生状态码，正则和 Python 可以把这些请求结果整理成报告，Git 再记录你的改动。

## 5. 进阶挑战

基础任务做完后任选一个：

- 在 `api-check-report.md` 里增加一列“响应时间”。
- 把 `check_api.py` 改成自动生成 Markdown 表格。
- 给 `/api/orders/slow` 设置一个规则：超过 500ms 就标记为需要关注。
- 故意把服务关掉，再观察 `curl` 和 Python 分别报什么错。

## 6. 自测问题

如果你请求一个接口，返回：

```text
HTTP/1.0 404 Not Found
Content-Type: application/json

{"error": "not found"}
```

你会怎么判断“服务器挂了”还是“请求地址写错了”？

请把答案和练习感受写到本目录的 `feedback.txt`。至少记录：

- 哪个命令最有用？
- 状态码是否比你想象中更容易理解？
- 下一课 Docker 基础想先练“运行别人做好的镜像”，还是“给自己的脚本写 Dockerfile”？
