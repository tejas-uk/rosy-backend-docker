# Rosy AI - Async AI Chat Backend

A high-performance, async-first AI chat backend built with FastAPI, LangGraph, and PostgreSQL. Features persistent memory, multi-agent conversations, and scalable architecture.

## 🚀 Features

- **Async-First Architecture**: Built with async/await for optimal performance
- **Persistent Memory**: Long-term conversation memory using Mem0
- **Multi-Agent System**: Supervisor agent with research and memory capabilities
- **PostgreSQL Checkpointing**: Persistent conversation state with AsyncPostgresSaver
- **Authentication**: JWT-based user authentication
- **RESTful API**: Clean, documented API endpoints
- **Docker Support**: Containerized deployment
- **Real-time Chat**: WebSocket support for real-time conversations

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   LangGraph     │    │   PostgreSQL    │
│                 │    │   Agents        │    │   Checkpointer  │
│  - Auth Routes  │◄──►│  - Supervisor   │◄──►│  - Async        │
│  - Chat Routes  │    │  - Research     │    │  - Memory       │
│  - WebSocket    │    │  - Scalable     │    │  - Persistent   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mem0 Memory   │    │   Pinecone      │    │   Web Search    │
│                 │    │   Vector DB     │    │   Tools         │
│  - Async Client │    │  - Embeddings   │    │  - Tavily       │
│  - User Context │    │  - Semantic     │    │  - Real-time    │
│  - Persistent   │    │  - Search       │    │  - Data         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **AI Framework**: LangGraph, LangChain
- **Database**: PostgreSQL with AsyncPostgresSaver
- **Memory**: Mem0 for persistent conversation memory
- **Vector DB**: Pinecone for semantic search
- **Authentication**: JWT with bcrypt
- **Deployment**: Docker, Docker Compose
- **API Documentation**: Auto-generated with FastAPI

## 📋 Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- PostgreSQL database
- API keys for:
  - OpenAI/Anthropic (for LLMs)
  - Mem0 (for memory)
  - Pinecone (for vector search)
  - Tavily (for web search)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd rosy-backend-docker
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 3. Docker Deployment (Recommended)
```bash
# Build and start services
docker-compose up --build

# The API will be available at http://localhost:8000
```

### 4. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/rosy_ai

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Providers
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Memory and Search
MEM0_API_KEY=your-mem0-api-key
PINECONE_API_KEY=your-pinecone-api-key
TAVILY_API_KEY=your-tavily-api-key

# Checkpointer
CHECKPOINTER=postgres
```

### AI Configuration

Edit `src/ai/config.yaml` to configure your AI models:

```yaml
llm_models:
  research_agent:
    provider: "openai"
    model: "gpt-4o-mini"
    prompt_file: "research_agent.md"
  
  memory_agent:
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    prompt_file: "memory_node.md"
  
  supervisor:
    provider: "openai"
    model: "gpt-4o-mini"
    prompt_file: "supervisor.md"
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Authentication
- `POST /api/auth/passwordless` - Passwordless authentication
- `POST /api/auth/verify` - Verify authentication token

#### Chat Management
- `GET /api/chats/list_chats` - List user chats
- `POST /api/chats/create_chat` - Create new chat
- `GET /api/chats/{chat_id}/history` - Get chat history
- `POST /api/chats/{chat_id}/send_message` - Send message
- `DELETE /api/chats/{chat_id}` - Delete chat

#### Health & Status
- `GET /health` - Health check
- `GET /api/chats/health` - Chat service health

## 🧪 Testing

### Run Tests
```bash
# Unit tests
python -m pytest tests/

# API tests
python test_api_async.py

# Async checkpointer tests
python test_async_checkpointer.py
```

### Manual Testing
```bash
# Start the server
uvicorn src.main:app --reload

# Test CLI interface
python src/main.py
```

## 🏃‍♂️ Development

### Project Structure
```
rosy-backend-docker/
├── src/
│   ├── ai/                    # AI components
│   │   ├── agents.py         # Agent definitions
│   │   ├── checkpointer.py   # Async PostgreSQL checkpointer
│   │   ├── graph.py          # LangGraph workflow
│   │   ├── llms.py           # LLM configurations
│   │   ├── tools/            # AI tools
│   │   └── prompts/          # Agent prompts
│   ├── api/                  # API layer
│   │   ├── auth/             # Authentication
│   │   ├── chat/             # Chat endpoints
│   │   ├── db.py             # Database setup
│   │   └── models.py         # Data models
│   └── main.py               # FastAPI application
├── tests/                    # Test files
├── docs/                     # Documentation
├── docker-compose.yml        # Docker services
├── Dockerfile               # Container definition
└── requirements.txt         # Python dependencies
```

### Adding New Features

1. **New AI Tools**: Add to `src/ai/tools/`
2. **New Agents**: Update `src/ai/agents.py`
3. **New API Endpoints**: Add to `src/api/`
4. **Database Models**: Update `src/api/models.py`

### Code Style
- Follow PEP 8
- Use type hints
- Write async functions where appropriate
- Add docstrings for public functions

## 🚀 Deployment

### Production Deployment
```bash
# Build production image
docker build -t rosy-ai-backend .

# Run with production settings
docker run -p 8000:8000 --env-file .env rosy-ai-backend
```

### Environment-Specific Configs
- **Development**: Use `docker-compose.yml`
- **Staging**: Use `docker-compose.staging.yml`
- **Production**: Use `docker-compose.prod.yml`

## 📊 Monitoring

### Health Checks
- Application health: `GET /health`
- Database connectivity: `GET /api/chats/health`
- Memory service: Check Mem0 dashboard

### Logging
- Application logs: Docker logs
- Database logs: PostgreSQL logs
- Memory logs: Mem0 dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Guidelines
- Write tests for new features
- Update documentation
- Follow async patterns
- Use type hints
- Add error handling

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` directory
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions

## 🔄 Changelog

### v1.0.0 (Latest)
- ✅ Complete async migration
- ✅ AsyncPostgresSaver implementation
- ✅ Async memory tools
- ✅ Performance optimizations
- ✅ Comprehensive API documentation

### v0.9.0
- 🔧 Initial async implementation
- 🔧 LangGraph integration
- 🔧 Basic chat functionality

---

**Built with ❤️ using FastAPI, LangGraph, and modern async Python** 