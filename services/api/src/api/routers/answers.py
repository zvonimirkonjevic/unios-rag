"""Answer one question per request: `{"id", "question"}` in, `{"id", "answer"}` out."""
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from api.models.answers import Answer, Question
from core.agent import Agent
from utils.config import Config

router = APIRouter(tags=["Answers"])


@router.post(
    "/answers",
    response_model=Answer,
    summary="Answer a question",
    responses={status.HTTP_502_BAD_GATEWAY: {"description": "The agent run failed."}},
)
async def answer(body: Question):
    """Run the agent on the question and return its answer under the same id.

    Responds with 502 if the agent run fails.
    """
    agent = Agent(body.id, model_id=Config.model_id)
    try:
        response = await agent.ainvoke(body.question)
    except Exception:
        logger.exception(f"agent run failed: question_id={body.id}")
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "agent run failed")
    return Answer(id=body.id, answer=str(response["messages"][-1].text))
