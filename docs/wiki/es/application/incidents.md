# dgt_monitor/application/incidents.py
Implementa la carga con caché, el filtrado y los recuentos por causa de incidentes; opcionalmente persiste los incidentes cargados.
## Dependencias
Usa modelos y puertos de `core`, las reglas compartidas de [core.indicators](../core/indicators.md), comparación textual y `TtlCache` de infraestructura; la fachada de aplicación usa `IncidentService`.
## Contenido
### `IncidentService`
- Servicio de aplicación para cargar y filtrar incidentes, calcular recuentos por causa y, opcionalmente, persistir resultados.
### `IncidentService.__init__(repository, cache, store=None)`
- Guarda el repositorio, la caché y el almacén opcional.
### `IncidentService.get_all(refresh=False)`
- Obtiene los incidentes mediante la caché; con refresco invalida `incidents`. La carga llama al repositorio y, si existe almacén, intenta guardar el resultado; un error de guardado se registra, pero no impide devolverlo.
### `load_incidents()` (función interna de `IncidentService.get_all`)
- Carga los incidentes desde el repositorio y, si hay almacén, intenta persistirlos; captura y registra excepciones de guardado para conservar los datos cargados.
### `IncidentService.filter(incidents, filters)`
- Devuelve solo incidentes que pasan todos los criterios según `_matches`.
### `IncidentService.stats(incidents)`
- Calcula total, accidentes, obras/mantenimiento, vehículos averiados o atascados, obstrucciones y eventos meteorológicos con los predicados compartidos de `core.indicators`; los recuentos se exponen como `total`, `accidents`, `roadworks`, `stuck`, `obstructions` y `weather`.
### `IncidentService._matches(item, filters)`
- Aplica coincidencias de texto a provincia, municipio y carretera; compara severidad sin distinguir mayúsculas y filtra causa (`kind`) mediante los mismos predicados de `core.indicators` y cobertura (`camera`). Un valor `kind` o `camera` desconocido no excluye el incidente.
