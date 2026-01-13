import re
import requests

OPENFDA_URL = "https://api.fda.gov/drug/label.json"

NON_DRUG_TERMS = {
    "tablet", "tablets", "capsule", "capsules",
    "mg", "ml", "syrup", "injection",
    "dose", "dosage", "oral",
    "medicine", "drug"
}

def extract_candidate_tokens(text: str) -> set[str]:
    """
    Extract possible drug-like tokens from OCR text
    """
    tokens = set()

    # Uppercase words (common on medicine strips)
    tokens.update(re.findall(r"\b[A-Z][A-Z0-9\-]{3,}\b", text))

    # Capitalized words
    tokens.update(re.findall(r"\b[A-Z][a-z]{3,}\b", text))

    return tokens


def extract_drug_names(text: str) -> list[str]:
    """
    LEVEL 3: Dynamic drug name extraction
    No predefined list
    OpenFDA is the source of truth
    """
    candidates = extract_candidate_tokens(text)
    validated_drugs = set()

    for token in candidates:
        params = {
            "search": f'openfda.generic_name:"{token.lower()}"',
            "limit": 1
        }

        try:
            response = requests.get(
                OPENFDA_URL,
                params=params,
                timeout=3
            )

            if response.status_code == 200:
                data = response.json()
                if "results" in data:
                    validated_drugs.add(token.lower())

        except requests.exceptions.RequestException:
            continue

    return list(validated_drugs)
