# backend/core/llm_client.py
from typing import Optional
from core.config import Config


class LLMClient:
    """
    LLM CLIENT

    Single interface for all LLM interactions.
    Agents must NEVER call an LLM provider directly.
    """

    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        self.model = Config.LLM_MODEL
        self.temperature = Config.LLM_TEMPERATURE

    async def generate(self, prompt: str) -> str:
        """
        Generate text from the LLM.
        Used by Generator Agent.
        """

        if self.provider == "dummy":
            return (
                "This is a dummy LLM response.\n\n"
                "Prompt received:\n"
                f"{prompt[:500]}"
            )

        raise NotImplementedError(
            "Real LLM provider not configured yet."
        )

    async def summarize(self, text: str, mode: str = "patient_friendly") -> str:
        """
        Summarize trusted text.
        Used by Summariser Agent.
        """

        if self.provider == "dummy":
            return text[:400] + "..."

        raise NotImplementedError(
            "Real LLM provider not configured yet."
        )



llm_client = LLMClient()