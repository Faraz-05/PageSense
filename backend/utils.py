import re


def clean_text(text: str) -> str:
    """
    Cleans webpage text before chunking.
    """

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Remove extra spaces
    text = re.sub(r"[ ]+", " ", text)

    # Remove leading spaces from every line
    text = re.sub(r"(?m)^\s+", "", text)

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text