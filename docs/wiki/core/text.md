# dgt_monitor/core/text.py
**ES:** Reúne utilidades para corregir algunos errores de codificación, comparar texto, normalizar nombres de carretera y extraer puntos kilométricos. Son funciones auxiliares compartidas por parsers y servicios.
**EN:** Collects utilities for correcting selected encoding glitches, matching text, normalizing road names, and extracting kilometer points. These helpers are shared by parsers and services.
## Dependencies / Dependencias
Importa `re` de la biblioteca estándar. Los parsers usan `TextCleaner`; otros componentes pueden usar las funciones de comparación y normalización.
## Contents / Contenido
### `TextCleaner`
- **ES:** Limpiador de texto con una tabla interna de sustituciones de secuencias mal decodificadas.
- **EN:** Text cleaner with an internal replacement table for selected mis-decoded sequences.
### `TextCleaner._replacements`
- **ES:** Tabla privada de nueve secuencias defectuosas y sus caracteres acentuados previstos.
- **EN:** Private table of nine malformed sequences and their intended accented characters.
### `TextCleaner.clean(self, value: str | None) -> str`
- **ES:** Reemplaza secuencias conocidas; si recibe `None`, trabaja con una cadena vacía.
- **EN:** Replaces known sequences; if given `None`, operates on an empty string.
### `matches_text(value: str | None, needle: str | None, mode: str = "contains") -> bool`
- **ES:** Si no hay término de búsqueda devuelve `True`; `exact` compara sin distinguir mayúsculas, `regex` evalúa una expresión regular y devuelve `False` si es inválida, y otros modos buscan una subcadena sin distinguir mayúsculas.
- **EN:** Returns `True` when there is no search term; `exact` compares case-insensitively, `regex` evaluates a regular expression and returns `False` if invalid, and other modes perform a case-insensitive substring search.
### `normalize_road(value: str | None) -> str`
- **ES:** Convierte a mayúsculas y elimina todo carácter que no sea una letra ASCII o un dígito.
- **EN:** Converts to uppercase and removes every character that is not an ASCII letter or digit.
### `parse_kilometer_point(value: str | None) -> float | None`
- **ES:** Interpreta formatos numéricos con coma o punto decimal y formato `km+metros` (por ejemplo, suma los metros como milésimas); si no encuentra número devuelve `None`.
- **EN:** Parses numeric values with comma or dot decimals and `km+meters` notation (adding meters as thousandths); returns `None` when no number is found.
