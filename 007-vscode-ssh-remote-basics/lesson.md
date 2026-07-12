# 007：VS Code / SSH——安全地连上一台远程开发机

预计用时：45～60 分钟。

## 先用大白话说清楚

SSH 是一条加密的远程命令通道：你在自己的电脑输入命令，远程机器执行，再把结果传回来。它不是“把远程电脑搬到本地”，而是你带着一把受保护的钥匙，在远程机器门口证明“我是被允许进来的人”。

最常见的三个东西：

- **私钥**：只留在自己电脑上的钥匙，绝不发送给别人，也不要提交到 Git；
- **公钥**：可以放到服务器上的锁芯信息；
- **SSH 配置 Host**：给一长串连接参数起一个短名字，例如 `dev-lab`。VS Code 的 Remote - SSH 会读取这份配置。

本课只检查和演练配置，不会改动你现有密钥，也不会连接未知服务器。

## 本次小任务

完成一个可以被 VS Code 和命令行共同使用的 SSH 连接配置草稿：

1. 确认电脑能找到 `ssh`、`ssh-keygen` 和 VS Code；
2. 用示例配置学习 `Host`、主机地址、用户名和私钥路径的含义；
3. 用 `ssh -G` 在**不联网**的情况下展开并检查配置；
4. 找到 VS Code Remote - SSH 的入口，并知道真正连接前要替换哪两项。

完成后，把你是否已有服务器、卡在哪个命令、或觉得哪一项抽象写进本目录的 `feedback.txt`。下次会据此调整数据处理课的难度。

## 跟着做

在本目录打开 PowerShell：

```powershell
cd "C:\Users\Aa133\Desktop\codex自动化\开发者练习\007-vscode-ssh-remote-basics"
Get-Command ssh, ssh-keygen, code
ssh -V
```

看到 `OpenSSH` 版本说明命令行工具已可用。`code` 能找到，说明可以从终端打开 VS Code。

### 1. 看懂示例配置

打开本目录的 `ssh_config_example`：

```powershell
code ssh_config_example
```

其中：

- `Host dev-lab` 是你以后输入的短名字；
- `HostName 203.0.113.10` 是教学用保留地址，不能真的连接；
- `User ubuntu` 是远程 Linux 用户名；
- `IdentityFile ~/.ssh/id_ed25519` 指向本机私钥；
- `IdentitiesOnly yes` 让 SSH 只使用指定钥匙，避免拿错。

真实服务器准备好后，只替换 `HostName` 和 `User`，并确认 `IdentityFile` 指向你自己的私钥。不要把私钥复制进项目，也不要把它贴到聊天、Issue 或仓库中。

### 2. 不联网检查配置

```powershell
ssh -G -F .\ssh_config_example dev-lab | Select-String '^(hostname|user|identityfile|port) '
```

`-G` 只让 SSH 展开最终会使用的配置，不会发起网络连接。你应看到示例地址、用户名、端口 `22` 和私钥路径。

### 3. 理解密钥是否存在（只看文件名）

```powershell
Get-ChildItem "$env:USERPROFILE\.ssh" -Force | Select-Object Name, Length, LastWriteTime
```

如果将来需要新建一把专用密钥，先确认目标平台的要求，再执行：

```powershell
ssh-keygen -t ed25519 -C "your-email@example.com"
```

这会生成私钥和 `.pub` 公钥。**本次不要因为练习而重复生成密钥**；已有可用密钥时，优先理解并使用它。

### 4. 在 VS Code 中准备连接

```powershell
code .
```

在 VS Code 按 `Ctrl+Shift+P`，选择 `Remote-SSH: Connect to Host...`。等你有自己的服务器信息后，可以选择 `Add New SSH Host...`，把下面格式写入 `%USERPROFILE%\.ssh\config`：

```sshconfig
Host my-server
    HostName your-server.example.com
    User your-linux-user
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

连接第一次会要求确认服务器指纹；只有当指纹来自可信来源时才接受。连接成功后，左下角会显示远程连接状态，此时打开的终端和文件夹才是在远程机器上。

## 真实开发里有什么用

许多开发环境不在你的笔记本上：云服务器、团队测试机、GPU 机器和跳板机都很常见。SSH 配置让命令行、Git、部署脚本和 VS Code 使用同一份连接定义；Remote - SSH 则让你直接编辑远程代码、运行终端和调试程序，而不用手动反复上传文件。把密钥与项目文件分开，是避免凭证泄露的基本习惯。

## 自测

如果 `ssh -G -F .\ssh_config_example dev-lab` 显示了正确的 `hostname` 和 `user`，这说明了什么？它还**不能**说明什么？请分别回答“配置解析”和“真实网络连接”两件事。
