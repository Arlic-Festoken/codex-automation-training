# 016：数据处理——把 API 检查结果变成可比较的交付报告

预计用时：45～55 分钟。你会把机器能读的 JSON 检查结果，整理成同事能快速复核的 CSV 和 Markdown 报告。这一步把第 013、014 课的“发现接口问题”升级为“比较环境、交付证据并安排下一步”。

## 先用大白话说清楚

API 检查脚本跑完时，经常只留下一堆零散的状态码、耗时和错误文本。JSON 像一叠字段固定的检查单，适合程序读取；CSV 像可筛选的表格，适合 Excel、表格软件和后续分析；Markdown 则像一页结论清楚的交付说明，适合发到项目、PR 或故障记录里。

“数据处理”不是把格式硬改一遍，而是给每条原始结果补上可行动的含义。例如 `503` 不只是一串数字，而是“需要处理”；同样的 `orders` 接口在本地异常、预发正常，这就是值得排查的环境差异。脚本应保留原始字段，同时生成结论，避免人工复制时漏行或写错。

本课使用的 `staging.example.test` 只是教学地址，不会发出任何网络请求；脚本只读取本地 JSON。

## 本次小任务

1. 读懂 `check_results.json` 的一条检查记录：环境、检查时间、接口名、状态码、耗时与说明。
2. 运行 `build_check_dashboard.py`，生成可筛选的 CSV 与可交付的 Markdown 报告。
3. 给 JSON 再添加一条你设计的检查结果，重新生成报告，并确认它出现在两份产物中。
4. 用 Git 查看这次“输入数据变更”如何影响“生成产物”。

完成标准：你能用报告说清哪个环境有问题、哪个接口需要处理，并解释 CSV 与 Markdown 为什么要同时保留。

## 跟着做

先进入本课目录：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习\016-data-processing-api-check-dashboard"
Get-Content .\check_results.json
```

### 1. 运行数据处理脚本

```powershell
python .\build_check_dashboard.py
Get-Content .\output\api_check_dashboard.md
Import-Csv .\output\api_check_dashboard.csv | Format-Table environment, name, status_code, duration_ms, result
```

现在你应看到：`local-compose` 的 `orders` 是 `503 / 需要处理`，而 `staging` 的两项检查正常。不要只因 `/health` 是 200 就宣布系统正常——业务接口可能仍然失败。

### 2. 看懂脚本中最关键的三件事

```powershell
Select-String -Path .\build_check_dashboard.py -Pattern 'json.loads|classify|DictWriter|write_markdown'
```

- `json.loads(...)`：把 JSON 文本读成 Python 中可遍历的列表和字典。
- `classify(...)`：把状态码翻译为“正常”“请求需要检查”或“需要处理”。规则集中在一个函数里，之后改标准不会散落各处。
- `csv.DictWriter(...)`：按固定列名写 CSV，保证表格列稳定。
- `write_markdown(...)`：按环境统计非正常项与平均耗时，再写出明细表和下一步。

### 3. 做一个自己的小改动

在 `check_results.json` 最后添加一条记录（注意前一条结尾的逗号）：

```json
{
  "environment": "staging",
  "checked_at": "2026-09-14T10:00:00+08:00",
  "name": "payments",
  "url": "https://staging.example.test/api/payments",
  "status_code": 429,
  "duration_ms": 230.0,
  "message": "rate limited"
}
```

重新运行并只查看非正常项：

```powershell
python .\build_check_dashboard.py
Import-Csv .\output\api_check_dashboard.csv |
  Where-Object result -ne '正常' |
  Format-Table environment, name, status_code, result, message
```

如果 JSON 少了逗号或多了逗号，Python 会明确报出行列位置。先按错误位置修 JSON，再运行脚本；不要手工修改 `output/`，因为它应始终由输入数据重新生成。

### 4. 审阅本次数据变更

```powershell
git status --short
git diff -- check_results.json output
git diff --check
```

检查无误后，按你第 010 课学过的流程，只暂存你确认过的输入和输出文件。

## 命令小抄

| 命令 | 它在做什么 |
| --- | --- |
| `python .\build_check_dashboard.py` | 从 JSON 重新生成两份报告产物。 |
| `Get-Content .\output\api_check_dashboard.md` | 直接阅读给人看的结论。 |
| `Import-Csv ... \| Where-Object result -ne '正常'` | 从表格筛出需要关注的行。 |
| `git diff -- check_results.json output` | 对照输入与生成结果，审阅变化是否合理。 |
| `git diff --check` | 检查空白字符等低级格式问题。 |

## 真实开发里有什么用

测试、监控和发布检查会产生大量原始结果。把它们固定地转成 CSV 和 Markdown，可以让开发者在表格中筛选、让负责人一眼看结论、让 Git 保留每次检查的证据。更重要的是：当不同环境表现不同时，报告会把“哪里坏了、慢了多少、何时检查”放在一起，减少靠记忆和聊天记录排障。

这会成为 `dev-workbench` 的报表中心：前面的日志、HTTP 检查和 Compose 检查都可以输出相同结构的 JSON，后续统一由它生成交付材料。

## 自测

如果 `local-compose` 的 `/health` 返回 200，但 `/api/orders` 返回 503，为什么不能把结论写成“系统正常”？如果要让报告能比较两次运行的趋势，你会额外保留哪个字段，为什么？

完成后，请在本目录创建 `feedback.txt`，写下最困惑的一处（JSON、列表/字典、CSV、筛选命令或报告结论）。下次会优先读取它；没有反馈则按轮换回到 Linux / Bash，练习用命令行批量核验这些报告产物。
