# dgt_monitor/infrastructure/incident_store.py
Persists incidents in SQLite using the situation identifier as the key and updates existing records when received again. Stores the complete model as JSON alongside queryable fields.
## Dependencies
Uses standard-library modules for SQLite, JSON, dates, paths, and synchronization; imports the domain `Incident`. Bootstrap builds the store, and `IncidentService` can use it.
## Contents
### `SaveResult`
- Immutable dataclass reporting inserted and updated counts.
### `SaveResult.inserted`, `SaveResult.updated`
- Number of rows treated as new and number treated as existing/updated in the operation.
### `SqliteIncidentStore`
- SQLite store maintaining one row per `Incident.id`.
### `SqliteIncidentStore.__init__(self, path: Path | str)`
- Converts the path to `Path`, creates a lock, and initializes the table.
### `SqliteIncidentStore._connect(self) -> sqlite3.Connection`
- Creates the parent directory, opens the database, and enables named-row access.
### `SqliteIncidentStore._init_database(self) -> None`
- Creates the `incidents` table if absent and closes the connection even if an error occurs.
### `SqliteIncidentStore.save(self, incidents: Sequence[Incident]) -> SaveResult`
- Discards incidents without IDs and returns zero counts if none remain. For the rest, stores a JSON snapshot and selected fields, counts new versus existing IDs (including duplicates within the batch), and performs a transactional `UPSERT`; on error it rolls back.
### `SqliteIncidentStore.load_all(self) -> list[Incident]`
- Reads JSON payloads, keeps only keys that remain fields of `Incident`, and reconstructs the models; result ordering is unspecified.
### `SqliteIncidentStore.count(self) -> int`
- Returns the number of table rows and closes the connection.
### `build_incident_store() -> SqliteIncidentStore`
- Builds the store using `INCIDENT_DB_PATH` or `data/incidents.db` when the variable is unset.
