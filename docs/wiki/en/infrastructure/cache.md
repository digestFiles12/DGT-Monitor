# dgt_monitor/infrastructure/cache.py
Implements a generic in-memory time-to-live cache with synchronized access and deep copies of values. The loader is called only when the key has no valid entry.
## Dependencies
Imports `deepcopy`, `dataclass`, `RLock`, `monotonic`, and generic typing tools. Bootstrap creates these caches for cameras and incidents.
## Contents
### `T`
- Generic type parameter for stored values.
### `_Entry[T]`
- Private dataclass grouping a cached value and its expiration time.
### `_Entry.value`, `_Entry.expires_at`
- Value of type `T` and expiration instant according to the configured clock.
### `TtlCache[T]`
- Cache with a per-instance TTL; uses an `RLock` to protect its dictionary.
### `TtlCache.__init__(self, ttl_seconds: float, clock: Callable[[], float] = monotonic) -> None`
- Stores the duration and clock (defaulting to `monotonic`), and creates the dictionary and lock.
### `TtlCache.get_or_load(self, key: str, loader: Callable[[], T]) -> T`
- Under lock, loads and stores a deep copy when there is no entry or it has expired; returns another deep copy. Expiration is current time plus TTL.
### `TtlCache.invalidate(self, key: str) -> None`
- Removes the key if present; it does not raise if absent.
### `TtlCache.clear(self) -> None`
- Removes all entries under the lock.
