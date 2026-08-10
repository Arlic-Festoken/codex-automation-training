# 011：Python——把零散结果汇总成项目状态摘要

预计用时：45～55 分钟。你会运行一个小脚本，读取已有订单报告和 Git 信息，生成一份可重复更新的项目状态摘要，并为它加上一条自己的检查。

## 先用大白话说清楚

开发里常有这样的碎片：一个报告在这里、一次提交在那里、自己写的复盘又在另一个文件夹。每次要汇报进度时，如果靠手工复制，很容易漏掉或写成旧信息。

Python 脚本就是把这套“找资料 → 摘要 → 写报告”的固定流程交给电脑。今天的脚本像一位只做事实记录的项目助理：`Path` 定位文件，`read_text()` 读取已有报告，`subprocess.run()` 运行只读 Git 命令，`write_text()` 保存 Markdown。它每次重新读取当前文件和 Git 状态，因此可反复运行。

## 本次小任务

1. 运行脚本，生成 `output/project_status.md`。
2. 打开生成文件，确认它包含订单报告、当前 Git 分支、生成时最近提交和学习复盘。
3. 在 `build_project_status.py` 的 `## 下一步` 下，添加一条自己的状态检查，例如“确认已支付订单数为 4”。
4. 重新运行脚本，确认新增检查出现在 Markdown 中。
5. 用 Git 审阅并提交你确认过的脚本与生成结果；不要把陌生改动一起提交。

完成标准：摘要和当前 Git 状态一致；新增检查可见；提交后 `git status` 干净。

## 跟着做

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习\011-python-project-status-summary"
python --version
python .\build_project_status.py
Get-Content -Encoding UTF8 .\output\project_status.md
```

`--output` 可把同一个脚本的结果写到另一个位置：

```powershell
python .\build_project_status.py --output output\project_status_draft.md
Get-Content -Encoding UTF8 .\output\project_status_draft.md
```

在 VS Code 打开 `build_project_status.py`，找到 `## 下一步` 对应的 `lines` 列表，加入这类 Markdown 列表项并保存：

```python
"- 检查：已支付订单数应为 4；不一致时先重新运行订单报告脚本。",
```

重新生成并验证：

```powershell
python .\build_project_status.py
Select-String -Path .\output\project_status.md -Pattern "已支付订单数"
```

最后从训练仓库根目录审阅并提交：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习"
git status --short
git diff -- 011-python-project-status-summary
git add -- 011-python-project-status-summary/build_project_status.py 011-python-project-status-summary/output/project_status.md
git diff --cached -- 011-python-project-status-summary
git commit -m "Add project status summary"
git status
```

若还没完成第 010 课的个人复盘，摘要会显示“尚未添加个人报告复盘”；这是正常提示。完成复盘后重新运行脚本，摘要会自动更新。

## 命令小抄

| 命令或写法 | 它在做什么 |
| --- | --- |
| `Path(__file__).parent` | 找到脚本所在文件夹，不依赖当前命令行目录。 |
| `path.exists()` | 文件存在才读取；不存在就给清楚提示。 |
| `subprocess.run([...], check=False)` | 运行外部命令，但 Git 信息暂时不可读时不直接崩溃。 |
| `python script.py --output 路径` | 用同一脚本生成不同位置的输出。 |
| `git diff -- 路径` | 提交前只查看本节相关的未暂存改动。 |

## 真实开发里有什么用

项目状态摘要器常把测试结果、构建版本、接口检查、Git 提交和数据处理结果汇总进日报、发布记录或 issue。价值不是 Markdown 本身，而是把手工汇报变成可重复、能校验、不容易过期的流程。

它也把前面的练习串成项目雏形：第 008 课生成订单报告，第 009 课检查报告，第 010 课留下变更复盘，这一课把它们汇总。下一轮正则表达式会让摘要器从日志或文本里抽取更具体的异常信号。

## 自测

为什么脚本要在读取 `my_report_review.md` 前先调用 `path.exists()`？如果从别的目录运行 `python 011-python-project-status-summary\build_project_status.py`，`Path(__file__).parent` 为什么仍能帮助脚本找到输出目录？

完成后，请在本目录创建 `feedback.txt`，写下最难理解的一行 Python、实际遇到的报错，或希望下一节正则练习分析什么文本。下次练习会优先据此调整。
