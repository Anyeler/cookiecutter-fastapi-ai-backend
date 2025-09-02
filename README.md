# Cookiecutter：FastAPI + LangChain + OpenAI（+ MCP）后端模板

一个用于快速生成 AI 后端的 Cookiecutter 模板。基于 Python 3.12 的 FastAPI，内置：
- LangChain 与 OpenAI 接入（支持自定义 OpenAI 兼容 Endpoint）
- 流式输出（SSE）与可选 WebSocket 端点
- 可选 LangGraph Agent 工作流示例
- Docker、docker-compose + Nginx 反向代理（SSE + WebSocket）
- VS Code Devcontainer

快速使用
```bash
pipx install cookiecutter  # 或 pip install cookiecutter
cookiecutter gh:Anyeler/cookiecutter-fastapi-ai-backend
```

提供的开关
- use_poetry：是否使用 Poetry 管理依赖
- use_docker：是否包含 Dockerfile
- enable_websocket：是否生成 /ws/chat WebSocket 端点
- enable_langgraph：是否生成 LangGraph 示例与 /v1/agent 端点

生成项目的主要能力
- GET /healthz 健康检查
- POST /v1/chat 使用 LangChain ChatOpenAI 完成对话
- GET /v1/chat/stream 通过 OpenAI SDK 进行 SSE 流式输出
- 可选：WS /ws/chat WebSocket 分片返回 tokens
- 可选：POST /v1/agent 一个最小的 LangGraph 工作流

关于自定义 OpenAI 兼容 Endpoint（国产/私有模型）
- 在生成项目后，将 `.env.example` 复制为 `.env`
- 配置以下变量：
  - OPENAI_API_KEY=你的密钥
  - OPENAI_BASE_URL=你的 OpenAI 兼容推理服务地址（默认 https://api.openai.com/v1）
- 代码会自动读取以上环境变量，并在 LangChain 与 OpenAI SDK 中生效

通过 Docker + Nginx 访问的路径前缀
- Nginx 将对外暴露带有前缀的 API：/api/
  - 例如健康检查：GET http://127.0.0.1/api/healthz
  - 同步对话：POST http://127.0.0.1/api/v1/chat
  - 流式对话（SSE）：GET http://127.0.0.1/api/v1/chat/stream?prompt=hello
  - WebSocket：ws://127.0.0.1/api/ws/chat
- 反向代理中会将 /api/ 前缀回写到应用根路径，因此后端路由仍保持 /v1/... 与 /ws/... 结构

欢迎提交 Issue/PR，提出更多开关或语言本地化需求。

---