# 008：数据处理——把 API 订单 JSON 变成可交付的小报告

预计用时：45～60 分钟。

## 先用大白话说清楚

数据处理就是把“机器方便传输的原料”变成“人和别的工具方便使用的结果”。`JSON` 很适合 API 返回嵌套数据；`CSV` 很适合 Excel、表格和批量导入；`Markdown` 很适合放进 README、日报或 GitHub Issue。

这不是复制粘贴：你需要先决定哪些记录有用、哪些字段要保留、怎样算总数，再把结果稳定地写进文件。这里的脚本把 `paid` 订单导出为 CSV，同时生成一份状态汇总报告。

## 本次小任务

运行 `build_report.py`，从 `orders.json` 中产出：

1. `output/paid_orders.csv`：只包含已支付订单；
2. `output/summary.md`：订单总数、已支付订单数、已支付总金额和各状态数量；
3. 自己新增一条订单，重新运行脚本，并确认两个输出都随之改变。

完成后，把你改了什么、哪个概念最容易混淆、或者看到的报错，写进本目录的 `feedback.txt`。下次会据此调整后续 Linux / Bash 练习的难度。

## 跟着做

在本目录打开 PowerShell：

```powershell
cd "C:\Users\Aa133\Desktop\codex自动化\开发者练习\008-data-processing-order-report"
python .\build_report.py
Get-ChildItem .\output
Get-Content .\output\summary.md
Import-Csv .\output\paid_orders.csv | Format-Table
```

第一次运行应看到 `Processed 6 orders`，并且：

- `paid_orders.csv` 有 4 条数据行；
- `summary.md` 的已支付总金额是 `614.00`；
- 状态统计包含 `cancelled`、`paid`、`pending`。

### 看懂脚本里的三个动作

```python
orders = json.load(file)
paid_orders = [o for o in orders if o["status"] == "paid"]
sum(order["amount"] for order in paid_orders)
```

把这三步记成：**读进来 → 挑出来 → 算出来**。`csv.DictWriter` 负责把字典列表安全地写成带表头的 CSV；`Path` 负责拼接文件路径，避免手写斜杠出错。

### 递进一步：新增一条订单

在 `orders.json` 最后的 `]` 前加入一条合法 JSON（注意上一条记录末尾需要逗号）：

```json
{"order_id": "A1007", "customer": "Zhou", "status": "paid", "amount": 99.90, "created_at": "2026-07-20T16:30:00"}
```

再运行：

```powershell
python .\build_report.py
Import-Csv .\output\paid_orders.csv | Measure-Object
Select-String -Path .\output\summary.md -Pattern "已支付"
```

你应该能解释：为什么 CSV 行数增加，汇总金额也增加；如果新增的是 `pending`，为什么金额不增加。

## 真实开发中有什么用

开发中常见的“数据处理”并不总是大数据：发布后把接口日志变成错误清单、把支付 API 的结果整理给运营、把 CI 测试结果写进 Markdown、把数据库导出转换成可审阅的表格，都是同一件事。

这节的 `build_report.py` 可以直接发展为最终 `dev-workbench` 的 `report` 子命令：前几课的 HTTP 请求拿到原始 JSON，正则和 Python 清洗数据，再由这个模块生成可交付报告；之后还能放进 Docker，在任何机器上重复运行。

## 自测

如果 `orders.json` 里有 10 条订单、其中 3 条是 `paid`，脚本为什么应该把 **10** 写进“原始订单数”，却只把 **3** 写进 `paid_orders.csv`？请用“原料、筛选条件、交付物”三个词回答。
