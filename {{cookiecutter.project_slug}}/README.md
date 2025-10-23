# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

> 📖 **详细使用指南**: 如果你是中文用户或需要更详细的开发指南（包括 macOS + VSCode + Docker 配置），请查看 [USAGE_GUIDE.md](./USAGE_GUIDE.md)

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 🧠 **LangChain** - Framework for developing applications with LLMs
- 🤖 **OpenAI Integration** - GPT models via OpenAI API
- 📡 **Server-Sent Events (SSE)** - Real-time streaming responses
{% if cookiecutter.enable_websocket == "yes" -%}
- 🔌 **WebSocket Support** - Real-time bidirectional communication
{% endif -%}
{% if cookiecutter.enable_langgraph == "yes" -%}
- 🕸️ **LangGraph** - Build stateful, multi-actor applications with LLMs
{% endif -%}
- 🛠️ **MCP Ready** - Placeholder structure for Model Context Protocol integration
- 🐳 **Docker Support** - Containerized deployment with Nginx reverse proxy
- 🔧 **Development Container** - Ready-to-use VS Code dev environment
{% if cookiecutter.use_poetry == "yes" -%}
- 📦 **Poetry** - Modern Python dependency management
{% endif -%}

## Quick Start

### Local Development

1. **Clone and setup environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

{% if cookiecutter.use_poetry == "yes" -%}
2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Run the application:**
   ```bash
   poetry run uvicorn {{ cookiecutter.package_name }}.main:app --reload
   ```
{% else -%}
2. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run the application:**
   ```bash
   uvicorn {{ cookiecutter.package_name }}.main:app --reload
   ```
{% endif -%}

4. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/healthz

### Docker Compose (with Nginx)

1. **Setup environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

2. **Start services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the API:**
   - API: http://localhost
   - Health check: http://localhost/healthz

### Development Container

1. **Open in VS Code with Dev Containers extension**
2. **Command Palette → "Dev Containers: Reopen in Container"**
3. **The container will automatically install dependencies**

## API Endpoints

### Core Endpoints

- `GET /healthz` - Health check
- `POST /v1/chat` - Chat completion using LangChain
- `GET /v1/chat/stream?prompt=...` - Streaming chat via SSE

{% if cookiecutter.enable_websocket == "yes" -%}
### WebSocket Endpoints

- `WS /ws/chat` - Real-time chat via WebSocket

Example WebSocket usage:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');
ws.send(JSON.stringify({prompt: 'Hello, AI!'}));
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data.content);
};
```
{% endif -%}

{% if cookiecutter.enable_langgraph == "yes" -%}
### Agent Endpoints

- `POST /v1/agent` - Agent workflow using LangGraph

The agent endpoint uses a simple LangGraph workflow that processes messages through an LLM node.
{% endif -%}

### Example Usage

```python
import requests

# Chat completion
response = requests.post("http://localhost:8000/v1/chat", json={
    "messages": [
        {"role": "user", "content": "Hello, AI!"}
    ]
})
print(response.json())

# Streaming chat
import sseclient
response = requests.get(
    "http://localhost:8000/v1/chat/stream",
    params={"prompt": "Tell me a story"},
    stream=True
)
client = sseclient.SSEClient(response)
for event in client.events():
    if event.data != "[DONE]":
        print(event.data)
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - OpenAI model to use (default: {{ cookiecutter.openai_model }})
- `DEBUG` - Enable debug mode (default: true)
- `LOG_LEVEL` - Logging level (default: info)

### Cookiecutter Variables

This project was generated with the following options:

- **Project Name:** {{ cookiecutter.project_name }}
- **Project Slug:** {{ cookiecutter.project_slug }}
- **Package Name:** {{ cookiecutter.package_name }}
- **Python Version:** {{ cookiecutter.python_version }}
- **OpenAI Model:** {{ cookiecutter.openai_model }}
- **Author:** {{ cookiecutter.author_name }}
- **License:** {{ cookiecutter.license }}
- **Use Poetry:** {{ cookiecutter.use_poetry }}
- **Use Docker:** {{ cookiecutter.use_docker }}
- **Enable WebSocket:** {{ cookiecutter.enable_websocket }}
- **Enable LangGraph:** {{ cookiecutter.enable_langgraph }}

## MCP Integration

This project includes placeholder structure for [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) integration. MCP enables AI models to connect to external tools and data sources.

See `{{ cookiecutter.package_name }}/mcp/placeholder.py` for detailed implementation guidance.

## Development

### Code Quality

{% if cookiecutter.use_poetry == "yes" -%}
```bash
# Format code
poetry run ruff format .

# Lint code  
poetry run ruff check .

# Run tests
poetry run pytest
```
{% else -%}
```bash
# Format code
ruff format .

# Lint code
ruff check .

# Run tests
pytest
```
{% endif -%}

### Adding New Dependencies

{% if cookiecutter.use_poetry == "yes" -%}
```bash
# Production dependency
poetry add package-name

# Development dependency  
poetry add --group dev package-name
```
{% else -%}
```bash
# Edit pyproject.toml dependencies section
# Then reinstall
pip install -e ".[dev]"
```
{% endif -%}

## Deployment

### Docker

```bash
# Build image
docker build -t {{ cookiecutter.project_slug }} .

# Run container
docker run -p 8000:8000 --env-file .env {{ cookiecutter.project_slug }}
```

### Production Considerations

- Set `DEBUG=false` in production
- Use a proper ASGI server like Gunicorn with Uvicorn workers
- Configure proper logging and monitoring
- Set up SSL/TLS termination
- Use environment-specific configuration

## License

This project is licensed under the {{ cookiecutter.license }} License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Check the [documentation](http://localhost:8000/docs)
- Open an issue on the repository
- Contact: {{ cookiecutter.author_name }}