# dgt_monitor/infrastructure/incident_store.py
Persiste incidencias en SQLite usando el identificador de situación como clave y actualiza registros existentes al volver a recibirlos. Guarda el contenido completo del modelo en JSON junto con campos consultables.
## Dependencias
Usa módulos estándar de SQLite, JSON, fechas, rutas y sincronización; importa `Incident` del dominio. Bootstrap construye el almacén y `IncidentService` puede utilizarlo.
## Contenido
### `SaveResult`
- Dataclass inmutable que comunica cantidades insertadas y actualizadas.
### `SaveResult.inserted`, `SaveResult.updated`
- Número de filas consideradas nuevas y número consideradas existentes/actualizadas en la operación.
### `SqliteIncidentStore`
- Almacén SQLite que mantiene una fila por `Incident.id`.
### `SqliteIncidentStore.__init__(self, path: Path | str)`
- Convierte la ruta a `Path`, crea un bloqueo e inicializa la tabla.
### `SqliteIncidentStore._connect(self) -> sqlite3.Connection`
- Crea el directorio padre, abre la base de datos y habilita acceso a filas por nombre.
### `SqliteIncidentStore._init_database(self) -> None`
- Crea la tabla `incidents` si no existe y cierra la conexión incluso si ocurre un error.
### `SqliteIncidentStore.save(self, incidents: Sequence[Incident]) -> SaveResult`
- Descarta incidentes sin ID y devuelve ceros si no queda ninguno. Para los demás guarda una instantánea JSON y campos seleccionados, cuenta IDs nuevos frente a ya existentes (incluidos duplicados en el lote) y ejecuta un `UPSERT` transaccional; ante error revierte la transacción.
### `SqliteIncidentStore.load_all(self) -> list[Incident]`
- Lee los payloads JSON, conserva solo las claves que siguen siendo campos de `Incident` y reconstruye los modelos; no fija orden de resultados.
### `SqliteIncidentStore.count(self) -> int`
- Devuelve el número de filas de la tabla y cierra la conexión.
### `build_incident_store() -> SqliteIncidentStore`
- Construye el almacén con `INCIDENT_DB_PATH` o, si no está definida, con `data/incidents.db`.
