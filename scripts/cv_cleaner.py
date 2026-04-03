import re


# words we want to REMOVE (common CV template noise)
NOISE_PATTERNS = [
    "modèles de cv",
    "créateur de cv",
    "lettre de motivation",
    "ressources en ligne",
    "copyright",
    "app.modeles-de-cv",
]


def remove_noise(text):
    for pattern in NOISE_PATTERNS:
        text = text.replace(pattern, "")
    return text


def clean_text(text):
    text = text.lower()

    # remove noise
    text = remove_noise(text)

    # remove special characters (keep letters/numbers/basic)
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()