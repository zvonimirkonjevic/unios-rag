"""Request and response schemas for the `/answers` endpoint."""
from pydantic import BaseModel, ConfigDict, Field


class Question(BaseModel):
    """Body of an answer request."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"id": "q1", "question": "What is the current price of AAPL stock?"}],
        },
    )

    id: str
    question: str = Field(min_length=1)


class Answer(BaseModel):
    """The agent's answer, carrying the id of the question it answers."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"id": "q1", "answer": "AAPL is currently trading at $412.37 USD."}],
        },
    )

    id: str
    answer: str
