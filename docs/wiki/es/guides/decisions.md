# Decisiones técnicas

Esta guía resume decisiones que se reflejan en la implementación actual. Para la estructura de componentes y sus recorridos, consulta [Arquitectura](architecture.md).

## Modelos tipados en el dominio

`Incident`, `Camera` y los filtros se representan con dataclasses en `core/models.py`. Los métodos `to_dict()` convierten los modelos en el borde de salida, evitando que el dominio dependa de la serialización de FastAPI.

## Adaptadores y composición

Los contratos de repositorio y almacén están definidos como protocolos en `core/ports.py`; HTTP, parsers, caché y SQLite se implementan en infraestructura. `bootstrap.build_application()` compone las dependencias de producción y `create_app(service=...)` admite una fachada inyectada. Las rutas llaman a los casos de uso a través de la fachada.

## Caché y almacenamiento

La caché TTL mantiene datos recientes en memoria y devuelve copias profundas para que los consumidores no muten el valor almacenado. Las incidencias también pueden guardarse en SQLite mediante `SqliteIncidentStore`: `id` es la clave de upsert, `first_seen` se conserva y `last_seen` se actualiza al recibir el registro otra vez. La ruta se controla con `INCIDENT_DB_PATH`; los errores al persistir se registran sin descartar la respuesta descargada.

## Normalización geográfica y cobertura

`core.regions` normaliza variantes de nombres de provincias para resolver comunidades autónomas, con `Unknown` como valor para entradas sin coincidencia. La cobertura de cámaras se calcula en la aplicación con carretera normalizada, provincia compatible y un umbral de 2 km, no se presupone que venga enlazada por DATEX II.

## Estadísticas compartidas

Los indicadores y las agrupaciones se calculan en `application.statistics` y se sirven mediante la API, el dashboard y el menú de consola. Así, las presentaciones reutilizan las mismas definiciones para provincia, comunidad autónoma, tipo y día de la semana.
