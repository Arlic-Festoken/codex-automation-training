# 015：VS Code / SSH——安全地远程打开 Compose 故障检查项目

预计用时：45～55 分钟。你会把 SSH 连接信息写成一个可读、可检查的别名，并让 VS Code Remote - SSH 准备好在远程机器上打开第 014 课的 Compose 项目。

## 先用大白话说清楚

SSH 像一条带门禁的加密通道：你在电脑上输入命令，真正执行命令的是远程服务器。VS Code Remote - SSH 则是在这条通道后面，把编辑器、终端和文件浏览器“搬到”远程机器上。

\`Host workbench-dev\` 不是服务器地址，而是你自己起的通讯录名字。它把主机地址、用户名、端口和私钥位置集中写进 \`~/.ssh/config\`。之后你只需记住 \`ssh workbench-dev\`，VS Code 也能选同一个名字。私钥相当于钥匙：只放在你的电脑，绝不复制进 Git、聊天记录或课程文件。

本课不需要真实服务器也能完成前半段：用 \`ssh -G\` 离线展开配置，确认 SSH 最终会用什么主机、用户和端口。只有在你拥有服务器地址、账号和授权私钥后，才做真实连接。

## 本次小任务

1. 读懂 SSH 配置模板中的四个位置：别名、地址、用户、私钥。
2. 用临时教学配置运行离线检查，确认 \`ssh -G\` 的展开结果。
3. 在自己拥有权限的服务器上，创建一个真实但不含密码的 \`Host workbench-dev\` 配置。
4. 用 VS Code Remote - SSH 打开远程的 \`014-docker-compose-incident-check\`，在远程终端运行 \`docker compose config\`。

完成标准：你能说清“别名”和“服务器地址”的区别，并能在不泄露私钥的前提下，让 VS Code 与命令行使用同一份 SSH 配置。

## 跟着做

先进入本课目录：

\`\`\`powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习\015-vscode-ssh-remote-compose-workbench"
Get-Content .\ssh_config_example
\`\`\`

模板里的 \`203.0.113.10\` 是专门用于文档示例的保留地址，不是真实服务器；不要尝试登录它。

### 1. 离线检查教学配置

\`\`\`powershell
.\verify_ssh_config.ps1
\`\`\`

脚本会把教学模板交给 \`ssh -G\` 解析，并断言 \`hostname\`、\`user\`、\`port\` 和 \`identityfile\`。它不会建立网络连接，也不会读取或创建你的真实私钥。

### 2. 准备你的真实 SSH 配置

仅当你已经有获授权的服务器和私钥时，在 PowerShell 中打开配置文件：

\`\`\`powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.ssh" | Out-Null
notepad "$env:USERPROFILE\.ssh\config"
\`\`\`

将下面的占位内容替换为**你自己的**服务器信息；不要把真实地址、用户名或私钥文件提交到这个训练仓库：

\`\`\`sshconfig
Host workbench-dev
  HostName your-server.example
  User your-login-name
  Port 22
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
\`\`\`

先只检查配置是否被正确读取：

\`\`\`powershell
ssh -G workbench-dev | Select-String '^(hostname|user|port|identityfile) '
\`\`\`

看到你的主机、用户、端口和私钥路径后，再在你确认有权限时连接：

\`\`\`powershell
ssh workbench-dev
\`\`\`

首次连接出现服务器指纹时，要通过你信任的运维渠道核对指纹；不确定就先取消。不要为了“连上”而跳过核验。

### 3. 在 VS Code 中打开远程项目

1. 在 VS Code 安装官方扩展 **Remote - SSH**。
2. 按 \`Ctrl+Shift+P\`，运行 \`Remote-SSH: Connect to Host...\`，选择 \`workbench-dev\`。
3. 连接成功后，选择 \`File > Open Folder\`，打开远程的 Compose 项目目录。
4. 在 VS Code 的远程终端运行：

\`\`\`bash
cd /path/to/014-docker-compose-incident-check
docker compose config
docker compose up -d incident-api
docker compose run --rm checker
docker compose down
\`\`\`

这些命令是在远程服务器执行的，所以 Docker Desktop 是否启动不再取决于你的 Windows 电脑；取决于远程服务器是否已安装 Docker、你的账号是否有 Docker 权限，以及项目文件是否已在远程目录中。

## 命令小抄

| 命令或配置 | 它在做什么 |
| --- | --- |
| \`ssh -G workbench-dev\` | 只展开配置，不发起 SSH 登录。 |
| \`Host workbench-dev\` | 给一台服务器起稳定别名。 |
| \`HostName ...\` | 真实服务器的域名或 IP。 |
| \`IdentityFile ~/.ssh/id_ed25519\` | 指向本机私钥；私钥不上传到仓库。 |
| \`IdentitiesOnly yes\` | 只尝试该 Host 指定的密钥，减少“试错式”认证。 |
| \`Remote-SSH: Connect to Host...\` | 让 VS Code 使用 SSH 配置创建远程窗口。 |
| \`docker compose config\` | 在远程环境先校验 Compose 文件，而不启动容器。 |

## 真实开发里有什么用

团队的测试机、云服务器或开发机通常不在你的桌面电脑上。一个清晰的 SSH 别名让终端、VS Code 和自动化脚本指向同一台受控机器，避免手输地址、用错账号或把私钥塞进项目。把第 014 课的 Compose 项目放到远程打开后，你能在更接近部署环境的 Linux 上复现 API 故障检查，同时保留本地编辑器的体验。这是 \`dev-workbench\` 从“自己电脑上的工具”走向“可在团队开发机使用”的一小步。

## 自测

为什么 \`ssh -G workbench-dev\` 可以在没有网络、没有真实服务器的情况下帮助排错？当 VS Code Remote - SSH 连不上时，你会先检查 \`HostName\`、\`User\`、私钥权限，还是直接把私钥复制进项目？为什么？

完成后，请在本目录创建 \`feedback.txt\`，写下一个最容易混淆的概念、实际连接报错或你对远程 Docker 的疑问。下次练习会优先读它；没有反馈时将按轮换进入数据处理，把远程或本地产生的检查结果整理成可比较的报表。
