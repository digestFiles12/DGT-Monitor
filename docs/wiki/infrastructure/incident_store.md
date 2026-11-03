# dgt_monitor/infrastructure/incident_store.py
**ES:** Persiste incidencias en SQLite usando el identificador de situación como clave y actualiza registros existentes al volver a recibirlos. Guarda el contenido completo del modelo en JSON junto con campos consultables.
**EN:** Persists incidents in SQLite using the situation identifier as the key and updates existing records when received again. Stores the complete model as JSON alongside queryable fields.
## Dependencies / Dependencias
Usa módulos estándar de SQLite, JSON, fechas, rutas y sincronización; importa `Incident` del dominio. Bootstrap construye el almacén y `IncidentService` puede utilizarlo.
## Contents / Contenido
### `SaveResult`
- **ES:** Dataclass inmutable que comunica cantidades insertadas y actualizadas.
- **EN:** Immutable dataclass reporting inserted and updated counts.
### `SaveResult.inserted`, `SaveResult.updated`
- **ES:** Número de filas consideradas nuevas y número consideradas existentes/actualizadas en la operación.
- **EN:** Number of rows treated as new and number treated as existing/updated in the operation.
### `SqliteIncidentStore`
- **ES:** Almacén SQLite que mantiene una fila por `Incident.id`.
- **EN:** SQLite store maintaining one row per `Incident.id`.
### `SqliteIncidentStore.__init__(self, path: Path | str)`
- **ES:** Convierte la ruta a `Path`, crea un bloqueo e inicializa la tabla.
- **EN:** Converts the path to `Path`, creates a lock, and initializes the table.
### `SqliteIncidentStore._connect(self) -> sqlite3.Connection`
- **ES:** Crea el directorio padre, abre la base de datos y habilita acceso a filas por nombre.
- **EN:** Creates the parent directory, opens the database, and enables named-row access.
### `SqliteIncidentStore._init_database(self) -> None`
- **ES:** Crea la tabla `incidents` si no existe y cierra la conexión incluso si ocurre un error.
- **EN:** Creates the `incidents` table if absent and closes the connection even if an error occurs.
### `SqliteIncidentStore.save(self, incidents: Sequence[Incident]) -> SaveResult`
- **ES:** Descarta incidentes sin ID y devuelve ceros si no queda ninguno. Para los demás guarda una instantánea JSON y campos seleccionados, cuenta IDs nuevos frente a ya existentes (incluidos duplicados en el lote) y ejecuta un `UPSERT` transaccional; ante error revierte la transacción.
- **EN:** Discards incidents without IDs and returns zero counts if none remain. For the rest, stores a JSON snapshot and selected fields, counts new versus existing IDs (including duplicates within the batch), and performs a transactional `UPSERT`; on error it rolls back.
### `SqliteIncidentStore.load_all(self) -> list[Incident]`
- **ES:** Lee los payloads JSON, conserva solo las claves que siguen siendo campos de `Incident` y reconstruye los modelos; no fija orden de resultados.
- **EN:** Reads JSON payloads, keeps only keys that remain fields of `Incident`, and reconstructs the models; result ordering is unspecified.
### `SqliteIncidentStore.count(self) -> int`
- **ES:** Devuelve el número de filas de la tabla y cierra la conexión.
- **EN:** Returns the number of table rows and closes the connection.
### `build_incident_store() -> SqliteIncidentStore`
- **ES:** Construye el almacén con `INCIDENT_DB_PATH` o, si no está definida, con `data/incidents.db`.
- **EN:** Builds the store using `INCIDENT_DB_PATH` or `data/incidents.db` when the variable is unset.
