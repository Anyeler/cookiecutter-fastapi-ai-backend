# Cookiecutter FastAPI AI Backend

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for creating production-ready FastAPI backends tailored for AI applications with LangChain, OpenAI, and optional MCP (Model Context Protocol) integration.

## Features

🚀 **FastAPI** - Modern, fast web framework with automatic API documentation  
🧠 **LangChain** - Framework for developing applications with language models  
🤖 **OpenAI Integration** - GPT models with streaming support  
📡 **Server-Sent Events (SSE)** - Real-time streaming responses  
🔌 **WebSocket Support** - Optional real-time bidirectional communication  
🕸️ **LangGraph** - Optional stateful, multi-actor LLM applications  
🛠️ **MCP Ready** - Placeholder structure for Model Context Protocol tools  
🐳 **Docker Support** - Complete containerization with Nginx reverse proxy  
🔧 **Dev Container** - Ready-to-use VS Code development environment  
📦 **Flexible Dependencies** - Choose between Poetry or pip/setuptools  

## Quick Start

### Prerequisites

- Python 3.8+
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter)

### Install Cookiecutter

```bash
pip install cookiecutter
```

### Generate Your Project

```bash
cookiecutter gh:Anyeler/cookiecutter-fastapi-ai-backend
```

You'll be prompted for the following options:

- **project_name** (default: "AI Backend Starter"): Display name for your project
- **project_slug** (auto-generated): Directory/package name (lowercase, hyphenated)
- **package_name** (default: "app"): Python package name
- **description** (default: "FastAPI + LangChain + OpenAI (+ MCP placeholder) backend on Python 3.12"): Project description
- **python_version** (default: "3.12"): Python version to use
- **openai_model** (default: "gpt-4o-mini"): Default OpenAI model
- **author_name**: Your name
- **license**: Choose from MIT, Apache-2.0, or Proprietary
- **use_poetry**: Use Poetry for dependency management (yes/no)
- **use_docker**: Include Docker configuration (yes/no)
- **enable_websocket**: Add WebSocket endpoint for real-time chat (yes/no)
- **enable_langgraph**: Include LangGraph for agent workflows (yes/no)

### Example Generation

```bash
$ cookiecutter gh:Anyeler/cookiecutter-fastapi-ai-backend

project_name [AI Backend Starter]: My AI Assistant
project_slug [my-ai-assistant]: 
package_name [app]: 
description [FastAPI + LangChain + OpenAI (+ MCP placeholder) backend on Python 3.12]: My custom AI assistant backend
python_version [3.12]: 
openai_model [gpt-4o-mini]: gpt-4
author_name: John Doe
license [MIT]: 
use_poetry [yes]: 
use_docker [yes]: 
enable_websocket [yes]: 
enable_langgraph [yes]:
```

## Generated Project Structure

```
my-ai-assistant/
├── .devcontainer/
│   ├── devcontainer.json          # VS Code dev container config
│   └── post-create.sh             # Setup script
├── app/                           # Main application package
│   ├── __init__.py
│   ├── main.py                    # FastAPI app with all endpoints
│   └── mcp/
│       ├── __init__.py
│       └── placeholder.py         # MCP integration guidelines
├── deploy/
│   └── nginx/
│       └── nginx.conf             # Nginx reverse proxy config
├── .dockerignore
├── .env.example                   # Environment variables template
├── .gitignore
├── docker-compose.yml             # Multi-service Docker setup
├── Dockerfile                     # Application container
├── pyproject.toml                 # Python project configuration
└── README.md                      # Project documentation
```

## What You Get

### Core API Endpoints

- `GET /healthz` - Health check endpoint
- `POST /v1/chat` - Chat completion using LangChain
- `GET /v1/chat/stream` - Streaming chat via Server-Sent Events

### Optional Features

**WebSocket Support** (if enabled):
- `WS /ws/chat` - Real-time chat via WebSocket

**LangGraph Agent** (if enabled):
- `POST /v1/agent` - Agent workflow endpoint

### Infrastructure

- **Docker Compose** - App + Nginx reverse proxy setup
- **Nginx Configuration** - Optimized for SSE and WebSocket
- **Development Container** - Complete VS Code dev environment
- **Environment Configuration** - Secure secret management

### Development Tools

- **Ruff** - Fast Python linter and formatter
- **Python 3.12** - Latest stable Python
- **Poetry or pip** - Flexible dependency management
- **pytest** - Testing framework (dev dependency)

## Getting Started After Generation

1. **Navigate to your project:**
   ```bash
   cd my-ai-assistant
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Choose your development approach:**

   **Option A: Local Development**
   ```bash
   # With Poetry (if selected)
   poetry install
   poetry run uvicorn app.main:app --reload
   
   # With pip (if Poetry not selected)
   pip install -e ".[dev]"
   uvicorn app.main:app --reload
   ```

   **Option B: Docker Compose**
   ```bash
   docker-compose up --build
   ```

   **Option C: Dev Container**
   - Open in VS Code
   - Command Palette → "Dev Containers: Reopen in Container"

4. **Access your API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/healthz

## Configuration Options

### Required Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key

### Optional Environment Variables

- `OPENAI_MODEL` - Model to use (default from cookiecutter)
- `DEBUG` - Enable debug mode (default: true)
- `LOG_LEVEL` - Logging level (default: info)

## MCP Integration

The generated project includes comprehensive guidance for integrating Model Context Protocol (MCP) tools. Check the `app/mcp/placeholder.py` file for:

- MCP client setup examples
- Tool integration patterns
- LangChain tool wrapping
- Agent integration approaches

## Customization

The template uses Jinja2 templating to conditionally include features based on your selections:

- **Poetry vs pip**: Different `pyproject.toml` configurations
- **Docker**: Containerization setup
- **WebSocket**: Real-time communication endpoints  
- **LangGraph**: Agent workflow capabilities

## Template Development

To contribute to this template:

1. Fork the repository
2. Make your changes
3. Test with different configuration combinations
4. Submit a pull request

### Testing the Template

```bash
# Test with different options
cookiecutter . --no-input
cookiecutter . --no-input use_poetry=no
cookiecutter . --no-input enable_websocket=no enable_langgraph=no
```

## License

This template is licensed under the MIT License. Generated projects will use the license you select during generation.

## Support

- 📖 **Documentation**: Check the generated project's README.md
- 🐛 **Issues**: Open an issue on this repository
- 💡 **Discussions**: Use GitHub Discussions for questions

## Related Projects

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework
- [LangChain](https://python.langchain.com/) - LLM application framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent workflow library
- [Model Context Protocol](https://modelcontextprotocol.io/) - AI tool integration standard
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) - Project templating tool