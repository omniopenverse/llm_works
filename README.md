# 🧠 LLM Works: Multi-Service AI App Environment

This project provides a local containerized setup for working with LLMs (Large Language Models), embeddings, and notebooks using Docker Compose. It includes:

- 🦙 **Ollama**: Model serving for LLMs
- 📦 **App**: Main application interface
- 🌐 **OpenWebUI**: Web-based interface for interacting with LLMs
- 📓 **Jupyter**: Notebook environment for experiments

## 📁 Directory Structure

```
.
├── app/               # Source for main application
├── ollama/            # Ollama Dockerfile & setup
├── openwebui/         # OpenWebUI Dockerfile & setup
├── jupyter/           # Jupyter environment
├── docker-compose.yml
├── Makefile
└── README.md
```

## ⚙️ Prerequisites

- Docker
- Docker Compose v2
- GNU Make
- Set the required environment variable before running:
  ```bash
  export UNIVERSE_HOST=127.0.0.1  # Or your machine's IP
  ```

## 🚀 Getting Started

### 🏗️ Build and Run All Services

```bash
make service-all
```

This will:
- Build and start `ollama`, `app`, and `jupyter` services
- Pull required models inside the `ollama` container

### 🔧 Individual Services

```bash
make service-ollama     # Start Ollama and pull models
make service-app        # Start main app
make service-jupyter    # Start JupyterLab
```

## 📦 Model Management

### Pull LLM and Embedding Models

```bash
make pull-llama3.2      # Pulls llama3.2:1b model
make pull-embedings     # Pulls nomic-embed-text:v1.5 model
```

## 🌍 Available Endpoints

| Service     | URL                                |
|-------------|-------------------------------------|
| App         | http://${UNIVERSE_HOST}:8501         |
| Ollama API  | http://${UNIVERSE_HOST}:11434        |
| OpenWebUI   | http://${UNIVERSE_HOST}:8080         |
| Jupyter     | http://${UNIVERSE_HOST}:8888 (token: `token`) |

## 💾 Data Persistence

- Ollama models stored in Docker volume: `ollama_data`
- OpenWebUI data stored in volume: `dockerverse_openwebui_data`
- Jupyter notebooks bind-mounted from `jupyter/src`

## 🔌 Networking

All services are on the shared `common` Docker bridge network for internal communication.

## 🧹 Cleanup

```bash
docker compose down -v   # Stop containers and remove volumes
```

---

## 🛠️ Notes

- Make sure `UNIVERSE_HOST` is set properly, especially on non-Linux OS.
- Adjust ports in `docker-compose.yml` as needed for your local setup.
- Jupyter token is hardcoded as `token` for quick testing—change for production.

---

## 📜 License

MIT License. Use at your own discretion.
