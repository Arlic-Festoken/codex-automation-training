# 002 Git：看懂变更并做一次干净提交

建议用时：45-60 分钟

## 1. 大白话解释概念

Git 可以先理解成“项目的时间机器”，但更准确一点，它是“有选择地记录项目变化”的工具。

你平时写代码、改文档、删文件，电脑只知道文件变了；Git 会帮你回答更开发者化的问题：

- 哪些文件变了？
- 每个文件具体改了哪几行？
- 哪些改动准备提交，哪些还没准备？
- 这次提交到底解决了什么问题？
- 如果以后出错，能不能定位是哪次改动引入的？

今天先练最核心的一条线：

```text
status -> diff -> add -> commit -> log
```

可以把它理解成一次“交作业”流程：

- `git status`：先看桌面上有哪些作业纸还没收拾。
- `git diff`：逐行检查自己到底写了什么。
- `git add`：把确认要交的内容放进提交篮子。
- `git commit`：正式封存成一次有名字的记录。
- `git log`：回头查看交作业历史。

这里最重要的习惯不是“赶快 commit”，而是 commit 前先问自己一句：这次记录是不是一个清楚的小单元？

## 2. 小任务

在本目录完成一次“Git 最小真实工作流”练习，最后产出一个 `git-practice-notes.md`，并提交到 Git。

任务分 4 步：

1. 新建 `git-practice-notes.md`。
2. 写入 3 小节：`我改了什么`、`我怎么检查`、`这次提交为什么值得记录`。
3. 用 Git 查看变更、检查差异、加入暂存区并提交。
4. 用 `git log` 确认提交已经存在。

额外要求：不要一次性跳到 `git add .`。今天先明确写出文件名，训练“我知道自己要提交什么”的习惯。

## 3. 命令示例

### Bash / Linux / Git Bash / WSL

进入练习仓库：

```bash
cd "/mnt/c/Users/Aa133/Desktop/codex自动化/开发者练习"
git status
```

新建练习笔记：

```bash
cat > 002-git-status-commit-workflow/git-practice-notes.md <<'EOF'
# Git 练习笔记

## 我改了什么

我新增了一个练习笔记，用来记录 Git 提交流程。

## 我怎么检查

我会先用 git status 看文件状态，再用 git diff 看具体内容。

## 这次提交为什么值得记录

这是一份独立的练习成果，适合单独提交。
EOF
```

查看当前状态：

```bash
git status --short
```

查看具体改动：

```bash
git diff -- 002-git-status-commit-workflow/git-practice-notes.md
```

把这个文件放进暂存区：

```bash
git add 002-git-status-commit-workflow/git-practice-notes.md
git status --short
```

提交：

```bash
git commit -m "Add Git practice notes"
```

查看提交历史：

```bash
git log --oneline -5
```

### PowerShell 对照

进入练习仓库：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习"
git status
```

新建练习笔记：

```powershell
$note = @"
# Git 练习笔记

## 我改了什么

我新增了一个练习笔记，用来记录 Git 提交流程。

## 我怎么检查

我会先用 git status 看文件状态，再用 git diff 看具体内容。

## 这次提交为什么值得记录

这是一份独立的练习成果，适合单独提交。
"@

$note | Set-Content -Encoding UTF8 "002-git-status-commit-workflow\git-practice-notes.md"
```

查看当前状态：

```powershell
git status --short
```

查看具体改动：

```powershell
git diff -- "002-git-status-commit-workflow/git-practice-notes.md"
```

暂存并提交：

```powershell
git add "002-git-status-commit-workflow/git-practice-notes.md"
git status --short
git commit -m "Add Git practice notes"
```

查看提交历史：

```powershell
git log --oneline -5
```

### 读懂 `git status --short`

常见输出长这样：

```text
?? new-file.md
 M old-file.md
A  staged-file.md
M  staged-change.md
```

含义：

- `??`：Git 还没跟踪的新文件。
- ` M`：文件被改了，但还没放进暂存区。
- `A `：新文件已经放进暂存区，下一次 commit 会记录它。
- `M `：修改已经放进暂存区。

左边第一列偏向“已暂存”，第二列偏向“工作区”。现在不用背得很细，只要记住：`git status` 是提交前的体检单。

## 4. 真实开发中有什么用

Git 的价值不是“保存一下”，而是让团队和未来的自己看得懂项目怎么变成现在这样。

真实开发里它会用在这些地方：

- 提交前确认没有把临时文件、密码、调试输出带进去。
- 出 bug 时用提交历史追踪“问题从哪次改动开始出现”。
- 多人协作时，让别人知道你这次改动的边界。
- 做代码评审时，把一大坨变化拆成能理解的小块。
- 自动化部署时，服务器通常根据某次 Git 提交来构建和发布。

一个好提交通常满足 3 点：

- 小：只做一件事。
- 清楚：提交信息能说明目的。
- 可检查：别人能通过 diff 看懂你改了哪里。

## 5. 自测问题

如果 `git status --short` 显示：

```text
 M README.md
?? notes.txt
```

你只想提交 `README.md` 的改动，不想提交 `notes.txt`，应该先运行哪条 `git add` 命令？为什么不建议在这里直接用 `git add .`？

## 完成后反馈

做完后，在这个文件夹里放一个 `.txt`，写 3 行就够：

1. `git status` 的输出你能不能看懂？
2. `git diff` 哪一部分最容易困惑？
3. 下次 Git 练习你想继续“分支”还是先练“撤销误操作”？
