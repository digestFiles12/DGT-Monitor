# dgt_monitor/core/activity.py
Ofrece una interfaz global sencilla para registrar y consultar actividad mediante un almacén configurado por bootstrap. La interfaz tolera que todavía no haya un almacén configurado.
## Dependencias
Importa `Mapping` y `Any` de la biblioteca estándar. Bootstrap configura el almacén; la GUI y la API pueden compartirlo mediante inyección de dependencias.
## Contenido
### `_store`
- Referencia global al almacén activo; empieza como `None`.
### `set_store(store)`
- Sustituye el almacén activo por el objeto recibido; bootstrap lo utiliza durante la composición de dependencias.
### `record(entry: Mapping[str, Any]) -> None`
- Envía una entrada al almacén si existe; si no está configurado, no hace nada.
### `get_entries() -> list[dict[str, str]]`
- Devuelve las entradas del almacén, o una lista vacía si no hay almacén.
### `clear() -> None`
- Pide al almacén que elimine sus entradas; no hace nada si no hay almacén.
