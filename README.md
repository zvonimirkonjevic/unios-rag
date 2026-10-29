# unios-rag
Implementation of a scraper and agentic RAG using LangChain, FastAPI, Postgres and pgvector.

> Work in progress: the agent currently runs on dummy tools (`get_stock_price`, `get_weather`) that return random data. Scraping and pgvector retrieval are not wired in yet.

## Structure
A [uv workspace](https://docs.astral.sh/uv/concepts/projects/workspaces/) of small, independent packages:

| Path | Purpose |
| --- | --- |
| `packages/core` | Agent built on [deepagents](https://github.com/langchain-ai/deepagents), its system prompt and tools |
| `packages/utils` | Shared config (read from env vars) and logging |
| `services/api` | FastAPI service exposing the agent over HTTP |

## Getting started
Requires Docker and [uv](https://docs.astral.sh/uv/) (Python 3.14).

```bash
cp .env.example .env   # fill in Postgres, LangSmith and OpenAI values
make up                # build and start api + postgres
```

The API runs at http://localhost:8000 with interactive docs at http://localhost:8000/docs. Source directories are mounted into the container, so code changes hot reload.

Other commands:

```bash
make down    # stop containers, keep data
make clean   # stop containers, delete volumes and local images
```

## API
| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness check |
| `POST` | `/answers` | Answer one question, returns `502` if the agent run fails |

```bash
curl -X POST http://localhost:8000/answers \
  -H "Content-Type: application/json" \
  -d '{"id": "q1", "question": "What is the current price of AAPL stock?"}'
# {"id": "q1", "answer": "..."}
```

Every run is traced to LangSmith with `question_id` and `model_id` as metadata.

## Configuration
Set in `.env` (see `.env.example`):

| Variable | Default | Description |
| --- | --- | --- |
| `ENV` | `local` | Deployment environment, `local` derives the Postgres host automatically |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | | Database credentials |
| `POSTGRES_HOST`, `POSTGRES_PORT` | `5432` (port) | Required host outside `local` |
| `MODEL_ID` | `openai:gpt-5.6-luna` | Chat model in `provider:model` form |
| `LOG_LEVEL` | `INFO` | Minimum log level |
| `OPENAI_API_KEY` | | OpenAI key |
| `LANGSMITH_*`, `LANGCHAIN_API_KEY` | | LangSmith tracing |

## Development
```bash
uv sync
uv run ruff format .
uv run ruff check .
```
