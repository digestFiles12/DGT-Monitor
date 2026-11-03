"""Thread-safe in-memory TTL cache."""

from copy import deepcopy
from dataclasses import dataclass
from threading import RLock
from time import monotonic
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class _Entry(Generic[T]):
    value: T
    expires_at: float


class TtlCache(Generic[T]):
    def __init__(self, ttl_seconds: float, clock: Callable[[], float] = monotonic) -> None:
        self._ttl_seconds = ttl_seconds
        self._clock = clock
        self._entries: dict[str, _Entry[T]] = {}
        self._lock = RLock()

    def get_or_load(self, key: str, loader: Callable[[], T]) -> T:
        with self._lock:
            entry = self._entries.get(key)
            now = self._clock()
            if entry is None or entry.expires_at <= now:
                entry = _Entry(deepcopy(loader()), now + self._ttl_seconds)
                self._entries[key] = entry
            return deepcopy(entry.value)

    def invalidate(self, key: str) -> None:
        with self._lock:
            self._entries.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()