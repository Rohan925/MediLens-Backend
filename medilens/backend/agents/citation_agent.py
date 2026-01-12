# backend/agents/citation_agent.py
from typing import Dict, Any, List
from core.models import RetrievedChunk


OPENFDA_BASE_URL = "https://api.fda.gov/drug/label.json"


def _build_citation(chunk: RetrievedChunk) -> Dict[str, str]:
    """
    Convert a RetrievedChunk into a citation entry.
    """

    if chunk.source == "openfda":
        return {
            "source": "OpenFDA",
            "label": chunk.reference,
            "url": f"{OPENFDA_BASE_URL}?search={chunk.reference}"
        }

    elif chunk.source == "local":
        return {
            "source": "Local Knowledge Base",
            "label": chunk.reference,
            "url": "local://drug_knowledge.json"
        }

    else:
        return {
            "source": "Unknown Source",
            "label": chunk.reference,
            "url": ""
        }


async def citation_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    CITATION AGENT

    - Builds citations from retrieved chunks
    - Appends citations to the verified answer
    """

    retrieved_chunks: List[RetrievedChunk] = state.get("retrieved_chunks", [])
    checked_answer: str = state.get("checked_answer", "")

    if not checked_answer:
        state["final_answer"] = "No verified information available."
        state["citations"] = []
        return state

    citations = []
    seen = set()

    for chunk in retrieved_chunks:
        if chunk.reference not in seen:
            citations.append(_build_citation(chunk))
            seen.add(chunk.reference)

    citation_text = "\n".join(
        f"[{i+1}] {c['source']} — {c['url']}"
        for i, c in enumerate(citations)
    )

    final_answer = (
        f"{checked_answer}\n\n"
        f"Sources:\n{citation_text}"
    )

    state["final_answer"] = final_answer
    state["citations"] = citations
    return state