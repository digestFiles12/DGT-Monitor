# dgt_monitor/infrastructure/activity_store.py
**ES:** Implementa almacenes de actividad en memoria y en SQLite con una interfaz común. La fábrica elige SQLite cuando existe `ACTIVITY_DB_PATH`; en caso contrario crea un almacén en memoria.
**EN:** Implements in-memory and SQLite activity stores with a common interface. The factory selects SQLite when `ACTIVITY_DB_PATH` is set; otherwise it creates an in-memory store.
## Dependencies / Dependencias
Usa `sqlite3`, `threading`, `pathlib`, `os` y tipos de la biblioteca estándar; no importa módulos propios. Bootstrap y `core.activity` conectan el almacén con la aplicación.
## Contents / Contenido
### `_FIELDS`
- **ES:** Lista privada de los seis campos normalizados de cada entrada: `timestamp`, `level`, `source`, `event_type`, `user` y `message`.
- **EN:** Private list of the six normalized entry fields: `timestamp`, `level`, `source`, `event_type`, `user`, and `message`.
### `InMemoryActivityStore`
- **ES:** Almacén en memoria protegido por un `Lock` para coordinar accesos entre hilos.
- **EN:** In-memory store protected by a `Lock` to coordinate access across threads.
### `InMemoryActivityStore.__init__(self)`
- **ES:** Inicializa el bloqueo y la lista vacía de entradas.
- **EN:** Initializes the lock and empty entry list.
### `InMemoryActivityStore.record(self, entry: Mapping[str, Any]) -> None`
- **ES:** Convierte a texto los seis campos (valores ausentes se convierten en `""`) y añade la entrada bajo bloqueo.
- **EN:** Converts the six fields to strings (missing values become `""`) and appends the entry under the lock.
### `InMemoryActivityStore.get_entries(self) -> list[dict[str, str]]`
- **ES:** Devuelve, bajo bloqueo, una lista nueva con copias de las entradas.
- **EN:** Returns a new list containing copies of entries while holding the lock.
### `InMemoryActivityStore.clear(self) -> None`
- **ES:** Vacía la lista de entradas bajo bloqueo.
- **EN:** Empties the entry list under the lock.
### `SqliteActivityStore`
- **ES:** Almacén de actividad respaldado por SQLite con inicialización automática de esquema versión 1.
- **EN:** SQLite-backed activity store with automatic version-1 schema initialization.
### `SqliteActivityStore.__init__(self, path: Path)`
- **ES:** Requiere una ruta absoluta; si es relativa lanza `ValueError`. Guarda la ruta, crea el bloqueo e inicializa la base de datos.
- **EN:** Requires an absolute path; raises `ValueError` for a relative one. Stores the path, creates the lock, and initializes the database.
### `SqliteActivityStore._connect(self) -> sqlite3.Connection`
- **ES:** Crea el directorio padre si hace falta, abre SQLite y configura filas accesibles por nombre; si la versión es inferior a 1, crea la tabla y establece la versión.
- **EN:** Creates the parent directory if needed, opens SQLite, and enables named-row access; if the version is below 1, creates the table and sets the version.
### `SqliteActivityStore._init_database(self)`
- **ES:** Abre una conexión para asegurar la inicialización y la cierra inmediatamente.
- **EN:** Opens a connection to ensure initialization and closes it immediately.
### `SqliteActivityStore.record(self, entry: Mapping[str, Any]) -> None`
- **ES:** Normaliza los campos, inserta una fila y confirma la transacción bajo bloqueo.
- **EN:** Normalizes the fields, inserts a row, and commits the transaction under the lock.
### `SqliteActivityStore.get_entries(self) -> list[dict[str, str]]`
- **ES:** Consulta todas las filas y devuelve cada una como diccionario; la consulta no especifica orden explícito.
- **EN:** Queries all rows and returns each as a dictionary; the query does not specify an explicit order.
### `SqliteActivityStore.clear(self) -> None`
- **ES:** Elimina todas las filas y confirma la operación bajo bloqueo.
- **EN:** Deletes all rows and commits the operation under the lock.
### `build_activity_store() -> InMemoryActivityStore | SqliteActivityStore`
- **ES:** Lee `ACTIVITY_DB_PATH`; si está definido construye el almacén SQLite con esa ruta, y si no, el almacén en memoria.
- **EN:** Reads `ACTIVITY_DB_PATH`; when set it builds the SQLite store at that path, otherwise it builds the in-memory store.
