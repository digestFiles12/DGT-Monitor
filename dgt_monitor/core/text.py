"""Text and road-location normalization helpers."""

import re


class TextCleaner:
    _replacements = {
        "Ã¨": "è", "Ã©": "é", "Ã¡": "á", "Ã­": "í", "Ã³": "ó",
        "Ãº": "ú", "Ã±": "ñ", "Ã¼": "ü", "Ã ": "à",
    }

    def clean(self, value: str | None) -> str:
        text = value or ""
        for malformed, replacement in self._replacements.items():
            text = text.replace(malformed, replacement)
        return text


def matches_text(value: str | None, needle: str | None, mode: str = "contains") -> bool:
    if not needle:
        return True
    haystack = value or ""
    if mode == "exact":
        return haystack.casefold() == needle.casefold()
    if mode == "regex":
        try:
            return re.search(needle, haystack, re.IGNORECASE) is not None
        except re.error:
            return False
    return needle.casefold() in haystack.casefold()


def normalize_road(value: str | None) -> str:
    return re.sub(r"[^A-Z0-9]", "", (value or "").upper())


def parse_kilometer_point(value: str | None) -> float | None:
    if not value:
        return None
    text = str(value).strip().replace(",", ".")
    plus_match = re.search(r"(\d+(?:\.\d+)?)\s*\+\s*(\d+)", text)
    if plus_match:
        return float(plus_match.group(1)) + float(plus_match.group(2)) / 1000
    number_match = re.search(r"\d+(?:\.\d+)?", text)
    return float(number_match.group(0)) if number_match else None