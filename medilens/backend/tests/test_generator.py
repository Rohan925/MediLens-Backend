# backend/tests/test_generator.py

import pytest
from typing import List

from core.models import RetrievedChunk
from graph.state import GraphState
from agents.generator_agent import generator_agent


class MockLLMClient:
    """
    Mock LLM client to avoid real API calls during tests.
    """

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        return "This is a mocked generated answer."


@pytest.fixture
def mock_chunks() -> List[RetrievedChunk]:
    return [
        RetrievedChunk(
            text="Paracetamol is used to treat pain and fever.",
            source="openfda",
            reference="paracetamol"
        )
    ]


@pytest.fixture
def initial_state(mock_chunks) -> GraphState:
    return {
        "query": "What is paracetamol used for?",
        "retrieved_chunks": mock_chunks
    }


@pytest.mark.asyncio
async def test_generator_agent(monkeypatch, initial_state):
    """
    Test that generator agent produces an answer
    and stores it in graph state.
    """

    # Patch llm_client used inside generator_agent
    monkeypatch.setattr(
        "agents.generator_agent.llm_client",
        MockLLMClient()
    )

    updated_state = await generator_agent(initial_state)

    assert "generated_answer" in updated_state
    assert isinstance(updated_state["generated_answer"], str)
    assert updated_state["generated_answer"] != ""
