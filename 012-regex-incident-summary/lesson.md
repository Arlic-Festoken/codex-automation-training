# 012：正则表达式——把应用日志变成异常摘要

预计用时：45～55 分钟。你会用一条可读的正则表达式，从日志中找出 `WARN` 和 `ERROR`，再生成一份能交给同事看的异常摘要。

## 先用大白话说清楚

日志是一行一行的纯文本，但每行其实都藏着相同结构：时间、级别、接口路径、状态码和原因。正则表达式（regex）就是给电脑的一张“文字筛选模板”：不必认识每一行的具体内容，只要求它符合某种形状。

例如 `\d{3}` 表示“连续三个数字”，正好适合 HTTP 状态码；`(?P<status>\d{3})` 不但匹配，还把结果起名为 `status`。这样脚本拿到的是有名字的字段，而不是一团难记的位置编号。

今天不要试图背完所有符号。只记住：`^` 表示从一行开头开始，`\s+` 表示一段空格，`\S+` 表示一段非空白文字，`(?P<名字>...)` 表示把匹配到的部分存起来。

## 本次小任务

1. 用 `rg` 先找出日志里的 `WARN` 和 `ERROR`。
2. 运行 Python 脚本，把异常记录转成 `output/incident_summary.md`。
3. 在生成报告中确认有 3 条异常，状态码为 `429`、`500`、`503`。
4. 在样例日志最后添加一条自己的 `ERROR` 行（复制一行再改 `path`、`status` 和 `reason` 即可）。
5. 重新生成报告，确认你的新异常出现；只审阅并提交本节文件。

完成标准：报告中的异常条数与 `rg` 找到的条数一致，表格中能看出哪条接口、什么状态码、什么原因出了问题。

## 跟着做

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习\012-regex-incident-summary"
rg -n "WARN|ERROR" .\sample_logs\app.log
python .\build_incident_summary.py
Get-Content -Encoding UTF8 .\output\incident_summary.md
```

只想查 5xx 服务端错误时，用这个更窄的模式：

```powershell
rg -n "status=5\d{2}" .\sample_logs\app.log
```

打开 `sample_logs/app.log`，在最后添加一条与现有格式一致的记录，例如：

```text
2026-08-21T09:06:40Z ERROR request_id=m3n4 method=GET path=/api/profile status=500 duration_ms=1201 reason=cache_failure
```

再运行脚本并验证：

```powershell
python .\build_incident_summary.py
Select-String -Path .\output\incident_summary.md -Pattern "/api/profile|找到 4 条"
```

最后回到训练仓库根目录，审阅自己的改动。`git add` 只列出本节目录，避免把别的练习一起带进提交：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习"
git status --short
git diff -- 012-regex-incident-summary
git add -- 012-regex-incident-summary
git diff --cached -- 012-regex-incident-summary
git commit -m "Add regex incident summary practice"
git status
```

## 命令小抄

| 命令或写法 | 它在做什么 |
| --- | --- |
| `rg -n "WARN|ERROR" 文件` | 找出包含任意一个关键词的行，并显示行号。 |
| `\d{3}` | 匹配恰好三位数字，例如 `200` 或 `503`。 |
| `(?P<status>...)` | 给捕获到的文本命名，Python 可用 `groupdict()` 直接取字段。 |
| `(?:...)?` | 这段内容可有可无；日志里没有 `reason` 时脚本也不会崩。 |
| `re.compile(...)` | 先把模板编译好，再重复用于多行文本。 |

## 真实开发里有什么用

线上问题通常先从日志开始：你会筛出失败状态码，确认是否集中在某条 API、哪个时间段或某个原因，再决定是查数据库、第三方服务还是限流配置。把正则提取和 Markdown 报告做成脚本，能让“翻几千行日志”变成几秒钟可重复的诊断动作。

这正是 `dev-workbench` 缺的一块：第 011 课汇总项目状态，本课提供异常信号。下一节 HTTP / API 会让你用接口健康检查去验证日志中看到的问题。

## 自测

`\S+` 与 `\s+` 分别会匹配什么？为什么本课的状态码用 `\d{3}`，而不直接写 `\d+`？

完成后，请在本目录创建 `feedback.txt`，写下最难理解的一个符号、你实际遇到的报错，或希望下节 HTTP / API 练习检查什么接口。下次练习会优先据此调整。
