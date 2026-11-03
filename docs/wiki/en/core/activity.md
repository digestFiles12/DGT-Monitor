# dgt_monitor/core/activity.py
Provides a simple global interface for recording and reading activity through a store configured by bootstrap. The interface tolerates the absence of a configured store.
## Dependencies
Imports `Mapping` and `Any` from the standard library. Bootstrap configures the store; the GUI and API can share it through dependency injection.
## Contents
### `_store`
- Global reference to the active store; starts as `None`.
### `set_store(store)`
- Replaces the active store with the supplied object; bootstrap uses it while composing dependencies.
### `record(entry: Mapping[str, Any]) -> None`
- Sends an entry to the store when one exists; otherwise it does nothing.
### `get_entries() -> list[dict[str, str]]`
- Returns the store's entries, or an empty list when no store is configured.
### `clear() -> None`
- Asks the store to remove its entries; does nothing when no store is configured.
