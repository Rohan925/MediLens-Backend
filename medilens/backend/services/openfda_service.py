import requests
from core.config import settings


def fetch_drug_info(drug_name: str):
    """
    Fetch drug information from OpenFDA API
    """
    if not drug_name:
        return None

    params = {
        "search": f'openfda.generic_name:"{drug_name}"',
        "limit": 1
    }

    try:
        response = requests.get(settings.OPENFDA_BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        if not results:
            return None

        label = results[0]

        return {
            "drug_name": drug_name,
            "purpose": label.get("purpose", []),
            "warnings": label.get("warnings", []),
            "usage": label.get("indications_and_usage", []),
            "side_effects": label.get("adverse_reactions", []),
        }

    except Exception as e:
        print("OpenFDA error:", e)
        return None
