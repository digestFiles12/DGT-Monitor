"""Static map from Spanish provinces to autonomous communities (CCAA)."""

import logging
import re
import unicodedata

logger = logging.getLogger(__name__)

UNKNOWN_REGION = "Unknown"

# Bilingual names use "/" (as in the DGT feed); each side is also accepted on its own.
PROVINCE_TO_REGION: dict[str, str] = {
    "Almería": "Andalucía", "Cádiz": "Andalucía", "Córdoba": "Andalucía", "Granada": "Andalucía",
    "Huelva": "Andalucía", "Jaén": "Andalucía", "Málaga": "Andalucía", "Sevilla": "Andalucía",
    "Huesca": "Aragón", "Teruel": "Aragón", "Zaragoza": "Aragón",
    "Asturias": "Asturias",
    "Illes Balears": "Illes Balears",
    "Las Palmas": "Canarias", "Santa Cruz de Tenerife": "Canarias",
    "Cantabria": "Cantabria",
    "Ávila": "Castilla y León", "Burgos": "Castilla y León", "León": "Castilla y León",
    "Palencia": "Castilla y León", "Salamanca": "Castilla y León", "Segovia": "Castilla y León",
    "Soria": "Castilla y León", "Valladolid": "Castilla y León", "Zamora": "Castilla y León",
    "Albacete": "Castilla-La Mancha", "Ciudad Real": "Castilla-La Mancha", "Cuenca": "Castilla-La Mancha",
    "Guadalajara": "Castilla-La Mancha", "Toledo": "Castilla-La Mancha",
    "Barcelona": "Cataluña", "Girona": "Cataluña", "Lleida": "Cataluña", "Tarragona": "Cataluña",
    "Alacant/Alicante": "Comunitat Valenciana", "Castelló/Castellón": "Comunitat Valenciana",
    "València/Valencia": "Comunitat Valenciana",
    "Badajoz": "Extremadura", "Cáceres": "Extremadura",
    "A Coruña": "Galicia", "Lugo": "Galicia", "Ourense": "Galicia", "Pontevedra": "Galicia",
    "Madrid": "Comunidad de Madrid",
    "Murcia": "Región de Murcia",
    "Navarra": "Navarra",
    "Araba/Álava": "País Vasco", "Bizkaia": "País Vasco", "Gipuzkoa": "País Vasco",
    "La Rioja": "La Rioja",
    "Ceuta": "Ceuta",
    "Melilla": "Melilla",
}

# Other spellings found in feeds, mapped to a canonical province name.
EXTRA_ALIASES: dict[str, str] = {
    "Alicante": "Alacant/Alicante", "Valencia": "València/Valencia", "Castellón": "Castelló/Castellón",
    "Álava": "Araba/Álava", "Vizcaya": "Bizkaia", "Guipúzcoa": "Gipuzkoa", "La Coruña": "A Coruña",
    "Orense": "Ourense", "Gerona": "Girona", "Lérida": "Lleida", "Baleares": "Illes Balears",
    "Islas Baleares": "Illes Balears", "Balears": "Illes Balears", "Principado de Asturias": "Asturias",
}

_warned_names: set[str] = set()


def normalize_province_name(name: str) -> str:
    """Return a lookup key: lowercase, no accents, no punctuation, single spaces."""
    decomposed = unicodedata.normalize("NFKD", name.casefold())
    without_accents = "".join(char for char in decomposed if not unicodedata.combining(char))
    return re.sub(r"[\W_]+", " ", without_accents).strip()


def _build_lookup() -> dict[str, str]:
    lookup: dict[str, str] = {}
    for canonical in PROVINCE_TO_REGION:
        lookup[normalize_province_name(canonical)] = canonical
        for side in canonical.split("/"):
            lookup[normalize_province_name(side)] = canonical
    for alias, canonical in EXTRA_ALIASES.items():
        lookup[normalize_province_name(alias)] = canonical
    return lookup


_LOOKUP = _build_lookup()


def region_for_province(name: str) -> str:
    """Return the autonomous community of a province, or UNKNOWN_REGION if not recognised."""
    canonical = _LOOKUP.get(normalize_province_name(name or ""))
    if canonical:
        return PROVINCE_TO_REGION[canonical]
    if name and name.strip() and name not in _warned_names:
        _warned_names.add(name)
        logger.warning("Unknown province %r: cannot assign an autonomous community", name)
    return UNKNOWN_REGION
