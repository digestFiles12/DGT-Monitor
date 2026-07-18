"""Activity logging convenience API.

This module provides a global interface to an activity store configured
and injected by bootstrap. In production, GUI and API receive the same
store instance by dependency injection.
"""

from collections.abc import Mapping
from typing import Any

_store: Any = None


def set_store(store) -> None:
    """Set the active activity store (called by bootstrap)."""
    global _store
    _store = store


def record(entry: Mapping[str, Any]) -> None:
    """Record one activity entry."""
    if _store:
        _store.record(entry)


def get_entries() -> list[dict[str, str]]:
    """Return all activity entries ordered by insertion."""
    if _store:
        return _store.get_entries()
    return []


def clear() -> None:
    """Clear all activity entries."""
    if _store:
        _store.clear()
