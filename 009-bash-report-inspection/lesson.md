# 009：Linux / Bash——用脚本巡检一份可交付报告

预计用时：45～60 分钟。Windows 用户请用 **Git Bash** 或 **WSL** 完成；PowerShell 命令与 Bash 不完全相同，这正是本节要建立的边界意识。

## 先用大白话说清楚

`Bash` 是一种让你把多条命令写成“可重复执行的说明书”的工具。你不必每次手工打开文件、数 CSV 行、查报告金额；把这些动作写进脚本后，只需给它一个目录，它就会按同一套规则检查。

脚本中的三个关键点：

- `"${1:-默认值}"`：把第一个输入当作目录；没输入时就使用默认目录；
- `if [[ ... ]]`：先验证前提，避免在错误目录里悄悄给出错误结论；
- `find`、`grep`、`wc`：分别负责找文件、找关键信息、计数。

这节不是背命令。核心是把“我如何确认报告真的产出了正确文件”变成一个可复用的检查流程。

## 本次小任务

运行 `inspect_report.sh`，让它检查第 008 课生成的订单报告，并完成这三件事：

1. 确认 `summary.md` 与 `paid_orders.csv` 都存在；
2. 从输出中读出已支付订单数、总金额和 CSV 数据行数；
3. 故意传入一个不存在的目录，观察脚本如何提前失败；然后恢复正确命令。

完成后，在本目录新增 `feedback.txt`，写下你最不确定的一条命令或实际看到的报错。下次 Git 练习会优先利用这份反馈调整难度。

## 跟着做

先确保第 008 课的报告是新的。在 **PowerShell** 中：

```powershell
cd "C:\Users\Aa133\Desktop\codex自动化\开发者练习\008-data-processing-order-report"
python .\build_report.py
```

然后打开 **Git Bash**，运行：

```bash
cd /c/Users/Aa133/Desktop/codex自动化/开发者练习/009-bash-report-inspection
bash inspect_report.sh
```

正常情况下，应至少看到：

```text
已支付订单数：4
已支付总金额：614.00
paid_orders.csv: 4 条已支付订单
```

### 看懂并验证每一步

```bash
# 只看输出目录第一层的文件；-type f 表示普通文件
find ../008-data-processing-order-report/output -maxdepth 1 -type f

# 只从 Markdown 中找三个关键字段；-E 允许使用“或”
grep -E '原始订单数|已支付订单数|已支付总金额' ../008-data-processing-order-report/output/summary.md

# 跳过 CSV 的表头，再统计真正的数据行
tail -n +2 ../008-data-processing-order-report/output/paid_orders.csv | wc -l
```

### 故意触发一次安全失败

```bash
bash inspect_report.sh ./does-not-exist
echo $?
```

应该先看到“找不到报告目录”，随后 `$?` 是 `1`。这表示脚本在前提不满足时明确停止，而不是继续输出不可信结果。

### 递进一步：检查另一份报告目录

脚本把目录设计成参数，所以可以检查任何具有同样文件结构的报告：

```bash
bash inspect_report.sh ../008-data-processing-order-report/output
```

试着把 `REPORT_DIR` 的默认目录临时改错，再运行一次；理解为什么脚本参数比把路径硬编码在每条命令里更灵活。恢复原样后再继续。

## 真实开发中有什么用

CI、发布前检查、数据导入和定时任务都需要“先确认输入与产物，再输出结论”。例如夜间报表生成后用 Bash 检查文件是否存在、日志分析后统计错误数、发布前确认构建产物没有缺失。`set -euo pipefail` 和明确的目录检查，能把很多“脚本看似跑完、结果却是错的”问题提前暴露。

本节的脚本会成为最终 `dev-workbench` 的巡检入口：第 008 课负责生成报告，这里负责验证报告。下一节 Git 会把这种可验证的改动整理成清晰历史。

## 自测

为什么 `tail -n +2 paid_orders.csv | wc -l` 比直接 `wc -l paid_orders.csv` 更接近“订单数量”？请用“表头、数据行、交付结论”三个词回答。
