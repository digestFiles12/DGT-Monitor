# dgt_monitor/core/regions.py
**ES:** Asocia nombres de provincias españolas con sus comunidades autónomas, tolerando acentos, variantes bilingües y alias encontrados en los datos. Los nombres no reconocidos producen una advertencia única y el valor `Unknown`.
**EN:** Maps Spanish province names to autonomous communities while tolerating accents, bilingual variants, and aliases found in the data. Unrecognized names produce a one-time warning and the value `Unknown`.
## Dependencies / Dependencias
Usa `logging`, `re` y `unicodedata` de la biblioteca estándar. `IncidentParser` usa `region_for_province` para completar la comunidad.
## Contents / Contenido
### `UNKNOWN_REGION`
- **ES:** Valor centinela (`"Unknown"`) para provincias no reconocidas.
- **EN:** Sentinel value (`"Unknown"`) for unrecognized provinces.
### `PROVINCE_TO_REGION`, `EXTRA_ALIASES`
- **ES:** Tablas estáticas: la primera asigna provincias canónicas a comunidades y la segunda asigna variantes ortográficas a una provincia canónica.
- **EN:** Static tables: the first maps canonical provinces to communities, and the second maps spelling variants to a canonical province.
### `_warned_names`
- **ES:** Conjunto privado que evita repetir advertencias para el mismo nombre desconocido.
- **EN:** Private set used to avoid repeating warnings for the same unknown name.
### `normalize_province_name(name: str) -> str`
- **ES:** Genera una clave de búsqueda en minúsculas, sin marcas de acento ni puntuación y con espacios normalizados.
- **EN:** Produces a lookup key in lowercase, without accent marks or punctuation, and with normalized spaces.
### `_build_lookup() -> dict[str, str]`
- **ES:** Construye el índice normalizado de provincias canónicas, lados individuales de nombres con `/` y alias.
- **EN:** Builds the normalized index for canonical provinces, individual sides of slash-separated names, and aliases.
### `_LOOKUP`
- **ES:** Índice privado creado al importar el módulo mediante `_build_lookup`.
- **EN:** Private index built at module import time by `_build_lookup`.
### `region_for_province(name: str) -> str`
- **ES:** Devuelve la comunidad de la provincia normalizada; devuelve `Unknown` si no existe coincidencia y registra una advertencia solo la primera vez por nombre desconocido no vacío.
- **EN:** Returns the community for the normalized province; returns `Unknown` when there is no match and warns only once per non-empty unknown name.
