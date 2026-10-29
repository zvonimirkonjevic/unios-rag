"""API gateway entrypoint; `app` is served by uvicorn."""
from fastapi import FastAPI

from api.routers import answers
from utils.config import Config
from utils.logger import setup_logging


def create_app() -> FastAPI:
    """Configure logging and build the FastAPI app.

    Returns:
        The configured application with all routes registered.
    """
    setup_logging(level=Config.log_level)

    app = FastAPI(
        title="UniOS RAG API",
        description=(
            "Agentic RAG answering one question per request. "
            "Built to run locally, single-user, with no authentication.\n\n"
            "`POST /answers` takes `{\"id\", \"question\"}` and returns "
            "`{\"id\", \"answer\"}` with the same id."
        ),
        version="1.0.0"
    )

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Report that the API process is up and serving requests."""
        return {"status": "healthy"}

    app.include_router(answers.router)

    return app

app = create_app()
