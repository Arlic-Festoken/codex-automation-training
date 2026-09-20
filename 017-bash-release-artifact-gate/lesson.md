# 017：Linux / Bash——给交付报告加一道发布前检查

预计用时：45～55 分钟。你会用一个 Bash 脚本批量核验第 016 课生成的 JSON、CSV 和 Markdown，区分“文件格式没问题”与“业务结果仍有风险”，并让脚本在严格模式下安全地拒绝发布。

## 先用大白话说清楚

发布前检查就像寄快递前的验货：箱子没破、地址写了、清单对得上，是“结构没问题”；但如果清单上写着某个零件坏了，箱子再完整也不能说货物一切正常。

Bash 是把几条命令固定成一个可重复流程的工具。这里它不替你猜结论：先确认三个文件都在，检查 JSON 能否解析、CSV 行数是否和 JSON 对得上、Markdown 是否有结论和下一步；然后再提示业务接口是否异常。加上 `set -euo pipefail` 后，漏文件、变量拼错或中间命令失败都会尽早停下，不会继续产出一份看似可信的假结果。

本课只读取本地教学数据，不会访问网络，也没有真实凭证。

## 本次小任务

1. 用脚本巡检第 016 课的 `check_results.json`、CSV 和 Markdown 报告。
2. 看懂默认模式为何能完成“结构巡检”却仍提示 `orders` 的 503。
3. 用严格模式让脚本以退出码 `2` 拒绝包含非正常接口的发布。
4. 自己把 JSON 中的一条字段或 CSV 中的一行临时改坏，观察失败信息；随后用 Python 重新生成产物恢复它。

完成标准：你能说清“报告能被读取”与“报告可以宣称全部正常”的区别，并会用退出码让自动化流程停在风险点。

## 跟着做

本课需要 Git Bash 或一个可用的 Linux/WSL Bash。PowerShell 的语法不同；请在 Git Bash 终端运行下面命令。当前电脑的 WSL 没有可用 Linux 发行版，因此本次先完成阅读和脚本审阅；安装 Git for Windows 后即可实际运行。

### 1. 先做普通巡检

```bash
cd /c/Users/Aa133/Desktop/codex自动化/开发者练习/017-bash-release-artifact-gate
bash inspect_release_artifacts.sh
echo "上一条命令的退出码：$?"
```

预期：前三项通过；第 4 项会列出 `local-compose/orders: HTTP 503`。默认模式退出码仍是 `0`，因为它回答的是“产物是否相互一致”，而不是掩盖业务风险。

### 2. 用严格模式模拟发布门禁

```bash
bash inspect_release_artifacts.sh --strict
echo "上一条命令的退出码：$?"
```

预期：最后显示“拒绝通过”，退出码是 `2`。在 CI、发布脚本或提交前检查中，非零退出码会停止后续动作，避免把“有已知异常”的结果误发成绿色报告。

若你要确认退出码而不想让当前终端把失败当异常，可以这样写：

```bash
if bash inspect_release_artifacts.sh --strict; then
  echo "可以继续发布"
else
  echo "先处理接口异常，再发布"
fi
```

### 3. 故意制造一个可恢复的问题

先备份 CSV，再删除它的最后一条数据行：

```bash
cd ../016-data-processing-api-check-dashboard
cp output/api_check_dashboard.csv output/api_check_dashboard.csv.bak
sed -i '$d' output/api_check_dashboard.csv
cd ../017-bash-release-artifact-gate
bash inspect_release_artifacts.sh
```

它会告诉你 CSV 行数与 JSON 不一致。不要手工补报告；回到数据的来源重新生成：

```bash
cd ../016-data-processing-api-check-dashboard
python build_check_dashboard.py
rm output/api_check_dashboard.csv.bak
cd ../017-bash-release-artifact-gate
bash inspect_release_artifacts.sh
```

### 4. 看懂脚本里的关键写法

```bash
rg -n 'set -euo pipefail|require_file|json.tool|expected_header|STRICT_MODE|exit 2' inspect_release_artifacts.sh
git diff --check
```

- `require_file`：把“文件不存在就停止”的规则写一次，避免遗漏。
- `python -m json.tool`：用 Python 标准库验证 JSON，不需要安装 `jq`。
- `head`、`tail`、`grep`、`awk`：从很大的文本表格中只取需要检查的部分。
- `--strict` 与 `exit 2`：把“发现业务风险”变成机器可识别的阻断信号；`1` 留给缺文件、格式错误等脚本/产物问题。

## 命令小抄

| 命令 | 它在做什么 |
| --- | --- |
| `bash inspect_release_artifacts.sh` | 核验三个交付产物是否存在、可读且相互一致。 |
| `bash inspect_release_artifacts.sh --strict` | 若有非正常接口，以退出码 2 阻止继续。 |
| `python -m json.tool check_results.json` | 验证 JSON 语法并格式化输出。 |
| `head -n 1 file.csv` | 只看 CSV 的表头。 |
| `tail -n +2 file.csv` | 跳过表头，只处理数据行。 |
| `grep -q '文本' file` | 静默确认一个关键文本是否存在。 |

## 真实开发里有什么用

CI、日报、迁移和发布经常依赖机器生成的 CSV、JSON、Markdown。只检查文件存在会遗漏“少导了一行”；只看 HTTP 200/503 会遗漏“报告有没有被错误截断”。这类门禁脚本将结构完整性、产物一致性和业务风险分层：格式错误直接失败，已知故障清晰暴露，严格环境则可靠地拦住发布。

它会成为 `dev-workbench` 的发布前巡检入口：以后日志摘要、API 检查和其他报表都可以复用同一个“先校验，再决定是否放行”的模式。

## 自测

为什么 `bash inspect_release_artifacts.sh` 在发现 503 时仍可以返回 `0`，而 `--strict` 要返回 `2`？如果你在 CI 中只想阻止格式损坏、但允许已登记的业务故障继续生成日报，应该选哪个模式，为什么？

完成后，请在本目录创建 `feedback.txt`，记录最困惑的一处（Bash 路径、管道、退出码、`awk` 或“结构检查和业务结论的区别”）。下次会优先读取它；没有反馈则按轮换进入 Git，围绕本次检查产物做一次可审阅的“基线/例外”提交。
