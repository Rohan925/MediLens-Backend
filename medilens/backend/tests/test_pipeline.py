# backend/tests/test_pipeline.py

import pytest
from typing import List

from core.models import RetrievedChunk
from graph.graph_runner import run_graph
from graph.state import GraphState


# -------------------------
# MOCKS
# -------------------------

class MockLLMClient:
    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        return "Paracetamol is used to treat pain and fever."


def mock_openfda_fetch(drug_name: str) -> List[RetrievedChunk]:
    return [
        RetrievedChunk(
            text="Paracetamol treats pain and fever.",
            source="openfda",
            reference=drug_name
        )
    ]


def mock_drugbank_fetch(drug_name: str) -> List[RetrievedChunk]:
    return [
        RetrievedChunk(
            text="Analgesic and antipyretic drug.",
            source="drugbank",
            reference=drug_name
        )
    ]


def mock_pubchem_fetch(drug_name: str) -> List[RetrievedChunk]:
    return [
        RetrievedChunk(
            text="Widely used chemical compound in medicine.",
            source="pubchem",
            reference=drug_name
        )
    ]


# -------------------------
# TEST
# -------------------------

@pytest.mark.asyncio
async def test_full_pipeline(monkeypatch):
    """
    End-to-end test of the full agent graph pipeline.
    """

    # Patch LLM client
    monkeypatch.setattr(
        "agents.generator_agent.llm_client",
        MockLLMClient()
    )
    monkeypatch.setattr(
        "services.summarizer.llm_client",
        MockLLMClient()
    )

    # Patch integrations
    monkeypatch.setattr(
        "agents.retriever_agent.fetch_openfda_drug_info",
        mock_openfda_fetch
    )
    monkeypatch.setattr(
        "agents.retriever_agent.fetch_drugbank_drug_info",
        mock_drugbank_fetch
    )
    monkeypatch.setattr(
        "agents.retriever_agent.fetch_pubchem_compound_info",
        mock_pubchem_fetch
    )

    initial_state: GraphState = {
        "query": "What is paracetamol used for?"
    }

    final_state = await run_graph(initial_state)

    # -------------------------
    # ASSERTIONS
    # -------------------------

    assert "retrieved_chunks" in final_state
    assert len(final_state["retrieved_chunks"]) == 3

    assert "generated_answer" in final_state
    assert isinstance(final_state["generated_answer"], str)

    assert "checked_answer" in final_state
    assert isinstance(final_state["checked_answer"], str)

    assert "citations" in final_state
    assert isinstance(final_state["citations"], list)

    assert "final_answer" in final_state
    assert isinstance(final_state["final_answer"], str)
    assert final_state["final_answer"] != ""
