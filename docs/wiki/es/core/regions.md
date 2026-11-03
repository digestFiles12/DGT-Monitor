# dgt_monitor/core/regions.py
Asocia nombres de provincias españolas con sus comunidades autónomas, tolerando acentos, variantes bilingües y alias encontrados en los datos. Los nombres no reconocidos producen una advertencia única y el valor `Unknown`.
## Dependencias
Usa `logging`, `re` y `unicodedata` de la biblioteca estándar. `IncidentParser` usa `region_for_province` para completar la comunidad.
## Contenido
### `UNKNOWN_REGION`
- Valor centinela (`"Unknown"`) para provincias no reconocidas.
### `PROVINCE_TO_REGION`, `EXTRA_ALIASES`
- Tablas estáticas: la primera asigna provincias canónicas a comunidades y la segunda asigna variantes ortográficas a una provincia canónica.
### `_warned_names`
- Conjunto privado que evita repetir advertencias para el mismo nombre desconocido.
### `normalize_province_name(name: str) -> str`
- Genera una clave de búsqueda en minúsculas, sin marcas de acento ni puntuación y con espacios normalizados.
### `_build_lookup() -> dict[str, str]`
- Construye el índice normalizado de provincias canónicas, lados individuales de nombres con `/` y alias.
### `_LOOKUP`
- Índice privado creado al importar el módulo mediante `_build_lookup`.
### `region_for_province(name: str) -> str`
- Devuelve la comunidad de la provincia normalizada; devuelve `Unknown` si no existe coincidencia y registra una advertencia solo la primera vez por nombre desconocido no vacío.
