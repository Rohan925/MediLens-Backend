import re


def extract_drug_name(text: str) -> str:
    """
    Very simple heuristic-based drug name extraction.
    Can be improved later with NLP or APIs.
    """

    if not text:
        return "Unknown"

    # Split text into words
    words = re.findall(r"[A-Za-z]{3,}", text)

    if not words:
        return "Unknown"

    # Return the first reasonable-looking word
    return words[0].capitalize()
