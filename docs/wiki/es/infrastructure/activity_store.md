# dgt_monitor/infrastructure/activity_store.py
Implementa almacenes de actividad en memoria y en SQLite con una interfaz común. La fábrica elige SQLite cuando existe `ACTIVITY_DB_PATH`; en caso contrario crea un almacén en memoria.
## Dependencias
Usa `sqlite3`, `threading`, `pathlib`, `os` y tipos de la biblioteca estándar; no importa módulos propios. Bootstrap y `core.activity` conectan el almacén con la aplicación.
## Contenido
### `_FIELDS`
- Lista privada de los seis campos normalizados de cada entrada: `timestamp`, `level`, `source`, `event_type`, `user` y `message`.
### `InMemoryActivityStore`
- Almacén en memoria protegido por un `Lock` para coordinar accesos entre hilos.
### `InMemoryActivityStore.__init__(self)`
- Inicializa el bloqueo y la lista vacía de entradas.
### `InMemoryActivityStore.record(self, entry: Mapping[str, Any]) -> None`
- Convierte a texto los seis campos (valores ausentes se convierten en `""`) y añade la entrada bajo bloqueo.
### `InMemoryActivityStore.get_entries(self) -> list[dict[str, str]]`
- Devuelve, bajo bloqueo, una lista nueva con copias de las entradas.
### `InMemoryActivityStore.clear(self) -> None`
- Vacía la lista de entradas bajo bloqueo.
### `SqliteActivityStore`
- Almacén de actividad respaldado por SQLite con inicialización automática de esquema versión 1.
### `SqliteActivityStore.__init__(self, path: Path)`
- Requiere una ruta absoluta; si es relativa lanza `ValueError`. Guarda la ruta, crea el bloqueo e inicializa la base de datos.
### `SqliteActivityStore._connect(self) -> sqlite3.Connection`
- Crea el directorio padre si hace falta, abre SQLite y configura filas accesibles por nombre; si la versión es inferior a 1, crea la tabla y establece la versión.
### `SqliteActivityStore._init_database(self)`
- Abre una conexión para asegurar la inicialización y la cierra inmediatamente.
### `SqliteActivityStore.record(self, entry: Mapping[str, Any]) -> None`
- Normaliza los campos, inserta una fila y confirma la transacción bajo bloqueo.
### `SqliteActivityStore.get_entries(self) -> list[dict[str, str]]`
- Consulta todas las filas y devuelve cada una como diccionario; la consulta no especifica orden explícito.
### `SqliteActivityStore.clear(self) -> None`
- Elimina todas las filas y confirma la operación bajo bloqueo.
### `build_activity_store() -> InMemoryActivityStore | SqliteActivityStore`
- Lee `ACTIVITY_DB_PATH`; si está definido construye el almacén SQLite con esa ruta, y si no, el almacén en memoria.
