# 010：Git——审阅一次报告改动，再做一个干净提交

预计用时：45～55 分钟。你会在现有的 `dev-workbench` 练习仓库里，写一条小型运行说明，然后只提交自己确认过的改动。

## 先用大白话说清楚

Git 可以把项目想成有三个区域：

- **工作区**：你正在编辑的文件；`git status` 会告诉你这里有什么变化。
- **暂存区**：你明确挑出来、准备放进下一次提交的文件；`git add` 不是“保存全部”，而是“把这一版选进包裹”。
- **提交历史**：已经封好的包裹；每个提交都应当能回答“改了什么、为什么改”。

所以一次可靠的提交不是“看到有文件就全选”，而是：先看状态，再看具体差异，只暂存本次任务需要的文件，最后检查暂存区后再提交。

## 本次小任务

为订单报告模块添加一份你自己的运行复盘，然后完成一次干净提交。

1. 新建 `010-git-report-change-review/my_report_review.md`。
2. 用下面的模板写 3～6 行：报告如何生成、你检查过什么、你还想改进什么。不要写真实账号、密钥或隐私数据。
3. 用 Git 审阅改动，并且**只**暂存这份复盘文件；如果看到其他陌生改动，先不要提交它们。
4. 创建一条清楚的提交，例如：`Add report review notes`。

完成标准：`git status` 显示工作区干净，并且 `git log -1 --oneline` 能看到你的提交。

复盘模板：

```markdown
# 订单报告复盘

- 生成命令：`python .\\build_report.py`
- 我检查了：已支付订单数量、总金额、CSV 数据行。
- 下次想改进：……
```

## 跟着做

在 PowerShell 中进入训练仓库：

```powershell
cd "C:\Users\Aa133\Desktop\codex自动化\开发者练习"
git status
git log -3 --oneline
```

先确认你正在哪个分支，以及上一节新增的 Bash 巡检文件是否真的在历史里：

```powershell
git branch --show-current
git show --stat --oneline HEAD
git show --name-only --format="" HEAD
```

创建并编辑复盘文件。用 VS Code 打开当前目录最方便：

```powershell
code .
```

保存 `010-git-report-change-review\my_report_review.md` 后，不急着提交，先审阅：

```powershell
git status --short
git diff -- 010-git-report-change-review/my_report_review.md
```

确认内容正确后，只把这一份文件放进暂存区：

```powershell
git add -- 010-git-report-change-review/my_report_review.md
git diff --cached -- 010-git-report-change-review/my_report_review.md
git status
```

这里最关键的是 `git diff --cached`：它显示的才是“即将被提交的版本”。确认无误后提交：

```powershell
git commit -m "Add report review notes"
git log -1 --oneline
git status
```

如果你不小心暂存了不该提交的文件，不要删除文件内容；只把它从暂存区取回工作区：

```powershell
git restore --staged -- 路径/文件名
git status
```

## 命令小抄

| 命令 | 它回答的问题 |
| --- | --- |
| `git status` | 哪些文件变了？哪些已暂存？ |
| `git diff` | 工作区中还没暂存的改动具体是什么？ |
| `git add -- 文件` | 我只想把哪一份文件放进这次提交？ |
| `git diff --cached` | 下一次提交里究竟会有什么？ |
| `git log -1 --oneline` | 刚刚的提交是否真的写进历史？ |
| `git restore --staged -- 文件` | 怎么取消暂存、但保留我写的内容？ |

## 真实开发里有什么用

代码评审、线上问题修复和多人协作中，最危险的情况之一是把无关调试文件、半成品或别人的改动一起带进提交。`status → diff → add 指定文件 → diff --cached → commit` 这条小流程能让每一次改动可审阅、可回退，也让其他人一眼看懂你为什么改。

这一节给 `dev-workbench` 补上“变更可追溯”的能力：前面能生成并检查订单报告；现在你能为结果留下经过审阅的记录。下一轮 Python 会把这个复盘流程再自动化一点。

## 自测

`git diff` 和 `git diff --cached` 分别在看哪个区域？如果你发现暂存区里混入了 `debug.txt`，但想保留它在电脑上，应使用哪条命令？

做完后，可以在本目录放一个 `feedback.txt`，写下最容易混淆的一条 Git 命令或实际报错；下一次练习会优先据此调整。
