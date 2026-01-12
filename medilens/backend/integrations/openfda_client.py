# backend/integrations/openfda_client.py

from typing import List
import requests

from core.config import Config
from core.models import RetrievedChunk


def _query_openfda(search_query: str) -> list:
    """
    Internal helper to query OpenFDA safely.
    """
    params = {
        "search": search_query,
        "limit": Config.TOP_K_RESULTS,
    }

    try:
        response = requests.get(
            Config.OPENFDA_BASE_URL,
            params=params,
            headers={
                "User-Agent": "MediLens/1.0 (academic-project)"
            },
            timeout=10,
        )
    except requests.RequestException:
        return []

    if response.status_code != 200:
        return []

    data = response.json()
    return data.get("results", [])


def fetch_openfda_drug_info(drug_name: str) -> List[RetrievedChunk]:
    """
    Fetch drug label information from OpenFDA.

    Strategy:
    1. Try generic_name search
    2. Fallback to brand_name search
    """

    results = _query_openfda(
        f'openfda.generic_name:"{drug_name}"'
    )

    
    if not results:
        results = _query_openfda(
            f'openfda.brand_name:"{drug_name}"'
        )

    chunks: List[RetrievedChunk] = []

    for item in results:
        text_parts = []

        if "description" in item:
            text_parts.extend(item["description"])

        if "indications_and_usage" in item:
            text_parts.extend(item["indications_and_usage"])

        if "warnings" in item:
            text_parts.extend(item["warnings"])

        if "adverse_reactions" in item:
            text_parts.extend(item["adverse_reactions"])

        if not text_parts:
            continue

        chunks.append(
            RetrievedChunk(
                text=" ".join(text_parts),
                source="openfda",
                reference=drug_name,
            )
        )

    return chunks