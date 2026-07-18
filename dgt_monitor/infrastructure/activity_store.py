"""In-memory and optional SQLite implementations of activity storage."""

from collections.abc import Mapping
import os
from pathlib import Path
import sqlite3
from threading import Lock
from typing import Any

_FIELDS = ("timestamp", "level", "source", "event_type", "user", "message")


class InMemoryActivityStore:
    """Thread-safe in-memory activity store."""

    def __init__(self):
        self._lock = Lock()
        self._entries: list[dict[str, str]] = []

    def record(self, entry: Mapping[str, Any]) -> None:
        normalized = {field: str(entry.get(field) or "") for field in _FIELDS}
        with self._lock:
            self._entries.append(normalized)

    def get_entries(self) -> list[dict[str, str]]:
        with self._lock:
            return [entry.copy() for entry in self._entries]

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()


class SqliteActivityStore:
    """SQLite-backed activity store with automatic schema migration."""

    def __init__(self, path: Path):
        if not path.is_absolute():
            raise ValueError("SQLite database path must be absolute")
        self._path = path
        self._lock = Lock()
        self._init_database()

    def _connect(self) -> sqlite3.Connection:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self._path)
        connection.row_factory = sqlite3.Row
        if connection.execute("PRAGMA user_version").fetchone()[0] < 1:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS activity (
                    timestamp TEXT NOT NULL,
                    level TEXT NOT NULL,
                    source TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    user TEXT NOT NULL,
                    message TEXT NOT NULL
                )
                """
            )
            connection.execute("PRAGMA user_version = 1")
            connection.commit()
        return connection

    def _init_database(self):
        conn = self._connect()
        conn.close()

    def record(self, entry: Mapping[str, Any]) -> None:
        normalized = {field: str(entry.get(field) or "") for field in _FIELDS}
        with self._lock:
            conn = self._connect()
            conn.execute(
                """
                INSERT INTO activity (timestamp, level, source, event_type, user, message)
                VALUES (:timestamp, :level, :source, :event_type, :user, :message)
                """,
                normalized
            )
            conn.commit()
            conn.close()

    def get_entries(self) -> list[dict[str, str]]:
        with self._lock:
            conn = self._connect()
            cursor = conn.execute("SELECT * FROM activity")
            entries = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return entries

    def clear(self) -> None:
        with self._lock:
            conn = self._connect()
            conn.execute("DELETE FROM activity")
            conn.commit()
            conn.close()


def build_activity_store() -> InMemoryActivityStore | SqliteActivityStore:
    """Build activity store based on ACTIVITY_DB_PATH environment variable."""
    db_path = os.getenv("ACTIVITY_DB_PATH")
    if db_path:
        return SqliteActivityStore(Path(db_path))
    return InMemoryActivityStore()
