# dgt_monitor/application/statistics.py
Calcula indicadores de incidentes, agrupaciones geográficas/temporales, extremos por grupo y exportación JSON.
## Dependencias
Usa `Incident` y la correspondencia provincia-región de `core`; `DgtApplicationService` y `menu.py` consumen sus cálculos. También usa biblioteca estándar para fechas, JSON y rutas.
## Contenido
### `INDICATORS`, `WEEKDAYS`, `DEFAULT_GROUPED_JSON`
- Constantes con el orden/nombres de los cuatro indicadores, los siete días en inglés y el nombre de archivo JSON predeterminado (`grouped_incidents.json`).
### `is_severe(incident)`
- Devuelve `True` solo si la severidad, sin distinguir mayúsculas, es `highest`.
### `is_roadworks(incident)`
- Devuelve `True` si la causa contiene `roadworks` o `maintenance`, sin distinguir mayúsculas.
### `is_road_closure(incident)`
- Devuelve `True` cuando `management_type` es exactamente `roadClosed` o `carriagewayClosures`.
### `count_indicators(incidents)`
- Recorre un iterable y devuelve los cuatro contadores: todos los incidentes, los graves, obras y cierres de carretera; los tres últimos se incrementan según sus funciones predicado.
### `weekday_of(incident)`
- Intenta obtener el día del inicio ISO; si falta o no es válido, prueba la fecha de creación. Devuelve el nombre inglés en minúsculas o `None` si no puede analizar ninguna.
### `_empty_leaf()`
- Crea un diccionario de indicadores inicializados a cero.
### `_add_incident(groups, key, incident)`
- Crea la hoja del grupo si falta y suma el incidente a total, grave, obras y cierre según las reglas de indicadores.
### `_sorted_groups(groups)`
- Devuelve un nuevo diccionario con las claves de grupo en orden alfabético.
### `group_incidents(incidents, generated_at=None)`
- Genera el JSON agrupado por provincia, región, tipo y día, además de día+provincia y día+región. Los días sin fecha analizable se agrupan como `unknown` y esa sección se omite si queda vacía; los grupos geográficos desconocidos usan `UNKNOWN_REGION`.
### `find_extremes(groups)`
- Para cada indicador devuelve `{max, min}` con nombre y valor. Los empates se resuelven alfabéticamente; el mínimo ignora valores cero y es `None` si no hay grupo positivo.
### `build_statistics(incidents, level="province", generated_at=None)`
- Acepta únicamente `province` o `region`; agrupa y devuelve nivel, total, grupos y extremos. Un nivel inválido produce `ValueError`.
### `write_grouped_json(data, path)`
- Crea los directorios padre, escribe JSON UTF-8 con caracteres Unicode y sangría de dos espacios, y devuelve la ruta de salida.
## Ejemplo
Cada hoja de grupo contiene los cuatro indicadores; este ejemplo muestra hojas por provincia, región y día de semana.
```json
{
  "by_province": {"Madrid": {"total": 2, "severe": 1, "roadworks": 1, "road_closures": 0}},
  "by_region": {"Comunidad de Madrid": {"total": 2, "severe": 1, "roadworks": 1, "road_closures": 0}},
  "by_weekday": {"monday": {"total": 2, "severe": 1, "roadworks": 1, "road_closures": 0}}
}
```
Reglas de los indicadores: `total` cuenta cada incidente; `severe` requiere severidad `highest`; `roadworks` busca `roadworks` o `maintenance` en la causa; `road_closures` requiere `management_type` exactamente `roadClosed` o `carriagewayClosures`. El máximo es el valor mayor y el mínimo el menor valor positivo (los grupos con cero se ignoran); los empates se resuelven alfabéticamente.
