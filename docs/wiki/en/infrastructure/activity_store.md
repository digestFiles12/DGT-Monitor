# dgt_monitor/infrastructure/activity_store.py
Implements in-memory and SQLite activity stores with a common interface. The factory selects SQLite when `ACTIVITY_DB_PATH` is set; otherwise it creates an in-memory store.
## Dependencies
Uses `sqlite3`, `threading`, `pathlib`, `os`, and standard-library types; it imports no project modules. Bootstrap and `core.activity` connect the store to the application.
## Contents
### `_FIELDS`
- Private list of the six normalized entry fields: `timestamp`, `level`, `source`, `event_type`, `user`, and `message`.
### `InMemoryActivityStore`
- In-memory store protected by a `Lock` to coordinate access across threads.
### `InMemoryActivityStore.__init__(self)`
- Initializes the lock and empty entry list.
### `InMemoryActivityStore.record(self, entry: Mapping[str, Any]) -> None`
- Converts the six fields to strings (missing values become `""`) and appends the entry under the lock.
### `InMemoryActivityStore.get_entries(self) -> list[dict[str, str]]`
- Returns a new list containing copies of entries while holding the lock.
### `InMemoryActivityStore.clear(self) -> None`
- Empties the entry list under the lock.
### `SqliteActivityStore`
- SQLite-backed activity store with automatic version-1 schema initialization.
### `SqliteActivityStore.__init__(self, path: Path)`
- Requires an absolute path; raises `ValueError` for a relative one. Stores the path, creates the lock, and initializes the database.
### `SqliteActivityStore._connect(self) -> sqlite3.Connection`
- Creates the parent directory if needed, opens SQLite, and enables named-row access; if the version is below 1, creates the table and sets the version.
### `SqliteActivityStore._init_database(self)`
- Opens a connection to ensure initialization and closes it immediately.
### `SqliteActivityStore.record(self, entry: Mapping[str, Any]) -> None`
- Normalizes the fields, inserts a row, and commits the transaction under the lock.
### `SqliteActivityStore.get_entries(self) -> list[dict[str, str]]`
- Queries all rows and returns each as a dictionary; the query does not specify an explicit order.
### `SqliteActivityStore.clear(self) -> None`
- Deletes all rows and commits the operation under the lock.
### `build_activity_store() -> InMemoryActivityStore | SqliteActivityStore`
- Reads `ACTIVITY_DB_PATH`; when set it builds the SQLite store at that path, otherwise it builds the in-memory store.
