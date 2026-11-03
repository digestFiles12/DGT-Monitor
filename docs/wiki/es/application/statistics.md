# dgt_monitor/application/statistics.py
Calcula los seis indicadores de incidencias, agrupaciones geográficas/temporales, extremos por grupo y exportación JSON.
## Dependencias
Usa las reglas compartidas de [core.indicators](../core/indicators.md), `Incident` y la correspondencia provincia-región de `core`; `DgtApplicationService` y `menu.py` consumen estos cálculos. También usa la biblioteca estándar para fechas, JSON y rutas.
## Contenido
### `INDICATORS`, `WEEKDAYS`, `DEFAULT_GROUPED_JSON`
- Constantes con el orden de indicadores (`total`, `accidents`, `roadworks`, `breakdowns`, `obstructions`, `weather`), los siete días en inglés y el nombre de archivo predeterminado (`grouped_incidents.json`).
### `count_indicators(incidents)`
- Recorre un iterable y devuelve los seis contadores. `total` cuenta cada incidente; los otros cinco usan los predicados de `core.indicators.INDICATOR_RULES`.
### `weekday_of(incident)`
- Intenta obtener el día del inicio ISO; si falta o no es válido, prueba la fecha de creación. Devuelve el nombre inglés en minúsculas o `None` si no puede analizar ninguna.
### `_empty_leaf()`
- Crea un diccionario con los seis indicadores inicializados a cero.
### `_count(leaf, incident)`
- Incrementa `total` y suma el resultado de cada predicado compartido de `INDICATOR_RULES` a su indicador correspondiente.
### `_add_incident(groups, key, incident)`
- Crea la hoja del grupo si falta y actualiza sus seis indicadores mediante `_count`.
### `_sorted_groups(groups)`
- Devuelve un nuevo diccionario con las claves de grupo en orden alfabético.
### `group_incidents(incidents, generated_at=None)`
- Genera JSON agrupado por provincia, región, tipo y día, además de día+provincia y día+región. Los días sin fecha analizable se agrupan como `unknown` y esa sección se omite si queda vacía; los grupos geográficos desconocidos usan `UNKNOWN_REGION`.
### `find_extremes(groups)`
- Para cada indicador devuelve `{max, min}` con nombre y valor. Los empates se resuelven alfabéticamente; el mínimo ignora valores cero y es `None` si no hay grupo positivo.
### `build_statistics(incidents, level="province", generated_at=None)`
- Acepta únicamente `province` o `region`; agrupa y devuelve nivel, total, grupos y extremos. Un nivel inválido produce `ValueError`.
### `write_grouped_json(data, path)`
- Crea los directorios padre, escribe JSON UTF-8 con caracteres Unicode y sangría de dos espacios, y devuelve la ruta de salida.
## Ejemplo
Cada hoja de grupo contiene los seis indicadores; en este ejemplo no hubo eventos meteorológicos, por lo que su mínimo es nulo.
```json
{
  "by_province": {"Madrid": {"total": 2, "accidents": 1, "roadworks": 1, "breakdowns": 0, "obstructions": 0, "weather": 0}},
  "by_region": {"Comunidad de Madrid": {"total": 2, "accidents": 1, "roadworks": 1, "breakdowns": 0, "obstructions": 0, "weather": 0}},
  "by_weekday": {"monday": {"total": 2, "accidents": 1, "roadworks": 1, "breakdowns": 0, "obstructions": 0, "weather": 0}}
}
```
Las reglas de clasificación están en [core.indicators](../core/indicators.md). `total` cuenta todos los incidentes; cada otro indicador aplica su predicado a la causa. El máximo puede ser cero si los grupos existen y todos tienen cero para ese indicador; el mínimo ignora esos ceros y es `null` si no hay valores positivos.
