# backend/tests/test_retriever.py

import pytest
from typing import List

from core.models import RetrievedChunk
from graph.state import GraphState
from agents.retriever_agent import retriever_agent


# -------------------------
# Mock integration functions
# -------------------------

def mock_openfda_fetch(drug_name: str) -> List[RetrievedChunk]:
    return [
        RetrievedChunk(
            text="Used to treat pain and fever.",
            source="openfda",
            reference=drug_name
        )
    ]


def mock_drugbank_fetch(drug_name: str) -> List[RetrievedChunk]:
    return [
        RetrievedChunk(
            text="Acts as an analgesic and antipyretic.",
            source="drugbank",
            reference=drug_name
        )
    ]


def mock_pubchem_fetch(drug_name: str) -> List[RetrievedChunk]:
    return [
        RetrievedChunk(
            text="Chemical compound commonly used in medicine.",
            source="pubchem",
            reference=drug_name
        )
    ]


# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def initial_state() -> GraphState:
    return {
        "query": "What is paracetamol?"
    }


# -------------------------
# Test
# -------------------------

@pytest.mark.asyncio
async def test_retriever_agent(monkeypatch, initial_state):
    """
    Test that retriever agent fetches data from integrations
    and stores RetrievedChunk objects in graph state.
    """

    # Patch integration calls inside retriever_agent
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

    updated_state = await retriever_agent(initial_state)

    assert "retrieved_chunks" in updated_state
    assert isinstance(updated_state["retrieved_chunks"], list)
    assert len(updated_state["retrieved_chunks"]) == 3

    for chunk in updated_state["retrieved_chunks"]:
        assert isinstance(chunk, RetrievedChunk)
        assert chunk.text
        assert chunk.source
