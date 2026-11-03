# dgt_monitor/application/statistics.py
**ES:** Calcula indicadores de incidentes, agrupaciones geográficas/temporales, extremos por grupo y exportación JSON.
**EN:** Computes incident indicators, geographic/temporal groupings, per-group extremes, and JSON export.
## Dependencies / Dependencias
Usa `Incident` y la correspondencia provincia-región de `core`; `DgtApplicationService` y `menu.py` consumen sus cálculos. También usa biblioteca estándar para fechas, JSON y rutas.
## Contents / Contenido
### `INDICATORS`, `WEEKDAYS`, `DEFAULT_GROUPED_JSON`
- **ES:** Constantes con el orden/nombres de los cuatro indicadores, los siete días en inglés y el nombre de archivo JSON predeterminado (`grouped_incidents.json`).
- **EN:** Constants for the ordered four indicator names, the seven English weekday names, and the default JSON filename (`grouped_incidents.json`).
### `is_severe(incident)`
- **ES:** Devuelve `True` solo si la severidad, sin distinguir mayúsculas, es `highest`.
- **EN:** Returns `True` only when severity, case-insensitively, is `highest`.
### `is_roadworks(incident)`
- **ES:** Devuelve `True` si la causa contiene `roadworks` o `maintenance`, sin distinguir mayúsculas.
- **EN:** Returns `True` if the cause contains `roadworks` or `maintenance`, case-insensitively.
### `is_road_closure(incident)`
- **ES:** Devuelve `True` cuando `management_type` es exactamente `roadClosed` o `carriagewayClosures`.
- **EN:** Returns `True` when `management_type` is exactly `roadClosed` or `carriagewayClosures`.
### `count_indicators(incidents)`
- **ES:** Recorre un iterable y devuelve los cuatro contadores: todos los incidentes, los graves, obras y cierres de carretera; los tres últimos se incrementan según sus funciones predicado.
- **EN:** Iterates over an iterable and returns four counts: all incidents, severe incidents, roadworks, and road closures; the latter three use their predicate functions.
### `weekday_of(incident)`
- **ES:** Intenta obtener el día del inicio ISO; si falta o no es válido, prueba la fecha de creación. Devuelve el nombre inglés en minúsculas o `None` si no puede analizar ninguna.
- **EN:** Tries the ISO start time; if missing or invalid, tries the creation time. Returns a lowercase English weekday or `None` if neither can be parsed.
### `_empty_leaf()`
- **ES:** Crea un diccionario de indicadores inicializados a cero.
- **EN:** Creates an indicator dictionary initialized to zero.
### `_add_incident(groups, key, incident)`
- **ES:** Crea la hoja del grupo si falta y suma el incidente a total, grave, obras y cierre según las reglas de indicadores.
- **EN:** Creates the group leaf if absent and increments total, severe, roadworks, and closures according to the indicator rules.
### `_sorted_groups(groups)`
- **ES:** Devuelve un nuevo diccionario con las claves de grupo en orden alfabético.
- **EN:** Returns a new dictionary with group keys in alphabetical order.
### `group_incidents(incidents, generated_at=None)`
- **ES:** Genera el JSON agrupado por provincia, región, tipo y día, además de día+provincia y día+región. Los días sin fecha analizable se agrupan como `unknown` y esa sección se omite si queda vacía; los grupos geográficos desconocidos usan `UNKNOWN_REGION`.
- **EN:** Builds grouped JSON by province, region, type, and weekday, plus weekday+province and weekday+region. Unparseable dates go into `unknown`, which is omitted if empty; unknown geographic values use `UNKNOWN_REGION`.
### `find_extremes(groups)`
- **ES:** Para cada indicador devuelve `{max, min}` con nombre y valor. Los empates se resuelven alfabéticamente; el mínimo ignora valores cero y es `None` si no hay grupo positivo.
- **EN:** For each indicator returns `{max, min}` with name and value. Ties are alphabetical; the minimum ignores zero values and is `None` if no positive group exists.
### `build_statistics(incidents, level="province", generated_at=None)`
- **ES:** Acepta únicamente `province` o `region`; agrupa y devuelve nivel, total, grupos y extremos. Un nivel inválido produce `ValueError`.
- **EN:** Accepts only `province` or `region`; groups data and returns level, total, groups, and extremes. An invalid level raises `ValueError`.
### `write_grouped_json(data, path)`
- **ES:** Crea los directorios padre, escribe JSON UTF-8 con caracteres Unicode y sangría de dos espacios, y devuelve la ruta de salida.
- **EN:** Creates parent directories, writes UTF-8 JSON with Unicode preserved and two-space indentation, and returns the output path.
## Example / Ejemplo
Una hoja para cada grupo siempre contiene los cuatro indicadores; por ejemplo, los tres ejes geográficos/temporales pueden verse así:
```json
{
  "by_province": {"Madrid": {"total": 2, "severe": 1, "roadworks": 1, "road_closures": 0}},
  "by_region": {"Comunidad de Madrid": {"total": 2, "severe": 1, "roadworks": 1, "road_closures": 0}},
  "by_weekday": {"monday": {"total": 2, "severe": 1, "roadworks": 1, "road_closures": 0}}
}
```
Los indicadores se calculan así: `total` cuenta cada incidente; `severe` requiere severidad `highest`; `roadworks` busca `roadworks` o `maintenance` en la causa; `road_closures` requiere `management_type` exactamente `roadClosed` o `carriagewayClosures`. Para cada indicador, el máximo toma el mayor valor y el mínimo el menor valor positivo (los grupos con cero se ignoran); en ambos casos los empates se deciden por nombre alfabético.
