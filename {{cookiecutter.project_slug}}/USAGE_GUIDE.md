# {{ cookiecutter.project_name }} 使用指南

本指南详细介绍如何使用这个由 Cookiecutter 生成的 FastAPI + LangChain + OpenAI 后端项目。

## 目录

- [前置要求](#前置要求)
- [1. 生成项目](#1-生成项目)
- [2. 依赖管理](#2-依赖管理)
- [3. 本地开发与调试](#3-本地开发与调试)
- [4. Docker 环境](#4-docker-环境)
- [常见问题](#常见问题)

---

## 前置要求

### macOS 环境

- **操作系统**: macOS 10.15 或更高版本
- **Python**: 3.12+ (建议使用 pyenv 或 RVM 管理)
- **包管理器**: Homebrew
- **IDE**: VS Code (推荐安装 Python 扩展)

### 必需工具安装

```bash
# 安装 Homebrew（如果尚未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 使用 Homebrew 安装 Python（可选，如果已使用 RVM/pyenv 则跳过）
brew install python@3.12

# 安装 pipx（用于全局安装 Python CLI 工具）
brew install pipx
pipx ensurepath
```

---

## 1. 生成项目

### 1.1 安装 Cookiecutter

使用 pipx 安装 Cookiecutter（推荐方式）：

```bash
pipx install cookiecutter
```

或使用 pip 安装：

```bash
pip install --user cookiecutter
```

### 1.2 从模板生成项目

```bash
# 从 GitHub 仓库生成项目
cookiecutter gh:Anyeler/cookiecutter-fastapi-ai-backend
```

### 1.3 配置选项说明

运行上述命令后，会提示你输入以下配置信息：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `project_name` | 项目名称 | My AI Backend |
| `project_slug` | 项目文件夹名（自动生成） | my-ai-backend |
| `package_name` | Python 包名 | app |
| `description` | 项目描述 | FastAPI AI 后端服务 |
| `python_version` | Python 版本 | 3.12 |
| `openai_model` | OpenAI 模型 | gpt-4o-mini |
| `author_name` | 作者名称 | Your Name |
| `license` | 开源协议 | MIT / Apache-2.0 / Proprietary |
| `use_poetry` | 是否使用 Poetry | yes / no |
| `use_docker` | 是否包含 Docker 配置 | yes / no |
| `enable_websocket` | 是否启用 WebSocket | yes / no |
| `enable_langgraph` | 是否启用 LangGraph | yes / no |

**推荐配置**（适用于 macOS + VSCode 环境）：
- `use_poetry`: `no`（更简单，直接使用 pip）
- `use_docker`: `yes`（便于部署）
- `enable_websocket`: 根据需求选择
- `enable_langgraph`: 根据需求选择

### 1.4 生成后的项目结构

```
my-ai-backend/
├── .devcontainer/          # VS Code 开发容器配置
├── .env.example            # 环境变量模板
├── .gitignore
├── .vscode/                # VS Code 配置（需手动创建，见下文）
├── deploy/                 # 部署配置（Nginx 等）
├── docker-compose.yml      # Docker Compose 配置
├── Dockerfile              # Docker 镜像构建文件
├── pyproject.toml          # Python 项目配置
├── README.md               # 项目说明（英文）
├── USAGE_GUIDE.md          # 使用指南（本文件）
└── app/                    # 应用代码目录
    ├── __init__.py
    ├── main.py             # FastAPI 主入口
    ├── config.py           # 配置管理
    ├── routers/            # API 路由
    └── mcp/                # MCP 集成占位符
```

---

## 2. 依赖管理

### 2.1 初始化环境

进入生成的项目目录：

```bash
cd {{ cookiecutter.project_slug }}
```

### 2.2 配置环境变量

复制环境变量模板并编辑：

```bash
cp .env.example .env
```

编辑 `.env` 文件，添加你的 OpenAI API Key：

```bash
# 必需配置
OPENAI_API_KEY=sk-your-api-key-here

# 可选配置
OPENAI_BASE_URL=https://api.openai.com/v1  # 国产模型可修改为兼容端点
OPENAI_MODEL={{ cookiecutter.openai_model }}
DEBUG=true
LOG_LEVEL=info
```

{% if cookiecutter.use_poetry == "yes" -%}
### 2.3 使用 Poetry 管理依赖

#### 安装 Poetry

```bash
# 使用 pipx 安装（推荐）
pipx install poetry

# 或使用官方安装脚本
curl -sSL https://install.python-poetry.org | python3 -
```

#### 安装项目依赖

```bash
# 安装所有依赖（包括开发依赖）
poetry install

# 仅安装生产依赖
poetry install --only=main
```

#### 添加新依赖

```bash
# 添加生产依赖
poetry add package-name

# 添加开发依赖
poetry add --group dev package-name

# 添加指定版本
poetry add "package-name>=1.0.0,<2.0.0"
```

#### 更新依赖

```bash
# 更新所有依赖到最新兼容版本
poetry update

# 更新指定包
poetry update package-name

# 查看可更新的包
poetry show --outdated
```

#### 导出依赖列表

```bash
# 导出 requirements.txt（用于 Docker 等）
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

{% else -%}
### 2.3 使用 pip 管理依赖

#### 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
```

#### 安装项目依赖

```bash
# 以可编辑模式安装项目及开发依赖
pip install -e ".[dev]"

# 仅安装生产依赖
pip install -e .
```

#### 添加新依赖

编辑 `pyproject.toml` 文件：

```toml
[project]
dependencies = [
    "fastapi>=0.104.1",
    "your-new-package>=1.0.0",  # 添加新依赖
    # ... 其他依赖
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "your-dev-package>=1.0.0",  # 添加开发依赖
    # ... 其他开发依赖
]
```

然后重新安装：

```bash
pip install -e ".[dev]"
```

#### 更新依赖

```bash
# 更新所有包到最新版本
pip install --upgrade -e ".[dev]"

# 更新指定包
pip install --upgrade package-name

# 查看已安装的包
pip list

# 查看过期的包
pip list --outdated
```

#### 导出依赖列表

```bash
# 导出当前环境的所有包
pip freeze > requirements.txt

# 仅导出项目依赖（推荐）
pip install pip-tools
pip-compile pyproject.toml
```
{% endif -%}

### 2.4 验证安装

```bash
{% if cookiecutter.use_poetry == "yes" -%}
# 查看已安装的包
poetry show

# 验证 Python 环境
poetry run python --version
poetry run python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"
{% else -%}
# 查看已安装的包
pip list

# 验证 Python 环境
python --version
python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"
{% endif -%}
```

---

## 3. 本地开发与调试

### 3.1 启动开发服务器

{% if cookiecutter.use_poetry == "yes" -%}
```bash
# 使用 Poetry 运行
poetry run uvicorn {{ cookiecutter.package_name }}.main:app --reload

# 或指定端口
poetry run uvicorn {{ cookiecutter.package_name }}.main:app --reload --host 0.0.0.0 --port 8000
```
{% else -%}
```bash
# 确保虚拟环境已激活
source .venv/bin/activate

# 启动开发服务器
uvicorn {{ cookiecutter.package_name }}.main:app --reload

# 或指定端口
uvicorn {{ cookiecutter.package_name }}.main:app --reload --host 0.0.0.0 --port 8000
```
{% endif -%}

访问：
- **API 文档**: http://localhost:8000/docs
- **ReDoc 文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/healthz

### 3.2 VS Code 调试配置

#### 3.2.1 安装 VS Code 扩展

打开 VS Code，安装以下扩展：

1. **Python** (ms-python.python) - 必需
2. **Pylance** (ms-python.vscode-pylance) - 推荐
3. **Ruff** (charliermarsh.ruff) - 代码检查和格式化
4. **Docker** (ms-azuretools.vscode-docker) - Docker 支持

#### 3.2.2 创建调试配置

在项目根目录创建 `.vscode` 文件夹（如果不存在）：

```bash
mkdir -p .vscode
```

创建 `.vscode/launch.json` 文件，添加以下配置：

{% if cookiecutter.use_poetry == "yes" -%}
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "{{ cookiecutter.package_name }}.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000"
            ],
            "jinja": true,
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal"
        }
    ]
}
```
{% else -%}
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "{{ cookiecutter.package_name }}.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000"
            ],
            "jinja": true,
            "justMyCode": false,
            "python": "${workspaceFolder}/.venv/bin/python",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal"
        }
    ]
}
```
{% endif -%}

#### 3.2.3 设置断点和调试

1. **设置断点**：
   - 在 VS Code 中打开任意 Python 文件（如 `{{ cookiecutter.package_name }}/main.py`）
   - 点击行号左侧区域设置断点（红点）

2. **启动调试**：
   - 按 `F5` 或点击"运行和调试"面板中的"Python: FastAPI"
   - 服务器将在调试模式下启动

3. **调试操作**：
   - **F5**: 继续执行
   - **F10**: 单步跳过（Step Over）
   - **F11**: 单步进入（Step Into）
   - **Shift+F11**: 单步跳出（Step Out）
   - **F9**: 切换断点

4. **查看变量**：
   - 左侧"变量"面板显示当前作用域的所有变量
   - 悬停在代码上查看变量值
   - 在"监视"面板添加表达式

5. **调试控制台**：
   - 在"调试控制台"中输入 Python 表达式实时查看结果

#### 3.2.4 创建 VS Code 设置

创建 `.vscode/settings.json` 文件：

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "none",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        }
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".venv": false
    }
}
```

### 3.3 代码质量工具

#### 代码格式化

```bash
{% if cookiecutter.use_poetry == "yes" -%}
# 格式化代码
poetry run ruff format .

# 检查但不修改
poetry run ruff format --check .
{% else -%}
# 格式化代码
ruff format .

# 检查但不修改
ruff format --check .
{% endif -%}
```

#### 代码检查

```bash
{% if cookiecutter.use_poetry == "yes" -%}
# 运行 linter
poetry run ruff check .

# 自动修复可修复的问题
poetry run ruff check --fix .
{% else -%}
# 运行 linter
ruff check .

# 自动修复可修复的问题
ruff check --fix .
{% endif -%}
```

#### 运行测试

```bash
{% if cookiecutter.use_poetry == "yes" -%}
# 运行所有测试
poetry run pytest

# 运行特定测试文件
poetry run pytest tests/test_main.py

# 显示详细输出
poetry run pytest -v

# 显示代码覆盖率
poetry run pytest --cov={{ cookiecutter.package_name }}
{% else -%}
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_main.py

# 显示详细输出
pytest -v

# 显示代码覆盖率
pytest --cov={{ cookiecutter.package_name }}
{% endif -%}
```

### 3.4 使用开发容器（可选）

如果你安装了 Docker，可以使用 VS Code 的开发容器功能：

1. 安装 **Dev Containers** 扩展（ms-vscode-remote.remote-containers）
2. 按 `Cmd+Shift+P`，选择 "Dev Containers: Reopen in Container"
3. VS Code 将在 Docker 容器中打开项目，自动安装所有依赖

优势：
- 隔离的开发环境
- 无需在本地安装 Python 和依赖
- 团队成员环境一致

---

## 4. Docker 环境

### 4.1 安装 Docker（macOS）

#### 使用 Homebrew 安装 Docker Desktop

```bash
# 安装 Docker Desktop（社区版，免费）
brew install --cask docker

# 启动 Docker Desktop
open -a Docker
```

**注意**：首次启动 Docker Desktop 时，需要：
1. 同意用户协议
2. 允许系统权限（需要管理员密码）
3. 等待 Docker 引擎启动（状态栏会显示绿色图标）

#### 验证 Docker 安装

```bash
# 检查 Docker 版本
docker --version
docker-compose --version

# 运行测试容器
docker run hello-world
```

#### Docker Desktop 设置建议

打开 Docker Desktop 设置（齿轮图标）：

1. **Resources（资源）**：
   - CPU: 4 核（根据你的 Mac 配置调整）
   - Memory: 4-8 GB
   - Swap: 1 GB

2. **Docker Engine（引擎）**：
   - 保持默认配置

3. **Experimental Features（实验性功能）**：
   - 可选启用，不影响基本使用

### 4.2 构建 Docker 镜像

#### 单独构建应用镜像

```bash
# 构建镜像
docker build -t {{ cookiecutter.project_slug }}:latest .

# 查看构建的镜像
docker images | grep {{ cookiecutter.project_slug }}
```

#### 使用不同的标签

```bash
# 构建开发版本
docker build -t {{ cookiecutter.project_slug }}:dev .

# 构建生产版本（可以自定义 Dockerfile）
docker build -t {{ cookiecutter.project_slug }}:prod .

# 构建指定版本
docker build -t {{ cookiecutter.project_slug }}:v1.0.0 .
```

### 4.3 运行 Docker 容器

#### 单独运行应用容器

```bash
# 运行容器（前台）
docker run -p 8000:8000 --env-file .env {{ cookiecutter.project_slug }}:latest

# 运行容器（后台）
docker run -d -p 8000:8000 --env-file .env --name my-ai-backend {{ cookiecutter.project_slug }}:latest

# 查看运行中的容器
docker ps

# 查看容器日志
docker logs -f my-ai-backend

# 停止容器
docker stop my-ai-backend

# 删除容器
docker rm my-ai-backend
```

#### 挂载本地代码（开发模式）

```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/{{ cookiecutter.package_name }}:/app/{{ cookiecutter.package_name }} \
  --name my-ai-backend-dev \
  {{ cookiecutter.project_slug }}:latest
```

### 4.4 使用 Docker Compose

Docker Compose 可以同时管理多个服务（应用 + Nginx 反向代理）。

#### 启动所有服务

```bash
# 构建并启动（前台）
docker-compose up --build

# 后台启动
docker-compose up -d --build

# 仅启动（不重新构建）
docker-compose up -d
```

#### 查看服务状态

```bash
# 查看运行中的服务
docker-compose ps

# 查看服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f app
docker-compose logs -f nginx
```

#### 停止和清理

```bash
# 停止所有服务
docker-compose stop

# 停止并删除容器
docker-compose down

# 删除容器、网络和卷
docker-compose down -v

# 删除容器、网络、卷和镜像
docker-compose down -v --rmi all
```

#### 重启单个服务

```bash
# 重启应用服务
docker-compose restart app

# 重新构建并重启
docker-compose up -d --build app
```

### 4.5 访问 Docker Compose 服务

使用 Docker Compose 启动后，Nginx 会在 80 端口提供反向代理：

- **健康检查**: http://localhost/api/healthz
- **API 文档**: http://localhost/api/docs
- **同步对话**: POST http://localhost/api/v1/chat
- **流式对话**: GET http://localhost/api/v1/chat/stream?prompt=hello
{% if cookiecutter.enable_websocket == "yes" -%}
- **WebSocket**: ws://localhost/api/ws/chat
{% endif -%}

**注意**：Nginx 添加了 `/api` 前缀，但会在转发时移除，因此后端路由保持 `/v1/...` 结构。

### 4.6 Docker 镜像部署

#### 推送到 Docker Hub

```bash
# 登录 Docker Hub
docker login

# 标记镜像
docker tag {{ cookiecutter.project_slug }}:latest your-dockerhub-username/{{ cookiecutter.project_slug }}:latest

# 推送镜像
docker push your-dockerhub-username/{{ cookiecutter.project_slug }}:latest

# 在其他服务器上拉取
docker pull your-dockerhub-username/{{ cookiecutter.project_slug }}:latest
docker run -d -p 8000:8000 --env-file .env your-dockerhub-username/{{ cookiecutter.project_slug }}:latest
```

#### 保存和加载镜像

```bash
# 保存镜像为 tar 文件
docker save -o {{ cookiecutter.project_slug }}.tar {{ cookiecutter.project_slug }}:latest

# 在其他机器上加载镜像
docker load -i {{ cookiecutter.project_slug }}.tar
```

#### 优化镜像大小

1. **使用多阶段构建**（可编辑 Dockerfile）：

```dockerfile
# 构建阶段
FROM python:{{ cookiecutter.python_version }}-slim as builder
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --user -e .

# 运行阶段
FROM python:{{ cookiecutter.python_version }}-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "{{ cookiecutter.package_name }}.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **清理缓存和临时文件**：

```dockerfile
RUN pip install --no-cache-dir -e . \
    && rm -rf /tmp/* /var/tmp/*
```

### 4.7 Docker 最佳实践

1. **环境变量管理**：
   - 不要在镜像中硬编码敏感信息
   - 使用 `.env` 文件或容器编排工具（如 Kubernetes Secrets）
   - 生产环境使用 Docker Secrets 或外部配置管理

2. **健康检查**：
   在 `docker-compose.yml` 中添加健康检查：

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

3. **日志管理**：

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

4. **资源限制**：

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

---

## 常见问题

### Q1: 如何切换 OpenAI 兼容的国产模型？

编辑 `.env` 文件：

```bash
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://your-provider.com/v1  # 例如：https://api.deepseek.com/v1
OPENAI_MODEL=your-model-name  # 例如：deepseek-chat
```

### Q2: Poetry vs pip，应该选择哪个？

- **Poetry**: 
  - ✅ 更现代的依赖管理
  - ✅ 自动处理依赖冲突
  - ✅ 生成 lock 文件确保环境一致
  - ❌ 额外的学习成本

- **pip**: 
  - ✅ Python 内置，无需额外安装
  - ✅ 简单直接
  - ❌ 需要手动管理虚拟环境
  - ❌ 依赖管理较弱

**推荐**：新手使用 `pip`，团队项目使用 `Poetry`。

### Q3: VS Code 无法找到 Python 解释器？

1. 确保已激活虚拟环境：
   ```bash
   source .venv/bin/activate
   ```

2. 在 VS Code 中按 `Cmd+Shift+P`，选择 "Python: Select Interpreter"

3. 选择项目虚拟环境中的 Python：
   - `.venv/bin/python`（pip）
   {% if cookiecutter.use_poetry == "yes" -%}
   - 或 Poetry 环境路径（运行 `poetry env info --path` 查看）
   {% endif -%}

### Q4: Docker 容器启动失败？

1. **检查端口占用**：
   ```bash
   lsof -i :8000  # 检查 8000 端口
   lsof -i :80    # 检查 80 端口
   ```

2. **查看容器日志**：
   ```bash
   docker-compose logs app
   ```

3. **检查 .env 文件**：
   - 确保 `.env` 文件存在
   - 确保 `OPENAI_API_KEY` 已设置

4. **重新构建镜像**：
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up
   ```

### Q5: 如何在生产环境部署？

1. **设置生产环境变量**：
   ```bash
   DEBUG=false
   LOG_LEVEL=warning
   ```

2. **使用 Gunicorn + Uvicorn Workers**：
   修改 Dockerfile CMD：
   ```dockerfile
   CMD ["gunicorn", "{{ cookiecutter.package_name }}.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4"]
   ```

3. **添加健康检查和监控**：
   - 使用 Prometheus + Grafana
   - 配置日志聚合（如 ELK Stack）

4. **使用容器编排**：
   - Docker Swarm（简单）
   - Kubernetes（复杂但功能强大）

### Q6: 如何添加新的 API 端点？

1. 在 `{{ cookiecutter.package_name }}/routers/` 目录创建新路由文件
2. 在 `{{ cookiecutter.package_name }}/main.py` 中注册路由：

```python
from {{ cookiecutter.package_name }}.routers import your_new_router

app.include_router(your_new_router.router, prefix="/api/v1", tags=["your-tag"])
```

### Q7: 如何配置 CORS？

编辑 `{{ cookiecutter.package_name }}/main.py`，添加 CORS 中间件：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Q8: 调试时断点不生效？

1. 确保 `.vscode/launch.json` 中的 `justMyCode` 设置为 `false`
2. 确保使用正确的 Python 解释器
3. 重启调试会话（`Ctrl+Shift+F5`）

---

## 更多资源

- **FastAPI 官方文档**: https://fastapi.tiangolo.com/
- **LangChain 官方文档**: https://python.langchain.com/
- **Docker 官方文档**: https://docs.docker.com/
- **VS Code Python 调试**: https://code.visualstudio.com/docs/python/debugging
- **Poetry 官方文档**: https://python-poetry.org/docs/

---

## 贡献与反馈

如有问题或建议，请：
- 查看项目 README: [README.md](./README.md)
- 提交 Issue: https://github.com/Anyeler/cookiecutter-fastapi-ai-backend/issues
- 联系作者: {{ cookiecutter.author_name }}
