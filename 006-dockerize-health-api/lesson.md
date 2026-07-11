# 006：Docker 基础——把健康检查 API 装进可搬运的盒子

预计用时：45～60 分钟。

## 先用大白话说清楚

Docker 可以理解为给程序准备一个“带说明书的运行盒子”。盒子里明确写了：用什么基础环境、把哪些文件放进去、启动时执行什么命令。别人拿到同一份盒子，在另一台电脑上也能用同样方式运行，不必猜“你的 Python 版本、依赖和启动命令是什么”。

两个词最重要：

- **镜像（image）**：做好的盒子模板。`docker build` 用 `Dockerfile` 造出它。
- **容器（container）**：从模板启动的一次实际运行。它会有名字、日志和生命周期；停掉后模板仍在。

`-p 8000:8000` 表示把电脑的 8000 端口接到容器内部的 8000 端口。左边是你访问的端口，右边是程序监听的端口。

## 本次小任务

把上一课的健康检查 API 打包成镜像并运行，然后用 `curl` 从宿主机验证：

1. `GET /health` 返回 `200` 和 JSON；
2. 未知路径返回 `404`；
3. 查看容器日志；
4. 停止并删除这次容器。

完成后，把遇到的命令、错误或感受写进同目录的 `feedback.txt`。下次练习会读取它。

## 跟着做

在本目录打开 PowerShell：

```powershell
cd "C:\Users\Aa133\Desktop\codex自动化\开发者练习\006-dockerize-health-api"
docker version
```

如果提示 Docker Desktop 没启动，先打开 Docker Desktop，等状态变为 Running 后再继续。

### 1. 看懂 Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY mock_api.py ./
EXPOSE 8000
CMD ["python", "mock_api.py"]
```

- `FROM`：选择一个带 Python 的轻量基础环境；
- `WORKDIR`：后面的命令在盒子里的 `/app` 执行；
- `COPY`：复制本课 API 文件；
- `EXPOSE`：声明程序使用 8000 端口；
- `CMD`：容器启动后要运行的命令。

### 2. 构建镜像

```powershell
docker build -t dev-practice-api:1.0 .
docker image ls dev-practice-api
```

最后的 `.` 表示“用当前目录作为构建材料”。Docker 会读取这里的 `Dockerfile`。

### 3. 启动容器

```powershell
docker run --name dev-practice-api -d -p 8000:8000 dev-practice-api:1.0
docker ps
```

`-d` 是让它在后台运行；容器名方便后面查看日志和停止。

### 4. 从你的电脑验证 API

```powershell
curl.exe -i http://127.0.0.1:8000/health
curl.exe -i http://127.0.0.1:8000/not-found
docker logs dev-practice-api
```

第一条应出现 `HTTP/1.0 200 OK`，第二条应出现 `404`。如果访问失败，先运行 `docker ps -a` 和 `docker logs dev-practice-api`，不要急着重建镜像。

### 5. 收尾

```powershell
docker stop dev-practice-api
docker rm dev-practice-api
docker ps -a
```

可选挑战：修改 `mock_api.py` 里的 `service` 值。你必须重新执行 `docker build`，因为镜像不会自动读取本地文件变化；再启动新容器验证结果。

## 真实开发里有什么用

Docker 让开发、测试和部署使用同一份运行说明。它常用于本地一键启动 API、数据库或任务脚本，也能降低“我电脑能跑、服务器不能跑”的概率。你后续的 `dev-workbench` 会用 Docker 把日志分析和 API 健康检查工具交付给别人运行。

## 自测

为什么改了 `mock_api.py` 后，只重启旧容器通常看不到改动？请分别说出应该更新的是“镜像”还是“容器”，以及要运行的关键命令。
