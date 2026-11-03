# Modelos

Los modelos tipados del dominio están en `src/dgt_monitor/core/models.py`. Son dataclasses y constituyen el formato común que usan los servicios de aplicación y los adaptadores.

## `Incident`

Representa una incidencia normalizada desde una situación DATEX II. Agrupa identificadores y tiempos, severidad, tipo y causa, ubicación (carretera, municipio, provincia, comunidad y punto kilométrico), dirección, coordenadas y otros atributos de tráfico. También contiene los campos de cobertura de cámaras calculados por la aplicación: `has_camera_coverage`, `camera_coverage_count` y `nearest_camera_km_delta`.

El modelo incluye etiquetas para tipo, causa y dirección. Al crear la respuesta de incidencias, la fachada añade etiquetas localizadas para otros campos traducibles; esas etiquetas adicionales pertenecen al payload y no son campos declarados en la dataclass.

## `Camera`

Representa una cámara con identificador, carretera, provincia, punto kilométrico, URL de imagen y coordenadas. `distance_km` y `km_delta` guardan distancias calculadas al aplicar una búsqueda; no son datos necesarios para identificar una cámara en la fuente.

## Estadísticas y filtros

`IncidentStats` es un valor inmutable con seis contadores: total, accidentes, obras, vehículos averiados, obstrucciones y condiciones meteorológicas.

`IncidentFilters` transporta provincia, municipio, carretera, severidad, tipo, cobertura de cámara y modo de coincidencia. `CameraFilters` transporta provincia, carretera, punto kilométrico, coordenadas, límite, umbrales de distancia, cobertura de incidencias y modo de coincidencia. Ambos son dataclasses inmutables; los servicios aplican los criterios.

## Conversión a diccionario

`Incident.to_dict()`, `Camera.to_dict()` e `IncidentStats.to_dict()` usan `dataclasses.asdict()` para crear estructuras serializables sin acoplar los modelos a FastAPI o Pydantic.

Véase [Servicios](services.md) para el uso de estos modelos y [Arquitectura](architecture.md) para su posición en las capas.
