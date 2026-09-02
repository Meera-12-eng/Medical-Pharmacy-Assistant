import re


def normalize_field(value):
    """Normalize OpenFDA field values."""

    if value is None:
        return None

    if isinstance(value, list):
        values = [
            str(item).strip()
            for item in value
            if item is not None and str(item).strip()
        ]

        return "\\n".join(values) if values else None

    if isinstance(value, str):
        value = value.strip()
        return value if value else None

    return str(value).strip()


def clean_text(text):
    """Clean medical text."""

    if not text:
        return None

    text = str(text)

    # Remove line breaks and tabs
    text = re.sub(r"[\\r\\n\\t]+", " ", text)

    # Normalize whitespace
    text = re.sub(r"\\s+", " ", text)

    return text.strip()
