# backend/services/context_builder.py

from typing import List

from core.models import RetrievedChunk
from core.config import Config


def build_context(chunks: List[RetrievedChunk]) -> str:
    """
    Build a formatted context string from retrieved chunks.

    Used by generator and fact-checker services.
    """

    if not chunks:
        return ""

    context_blocks = []

    for idx, chunk in enumerate(chunks, start=1):
        if not chunk.text:
            continue

        block = (
            f"[Source {idx} | {chunk.source}]\n"
            f"{chunk.text.strip()}"
        )
        context_blocks.append(block)

    full_context = "\n\n".join(context_blocks)

    return _trim_context(full_context)


def _trim_context(context: str) -> str:
    """
    Trim context to a safe maximum length.
    Prevents prompt overflow.
    """

    max_chars = Config.MAX_CONTEXT_CHARS

    if len(context) <= max_chars:
        return context

    return context[:max_chars] + "\n\n[Context truncated]"
