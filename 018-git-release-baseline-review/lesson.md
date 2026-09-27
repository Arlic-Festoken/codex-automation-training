# 018：Git——为发布门禁建立可审阅的基线

预计用时：45～55 分钟。你会为第 017 课的发布门禁写一份“现在已知什么”的基线记录，再用 Git 把它变成一条清楚、可追溯的提交。

## 先用大白话说清楚

Git 像项目的三层收纳盒：**工作区**是你正在改的文件，**暂存区**是你挑出来、准备交给下一次提交的文件，**提交历史**则是已经封存的版本。不要把“我改了东西”和“我确认这次要交什么”混成一件事。

基线不是“所有事情都正常”的证明，而是一张当前状态的快照。第 017 课已经确认：JSON、CSV、Markdown 的结构互相一致，但 `local-compose/orders` 仍是 HTTP 503。在基线里把这个例外写出来，后来的人才不会把“已知风险”误读成“新故障”，也不会把“结构通过”误读成“业务全绿”。

本课不会访问网络、不会读取凭证，也不会替你强制推送远程仓库。

## 本次小任务

1. 新建自己的 `release_baseline.md`，记录门禁的检查范围、已知例外与下一步。
2. 用 `status → diff → add 指定文件 → diff --cached → commit → show` 的顺序审阅它。
3. 在提交后确认这条提交只包含你预期的文件。

完成标准：你能指出一份改动目前位于工作区、暂存区还是历史中；并能解释为何 503 要写入基线而不是悄悄删掉。

## 跟着做

以下命令请在 **PowerShell** 中运行。先进入本课目录：

```powershell
cd C:\Users\Aa133\Desktop\codex自动化\开发者练习
git status --short
git log -3 --oneline
cd .\018-git-release-baseline-review
```

### 1. 写一份自己的基线记录

新建 `release_baseline.md`，内容可从下面开始；日期改成你实际练习的日期，`负责人`也可以写成你自己的称呼。

```markdown
# 发布基线

- 日期：2026-09-27
- 负责人：我自己
- 检查范围：第 016 课的 JSON、CSV、Markdown 产物；第 017 课的发布门禁

## 已确认

- JSON 可解析，CSV 数据行数与 JSON 记录数一致。
- Markdown 包含“结论”“明细”“下一步”。

## 已知例外

- `local-compose/orders` 返回 HTTP 503；默认门禁允许生成报告，严格模式应以退出码 2 阻断发布。

## 下一步

- 启动 Docker Desktop 后复现该接口，并判断 503 是否仍存在。
```

先只看这一个文件的改动：

```powershell
git status --short
git diff -- .\018-git-release-baseline-review\release_baseline.md
```

`git diff` 没有输出并不一定是坏事：如果文件还没被 Git 跟踪，先用 `git add -N .\018-git-release-baseline-review\release_baseline.md` 登记“意图添加”，再运行一次 `git diff`。此时它仍未进入暂存区。

### 2. 只把确认过的文件放进暂存区

不要用不带路径的 `git add .`。先精确加入这一个文件，再查看“将要提交的内容”：

```powershell
git add .\018-git-release-baseline-review\release_baseline.md
git status --short
git diff --cached -- .\018-git-release-baseline-review\release_baseline.md
```

此时 `git status --short` 左侧显示 `A`，表示这个文件已在暂存区。若你意外加进别的文件，先把它取出暂存区而不删除本地内容：

```powershell
git restore --staged .\不小心加进来的文件
git status --short
```

### 3. 创建并核对提交

确认暂存区只包含你想交的文件后再提交：

```powershell
git diff --check
git commit -m "Document release gate baseline"
git show --stat --oneline HEAD
git show --format=fuller -- .\018-git-release-baseline-review\release_baseline.md
git status --short
```

预期：最后一个 `status` 没有输出，`git show` 只展示你的基线记录。若你暂时不想提交，可以停在 `git diff --cached`：关闭终端不会丢掉暂存区，之后仍能继续审阅。

### 4. 可选：确认推送前后的远端差异

只有你已检查远端地址、且准备公开这条提交时才执行：

```powershell
git remote -v
git fetch origin
git log --oneline origin/main..HEAD
git push origin main
git ls-remote origin refs/heads/main
```

`origin/main..HEAD` 会列出“本地有、远端还没有”的提交。它为空时不需要推送。不要把账号、令牌或 `.env` 加入暂存区。

## 命令小抄

| 命令 | 它在做什么 |
| --- | --- |
| `git status --short` | 用极短格式看文件在工作区和暂存区的位置。 |
| `git diff -- 文件` | 看尚未暂存的改动。 |
| `git add 路径` | 只把指定文件放进暂存区。 |
| `git diff --cached` | 审阅下一次提交真正会包含什么。 |
| `git restore --staged 路径` | 取消暂存，保留你的本地编辑。 |
| `git show HEAD` | 复查最新提交的内容和作者时间。 |

## 真实开发里有什么用

线上故障、迁移、发布和数据修正很少是“代码全好或全坏”两种状态。可靠团队会把已知例外、检查范围和下一步固化到可审阅的提交里：代码审阅者能确认没有混入无关文件；接手的人能区分旧问题和新回归；需要撤销时也能精确定位一条提交。

它为 `dev-workbench` 增加“风险基线可追溯”的能力：后续 Python 汇总脚本可读取这类基线，报告出哪些异常已经登记、哪些是新出现的。

## 自测

假设 `git status --short` 显示一行 ` M lesson.md` 和一行 `A  release_baseline.md`：哪个文件已经暂存？你要如何确认下一次提交不会包含 `lesson.md`？为什么不应该把 HTTP 503 从基线记录中删掉来让报告看起来全绿？

完成后，请在本目录创建 `feedback.txt`，写下最卡的一处（工作区/暂存区区别、`git diff`、恢复暂存、提交信息或推送）。下次会优先读取；没有反馈则按轮换进入 Python 脚本，把这份基线和 API 检查结果汇总为一份可重复生成的发布摘要。
