# 014：Docker 基础——用 Compose 复现一次 API 故障检查

预计用时：45～55 分钟。你会让 API 和检查脚本在两个容器中协作，并把检查报告保存回电脑。

## 先用大白话说清楚

上一轮你在本机启动 API，再用另一个命令检查它。Docker Compose 就像一张“小组开工单”：它把多个会一起工作的容器、它们的网络、启动顺序和输出位置写在同一个 `compose.yaml` 里。

这节有两个服务：`incident-api` 是被检查的 API；`checker` 是检查员。它们在 Compose 创建的内部网络里，检查员可以直接用服务名 `incident-api` 找到 API，不需要写死电脑 IP。`ports: "8014:8014"` 只是在你想从电脑浏览器或 `curl` 访问 API 时才需要。

还有一个容易误会的点：API 的健康检查返回 `200`，只说明进程活着；订单接口仍会返回 `503`。Docker 能稳定复现运行环境，但不能把业务故障自动变好。

## 本次小任务

1. 用 Compose 构建并启动故障演示 API。
2. 确认 API 容器通过 `/health` 健康检查。
3. 运行一次 `checker` 容器，让它检查健康接口和订单接口。
4. 在本机的 `output/api_check_report.md` 看见健康接口 `200`、订单接口 `503` 和“需要处理”。
5. 查看日志后清理本次容器。

完成标准：你能解释“`incident-api` 是怎样被 `checker` 找到的”，以及为什么健康检查通过但报告仍然有故障。

## 跟着做

在 PowerShell 打开本课目录：

```powershell
Set-Location "C:\Users\Aa133\Desktop\codex自动化\开发者练习\014-docker-compose-incident-check"
docker version
docker compose version
```

如果 `docker version` 提示连不上引擎，先启动 Docker Desktop，等它显示 **Running** 后再继续。`docker compose version` 只能证明命令已安装，不能证明 Docker 引擎已经启动。

### 1. 先检查配置（不启动容器）

```powershell
docker compose config
```

你应看到两个 services：`incident-api` 和 `checker`。先读 `compose.yaml`：`checker` 的 `API_BASE_URL` 写的是 `http://incident-api:8014`，这里的 `incident-api` 就是 Compose 网络内的服务名。

### 2. 启动 API 并确认容器状态

```powershell
docker compose up -d incident-api
docker compose ps
curl.exe -i http://127.0.0.1:8014/health
docker compose logs incident-api
```

`docker compose ps` 里的 Health 应变为 `healthy`；`curl` 应显示 `200`。如果不是，先运行 `docker compose logs incident-api`，不要急着删镜像重建。

### 3. 在第二个容器中运行检查员

```powershell
docker compose run --rm checker
Get-Content -Encoding UTF8 .\output\api_check_report.md
```

`--rm` 表示检查员结束后自动删除，避免留下很多一次性容器。报告应说明：健康检查正常，但订单服务是 `503`、需要处理。`./output:/app/output` 是一个挂载：容器写 `/app/output`，你的电脑同步得到 `output` 文件夹。

### 4. 看日志并收尾

```powershell
docker compose logs --tail 30
docker compose down
docker compose ps
```

`down` 会停止并移除这次 Compose 创建的容器和网络，不会删除本地代码、镜像或 `output` 里的报告。

## 命令小抄

| 命令或配置 | 它在做什么 |
| --- | --- |
| `docker compose config` | 展开并校验 Compose 配置。 |
| `docker compose up -d incident-api` | 在后台启动指定服务。 |
| `docker compose ps` | 看服务、容器和健康状态。 |
| `docker compose run --rm checker` | 临时运行检查员，并在结束后删除它。 |
| `API_BASE_URL: http://incident-api:8014` | 让容器通过服务名访问同一 Compose 网络的 API。 |
| `./output:/app/output` | 将容器产物保存回本机目录。 |
| `docker compose down` | 清理本次服务和网络。 |

## 真实开发里有什么用

真实项目常常不是一个程序：API、数据库、缓存、后台任务和一次性检查脚本都要协作。Compose 能让新人和 CI 用同一份配置启动一组本地依赖；挂载输出则让检查报告、测试结果和导出文件留在宿主机，方便审阅和提交。它把 `dev-workbench` 从“本机能运行的脚本”推进为“别人也能复现的工具组合”。

## 自测

为什么 `checker` 访问的是 `http://incident-api:8014`，而你在电脑上用的是 `http://127.0.0.1:8014`？请分别说明它们所在的网络，以及 `ports` 配置在其中的作用。

完成后，请在本目录创建 `feedback.txt`，写下一个最容易混淆的点、Docker Desktop 报错或你对 Compose 的疑问。下次练习会先读它；没有反馈时将按轮换进入 VS Code / SSH，并把这套工具作为远程环境中的可复现项目来使用。
