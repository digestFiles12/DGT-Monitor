# dgt_monitor/core/text.py
Reúne utilidades para corregir algunos errores de codificación, comparar texto, normalizar nombres de carretera y extraer puntos kilométricos. Son funciones auxiliares compartidas por parsers y servicios.
## Dependencias
Importa `re` de la biblioteca estándar. Los parsers usan `TextCleaner`; otros componentes pueden usar las funciones de comparación y normalización.
## Contenido
### `TextCleaner`
- Limpiador de texto con una tabla interna de sustituciones de secuencias mal decodificadas.
### `TextCleaner._replacements`
- Tabla privada de nueve secuencias defectuosas y sus caracteres acentuados previstos.
### `TextCleaner.clean(self, value: str | None) -> str`
- Reemplaza secuencias conocidas; si recibe `None`, trabaja con una cadena vacía.
### `matches_text(value: str | None, needle: str | None, mode: str = "contains") -> bool`
- Si no hay término de búsqueda devuelve `True`; `exact` compara sin distinguir mayúsculas, `regex` evalúa una expresión regular y devuelve `False` si es inválida, y otros modos buscan una subcadena sin distinguir mayúsculas.
### `normalize_road(value: str | None) -> str`
- Convierte a mayúsculas y elimina todo carácter que no sea una letra ASCII o un dígito.
### `parse_kilometer_point(value: str | None) -> float | None`
- Interpreta formatos numéricos con coma o punto decimal y formato `km+metros` (por ejemplo, suma los metros como milésimas); si no encuentra número devuelve `None`.
