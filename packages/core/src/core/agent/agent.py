"""Deep agent wrapper that answers one question and tags its LangSmith trace."""

from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

from core.agent.prompt import SYSTEM_PROMPT
from core.agent.tools import TOOLS
from utils.config import Config


class Agent:
    """Runs a deepagents graph for one question with a given chat model.

    Every run carries `question_id` and `model_id` as run metadata, so a
    LangSmith trace can be matched back to the question it answered.

    Args:
        question_id: Caller-supplied id of the question.
        model_id: Chat model in "provider:model" form, e.g.
            "openai:gpt-5.6-luna". Must match a `Config.model_init_kwargs`
            key exactly for model-specific kwargs to apply.

    Attributes:
        question_id: Caller-supplied id of the question.
        model_id: Chat model in "provider:model" form.
        config: LangGraph run config passed to every invoke, holding the
            recursion limit and trace metadata.
    """

    def __init__(
        self,
        question_id: str,
        model_id: str,
    ):
        self.question_id = question_id
        self.model_id = model_id

        self.config = {
            "recursion_limit": 10,
            "metadata": {
                "question_id": self.question_id,
                "model_id": self.model_id,
            },
        }

    async def ainvoke(self, input_text: str):
        """Run the agent to completion on a single question.

        Args:
            input_text: The question text.

        Returns:
            The final graph state, including the full message history
            under "messages".
        """
        agent = self.create_agent()
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": input_text}]},
            config={**self.config, "run_name": "UniOS-Agent"},
        )
        return response

    def create_agent(self):
        """Build the deep agent graph for this question's model.

        The chat model gets any extra kwargs registered for `model_id` in
        `Config.model_init_kwargs`. There is no checkpointer, so every run
        starts from an empty history.

        Returns:
            The compiled deepagents graph.
        """
        kwargs = {
            "model": init_chat_model(
                self.model_id, **Config.model_init_kwargs.get(self.model_id, {})
            ),
            "tools": TOOLS,
            "system_prompt": SYSTEM_PROMPT,
        }

        return create_deep_agent(**kwargs)
