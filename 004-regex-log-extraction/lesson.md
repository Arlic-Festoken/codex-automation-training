# 004 正则表达式：从混杂日志里提取可用信息

建议用时：50-60 分钟

## 1. 大白话解释概念

正则表达式可以理解成“描述文本长什么样的模板”。

普通搜索只能问：“这行里有没有 `ERROR`？”  
正则还能问：“这行里有没有一个三位状态码、一个接口路径，以及以 `ms` 结尾的耗时？”

例如：

```text
status=503 path=/api/orders duration=842ms
```

可以拆成几种形状：

- `\d+`：一个或多个数字，例如 `503`、`842`
- `\S+`：一个或多个非空白字符，例如 `/api/orders`
- `(...)`：把匹配到的某一段单独抓出来
- `^` 和 `$`：限定必须从行首开始、到行尾结束

正则最容易踩的坑是“匹配得太宽”。例如 `.*` 像一个什么都吃的袋子，虽然常常能匹配成功，但可能把不该要的内容也吞进去。真实开发中要优先写出“够用、可读、能验证”的规则，不追求一条正则解决所有问题。

## 2. 小任务

处理本目录的 `sample_access.log`，找出所有失败请求，并生成 `failed-requests.md`。

失败请求定义：

- HTTP 状态码为 `400-599`

报告至少包含：

1. 失败请求总数。
2. 每条失败请求的时间、状态码、接口路径和耗时。
3. 去重后的失败接口列表。
4. 你认为最需要优先排查的接口，以及理由。

推荐拆成两步：

1. 先用 `rg` 或 `grep` 验证正则，确认哪些行会被匹配。
2. 再写 `extract_failures.py`，使用 Python 的 `re` 模块提取字段并生成 Markdown。

## 3. 命令示例

### 第一步：先看数据

PowerShell：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习\004-regex-log-extraction"
Get-Content .\sample_access.log
```

Bash / Git Bash / WSL：

```bash
cd "/mnt/c/Users/Aa133/Desktop/codex自动化/开发者练习/004-regex-log-extraction"
cat sample_access.log
```

### 第二步：用命令行试正则

找出状态码为 `4xx` 或 `5xx` 的行：

```bash
rg 'status=[45][0-9]{2}' sample_access.log
```

只显示接口路径：

```bash
rg -o 'path=/[^ ]+' sample_access.log
```

找出失败请求，并观察状态码、路径和耗时是否都存在：

```bash
rg 'status=[45][0-9]{2} path=/[^ ]+ duration=[0-9]+ms' sample_access.log
```

这些规则分别表示：

- `[45]`：这一位只能是 `4` 或 `5`
- `[0-9]{2}`：后面必须再有两个数字
- `/[^ ]+`：从 `/` 开始，一直匹配到空格之前
- `[0-9]+ms`：一个或多个数字，后面紧跟 `ms`

### 第三步：在 Python 中提取字段

先创建 `extract_failures.py`，从这个骨架开始：

```python
import re
from pathlib import Path

log_path = Path("sample_access.log")
report_path = Path("failed-requests.md")

pattern = re.compile(
    r"^(?P<time>\S+) "
    r"request_id=(?P<request_id>\S+) "
    r"status=(?P<status>[45][0-9]{2}) "
    r"path=(?P<path>/\S+) "
    r"duration=(?P<duration>[0-9]+)ms$"
)

failures = []

for line in log_path.read_text(encoding="utf-8").splitlines():
    match = pattern.match(line)
    if match:
        failures.append(match.groupdict())

# TODO：把 failures 整理成 Markdown 并写入 report_path。
```

运行并查看结果：

```powershell
python .\extract_failures.py
Get-Content .\failed-requests.md
```

调试时可以临时加入：

```python
print(match.groupdict())
```

预期抓到的失败请求数是 `5`。如果不是，先检查正则，不要急着写报告。

## 4. 这个技能在真实开发中有什么用

正则经常出现在这些工作里：

- 从应用日志里提取状态码、接口、请求 ID 和错误信息。
- 在代码库里批量定位旧 API、危险配置或待迁移写法。
- 校验输入格式，例如版本号、文件名、简单标识符。
- 清洗数据，把半结构化文本变成 CSV、JSON 或报告。
- 给监控告警定义规则，快速找到异常请求。

这次练习会直接成为最终项目 `dev-workbench` 的“日志字段提取”能力。后续 HTTP / API 练习会产生新的请求数据，再复用这里的正则做分析。

## 5. 进阶挑战

基础任务做完后任选一个，不必全部做：

- 在报告里按状态码统计数量。
- 按耗时从高到低排列失败请求。
- 修改正则，让它也能处理字段顺序改变的日志。
- 为无法匹配的行增加一个 `unmatched-lines.md` 报告。

## 6. 自测问题

下面两个正则都可能匹配接口路径，它们有什么差别？哪一个在日志处理中更稳妥？

```regex
path=(.*)
```

```regex
path=(/[^ ]+)
```

请把答案和练习感受写到本目录的 `feedback.txt`。至少记录：

- 哪个符号最难理解？
- 你的实际失败请求数是多少？
- 你希望下一课 HTTP / API 更偏命令行调用，还是更偏 Python 请求脚本？
