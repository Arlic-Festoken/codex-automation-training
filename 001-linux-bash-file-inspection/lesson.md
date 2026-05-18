# 001 Linux / Bash：用命令行完成文件巡检

建议用时：45-60 分钟

## 1. 大白话解释概念

Linux / Bash 可以先理解成“用文字操作电脑”的方式。

平时你用鼠标打开文件夹、排序、搜索、复制文件；Bash 做的是同一件事，只不过你把动作写成命令。它的好处是：动作可以保存、重复、组合。今天查 1 个文件夹，明天查 100 个项目，命令基本不用变。

几个核心概念：

- `pwd`：问电脑“我现在站在哪个文件夹里？”
- `ls`：看当前文件夹有什么。
- `cd`：进入另一个文件夹。
- `find`：按条件找文件。
- `grep`：在文本里找内容。
- `|`：管道，把前一个命令的结果交给后一个命令继续处理。

可以把管道想成流水线：第一个工人把文件列出来，第二个工人筛选 `.md`，第三个工人统计数量。

## 2. 小任务

在这个练习目录里完成一次“文件巡检”，产出一个 `inspection-report.md`。

报告需要回答 5 个问题：

1. 当前目录在哪里？
2. 这个目录下有哪些文件和文件夹？
3. 有多少个 Markdown 文件？
4. 哪些文件最近被修改过？
5. 哪些 Markdown 文件里出现了 `Bash` 这个词？

如果你在 Windows 上，可以先用 PowerShell 练习同类思路；如果你有 WSL、Git Bash、Linux 服务器，再用 Bash 命令练习一遍。

## 3. 命令示例

### Bash / Linux / Git Bash / WSL

进入练习目录：

```bash
cd "/mnt/c/Users/Aa133/Desktop/codex自动化/开发者练习"
pwd
ls -la
```

找 Markdown 文件：

```bash
find . -name "*.md"
find . -name "*.md" | wc -l
```

查看最近修改的文件：

```bash
find . -type f -printf "%TY-%Tm-%Td %TH:%TM %p\n" | sort -r | head -10
```

搜索包含 `Bash` 的 Markdown 文件：

```bash
grep -RIn --include="*.md" "Bash" .
```

把结果写进报告：

```bash
{
  echo "# 文件巡检报告"
  echo
  echo "## 当前目录"
  pwd
  echo
  echo "## Markdown 文件数量"
  find . -name "*.md" | wc -l
  echo
  echo "## 包含 Bash 的位置"
  grep -RIn --include="*.md" "Bash" . || true
} > inspection-report.md
```

### PowerShell 对照

进入练习目录：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习"
Get-Location
Get-ChildItem -Force
```

找 Markdown 文件并统计数量：

```powershell
Get-ChildItem -Recurse -Filter *.md
(Get-ChildItem -Recurse -Filter *.md).Count
```

查看最近修改的文件：

```powershell
Get-ChildItem -Recurse -File |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 10 FullName, LastWriteTime
```

搜索包含 `Bash` 的 Markdown 文件：

```powershell
Get-ChildItem -Recurse -Filter *.md |
  Select-String -Pattern "Bash"
```

生成报告：

```powershell
$root = "C:\Users\Aa133\Desktop\codex自动化\开发者练习"
Set-Location $root

$report = @()
$report += "# 文件巡检报告"
$report += ""
$report += "## 当前目录"
$report += (Get-Location).Path
$report += ""
$report += "## Markdown 文件数量"
$report += (Get-ChildItem -Recurse -Filter *.md).Count
$report += ""
$report += "## 最近修改文件"
$report += Get-ChildItem -Recurse -File |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 10 |
  ForEach-Object { "- $($_.LastWriteTime) $($_.FullName)" }
$report += ""
$report += "## 包含 Bash 的位置"
$report += Get-ChildItem -Recurse -Filter *.md |
  Select-String -Pattern "Bash" |
  ForEach-Object { "- $($_.Path):$($_.LineNumber) $($_.Line.Trim())" }

$report | Set-Content -Encoding UTF8 inspection-report.md
```

## 4. 真实开发中有什么用

这个技能非常基础，但一点都不低级。真实开发里，你经常需要快速回答这些问题：

- 这个项目入口文件在哪里？
- 哪些文件最近被改过？
- 某个配置项到底出现在哪些地方？
- 日志里有没有错误关键词？
- 提交代码前，有没有把临时文件、输出文件、密钥文件也带进去？

会 Bash / 命令行巡检后，你不需要一个个点开文件夹。你可以直接把项目当成“可查询的数据”来处理。

## 5. 自测问题

如果你想找出当前目录下所有 `.txt` 文件，并搜索其中包含 `error` 的行，Bash 命令应该怎么写？

提示：你可能会用到 `find`、`grep`，或者直接用 `grep -RIn --include="*.txt"`。

## 完成后反馈

做完后，在这个文件夹里新建一个 `.txt`，写 3 行就够：

1. 哪个概念最清楚？
2. 哪个命令最卡？
3. 下次你想要“更简单解释”还是“更真实任务”？

