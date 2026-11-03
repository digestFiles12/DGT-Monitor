# dgt_monitor/application/incidents.py
**ES:** Implementa la carga con caché, el filtrado y los recuentos por causa de incidentes; opcionalmente persiste los incidentes cargados.
**EN:** Implements cached loading, filtering, and cause-based incident counts; it can optionally persist loaded incidents.
## Dependencies / Dependencias
Usa modelos y puertos de `core`, comparación textual y `TtlCache` de infraestructura; la fachada de aplicación usa `IncidentService`.
## Contents / Contenido
### `IncidentService`
- **ES:** Servicio de aplicación para cargar y filtrar incidentes, calcular recuentos por causa y, opcionalmente, persistir resultados.
- **EN:** Application service for loading and filtering incidents, calculating cause-based counts, and optionally persisting results.
### `IncidentService.__init__(repository, cache, store=None)`
- **ES:** Guarda el repositorio, la caché y el almacén opcional.
- **EN:** Stores the repository, cache, and optional store.
### `IncidentService.get_all(refresh=False)`
- **ES:** Obtiene los incidentes mediante la caché; con refresco invalida `incidents`. La carga llama al repositorio y, si existe almacén, intenta guardar el resultado; un error de guardado se registra, pero no impide devolverlo.
- **EN:** Gets incidents through the cache; refresh invalidates `incidents`. Loading calls the repository and, if a store exists, attempts to save the result; save errors are logged without preventing the result from being returned.
### `load_incidents()` (función interna de `IncidentService.get_all`)
- **ES:** Carga los incidentes desde el repositorio y, si hay almacén, intenta persistirlos; captura y registra excepciones de guardado para conservar los datos cargados.
- **EN:** Loads incidents from the repository and, if a store is configured, attempts to persist them; catches and logs save exceptions so the loaded data is retained.
### `IncidentService.filter(incidents, filters)`
- **ES:** Devuelve solo incidentes que pasan todos los criterios según `_matches`.
- **EN:** Returns only incidents that pass every criterion according to `_matches`.
### `IncidentService.stats(incidents)`
- **ES:** Calcula total, accidentes, obras/mantenimiento, vehículos averiados o atascados, obstrucciones y eventos meteorológicos mediante búsquedas de palabras en `cause.casefold()`.
- **EN:** Counts total, accidents, roadworks/maintenance, stuck or broken-down vehicles, obstructions, and weather events using keyword checks in `cause.casefold()`.
### `IncidentService._matches(item, filters)`
- **ES:** Aplica coincidencias de texto a provincia, municipio y carretera; compara severidad sin distinguir mayúsculas y filtra causa (`kind`) y cobertura (`camera`). Un valor `kind` o `camera` desconocido no excluye el incidente.
- **EN:** Applies text matching to province, municipality, and road; compares severity case-insensitively and filters cause (`kind`) and coverage (`camera`). An unrecognized `kind` or `camera` value does not exclude the incident.
