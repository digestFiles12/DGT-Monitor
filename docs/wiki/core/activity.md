# dgt_monitor/core/activity.py
**ES:** Ofrece una interfaz global sencilla para registrar y consultar actividad mediante un almacén configurado por bootstrap. La interfaz tolera que todavía no haya un almacén configurado.
**EN:** Provides a simple global interface for recording and reading activity through a store configured by bootstrap. The interface tolerates the absence of a configured store.
## Dependencies / Dependencias
Importa `Mapping` y `Any` de la biblioteca estándar. Bootstrap configura el almacén; la GUI y la API pueden compartirlo mediante inyección de dependencias.
## Contents / Contenido
### `_store`
- **ES:** Referencia global al almacén activo; empieza como `None`.
- **EN:** Global reference to the active store; starts as `None`.
### `set_store(store)`
- **ES:** Sustituye el almacén activo por el objeto recibido; bootstrap lo utiliza durante la composición de dependencias.
- **EN:** Replaces the active store with the supplied object; bootstrap uses it while composing dependencies.
### `record(entry: Mapping[str, Any]) -> None`
- **ES:** Envía una entrada al almacén si existe; si no está configurado, no hace nada.
- **EN:** Sends an entry to the store when one exists; otherwise it does nothing.
### `get_entries() -> list[dict[str, str]]`
- **ES:** Devuelve las entradas del almacén, o una lista vacía si no hay almacén.
- **EN:** Returns the store's entries, or an empty list when no store is configured.
### `clear() -> None`
- **ES:** Pide al almacén que elimine sus entradas; no hace nada si no hay almacén.
- **EN:** Asks the store to remove its entries; does nothing when no store is configured.
