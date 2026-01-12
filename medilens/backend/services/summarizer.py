# backend/services/summarizer.py

from core.llm_client import llm_client


def summarize_text(text: str, max_words: int = 120) -> str:
    """
    Generate a concise summary of the provided text.

    Used by summariser_agent or UI-facing services.
    """

    if not text:
        return ""

    prompt = f"""
    Summarize the following medical information in under {max_words} words.
    Keep it clear, accurate, and easy to understand.

    TEXT:
    {text}
    """

    response = llm_client.generate(
        prompt=prompt,
        temperature=0.3
    )

    return response.strip()
