# 003 Python 脚本：把日志整理成一份小报告

建议用时：45-60 分钟

## 1. 大白话解释概念

Python 脚本可以先理解成“把你本来要手工重复做的步骤，写成一张可重复执行的清单”。

比如你拿到一份日志，手工看大概会这样做：

1. 打开文件。
2. 一行一行看。
3. 数一数有多少个 `ERROR`、`WARN`、`INFO`。
4. 找出哪些接口经常出问题。
5. 把结果写进一个报告。

Python 做的就是把这些动作写下来，让电脑稳定地重复执行。今天先不追求复杂语法，只抓住 4 个核心动作：

- 读文件：从磁盘拿到文本内容。
- 循环：一行一行处理。
- 判断：看到 `ERROR` 就归到错误类，看到 `WARN` 就归到警告类。
- 写文件：把统计结果保存成新的 Markdown 报告。

可以把 Python 想成一个很听话的实习生：你不能只说“帮我分析一下”，你要告诉它“打开哪个文件、看哪些词、怎么计数、写到哪里”。描述得越清楚，结果越稳定。

## 2. 小任务

在本文件夹里完成一个“日志摘要器”：

输入文件：

- `sample_logs/app.log`

你要写一个脚本：

- `analyze_logs.py`

运行后生成：

- `log-summary.md`

报告至少包含 4 部分：

1. 日志总行数。
2. `INFO`、`WARN`、`ERROR` 各有多少行。
3. 出现过 `ERROR` 的接口路径。
4. 你对这份日志的 2-3 句人工判断。

这次不要先追求“完美通用”。先让脚本能稳定处理给定的示例日志。

## 3. 命令示例

### Bash / Linux / Git Bash / WSL

进入练习目录：

```bash
cd "/mnt/c/Users/Aa133/Desktop/codex自动化/开发者练习/003-python-log-summary"
ls -la
```

确认 Python 可用：

```bash
python --version
# 如果上面不行，试试：
python3 --version
```

创建脚本：

```bash
cat > analyze_logs.py <<'PY'
from pathlib import Path

log_path = Path("sample_logs/app.log")
report_path = Path("log-summary.md")

lines = log_path.read_text(encoding="utf-8").splitlines()

level_counts = {
    "INFO": 0,
    "WARN": 0,
    "ERROR": 0,
}
error_paths = []

for line in lines:
    for level in level_counts:
        if f" {level} " in line:
            level_counts[level] += 1

    if " ERROR " in line:
        parts = line.split()
        # 示例日志里接口路径放在第 3 列，例如 /api/login。
        if len(parts) >= 3:
            error_paths.append(parts[2])

unique_error_paths = sorted(set(error_paths))

report = []
report.append("# 日志摘要报告")
report.append("")
report.append(f"- 日志总行数：{len(lines)}")
report.append(f"- INFO 行数：{level_counts['INFO']}")
report.append(f"- WARN 行数：{level_counts['WARN']}")
report.append(f"- ERROR 行数：{level_counts['ERROR']}")
report.append("")
report.append("## 出现 ERROR 的接口")

if unique_error_paths:
    for path in unique_error_paths:
        report.append(f"- {path}")
else:
    report.append("- 没有发现 ERROR 接口")

report.append("")
report.append("## 人工判断")
report.append("")
report.append("- 这里先写你自己的观察：哪个接口最值得优先检查？")
report.append("- 这里再写一句：你会先看日志里的哪类信息？")

report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
print(f"已生成 {report_path}")
PY
```

运行脚本：

```bash
python analyze_logs.py
cat log-summary.md
```

把结果提交到 Git：

```bash
git status --short
git add analyze_logs.py log-summary.md
git commit -m "Add Python log summary practice output"
```

### PowerShell 对照

进入练习目录：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习\003-python-log-summary"
Get-ChildItem -Force
```

确认 Python 可用：

```powershell
python --version
```

创建脚本：

```powershell
$script = @'
from pathlib import Path

log_path = Path("sample_logs/app.log")
report_path = Path("log-summary.md")

lines = log_path.read_text(encoding="utf-8").splitlines()

level_counts = {
    "INFO": 0,
    "WARN": 0,
    "ERROR": 0,
}
error_paths = []

for line in lines:
    for level in level_counts:
        if f" {level} " in line:
            level_counts[level] += 1

    if " ERROR " in line:
        parts = line.split()
        # 示例日志里接口路径放在第 3 列，例如 /api/login。
        if len(parts) >= 3:
            error_paths.append(parts[2])

unique_error_paths = sorted(set(error_paths))

report = []
report.append("# 日志摘要报告")
report.append("")
report.append(f"- 日志总行数：{len(lines)}")
report.append(f"- INFO 行数：{level_counts['INFO']}")
report.append(f"- WARN 行数：{level_counts['WARN']}")
report.append(f"- ERROR 行数：{level_counts['ERROR']}")
report.append("")
report.append("## 出现 ERROR 的接口")

if unique_error_paths:
    for path in unique_error_paths:
        report.append(f"- {path}")
else:
    report.append("- 没有发现 ERROR 接口")

report.append("")
report.append("## 人工判断")
report.append("")
report.append("- 这里先写你自己的观察：哪个接口最值得优先检查？")
report.append("- 这里再写一句：你会先看日志里的哪类信息？")

report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
print(f"已生成 {report_path}")
'@

$script | Set-Content -Encoding UTF8 "analyze_logs.py"
```

运行脚本：

```powershell
python .\analyze_logs.py
Get-Content -Encoding UTF8 .\log-summary.md
```

把结果提交到 Git：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习"
git status --short
git add "003-python-log-summary/analyze_logs.py" "003-python-log-summary/log-summary.md"
git commit -m "Add Python log summary practice output"
```

## 4. 这个技能在真实开发中有什么用

Python 脚本在真实开发里经常用来做“胶水工作”：它不一定是最终产品，但能把很多杂事自动化。

常见场景包括：

- 批量整理日志，快速判断线上问题集中在哪个接口。
- 把一堆文本、CSV、JSON 转成统一报告。
- 提交代码前自动检查文件、命名、配置。
- 从 API 拉数据，再生成日报或排查材料。
- 把一次手工操作沉淀成团队都能复用的小工具。

这次练习的价值不是“会写一个统计日志的脚本”这么窄，而是开始建立一个思路：只要一个动作有固定输入、固定规则、固定输出，就可以尝试脚本化。

## 5. 自测问题

如果你想把脚本改成“只统计包含 `/api/orders` 的日志行”，你会把判断条件加在循环的哪个位置？

请用大白话回答即可：是先筛行，再统计级别；还是先统计所有级别，再筛接口？为什么？

## 完成后反馈

做完后，在这个文件夹里放一个 `.txt`，写 3 行就够：

1. 你能不能看懂 `Path("sample_logs/app.log")` 这句？
2. `for line in lines` 和 `if " ERROR " in line` 哪个更卡？
3. 下次正则表达式练习，你想继续分析日志，还是换成整理文件名？
