"""SQLite-backed storage for DGT incidents."""

from collections.abc import Sequence
from dataclasses import dataclass, fields
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
from threading import Lock

from dgt_monitor.core.models import Incident


@dataclass(frozen=True, slots=True)
class SaveResult:
    inserted: int
    updated: int


class SqliteIncidentStore:
    """Store incidents by situation id, updating existing records on each poll."""

    def __init__(self, path: Path | str):
        self._path = Path(path)
        self._lock = Lock()
        self._init_database()

    def _connect(self) -> sqlite3.Connection:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self._path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_database(self) -> None:
        connection = self._connect()
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS incidents (
                    id TEXT PRIMARY KEY,
                    road TEXT,
                    province TEXT,
                    community TEXT,
                    type TEXT,
                    cause TEXT,
                    severity TEXT,
                    management_type TEXT,
                    start_time TEXT,
                    creation_time TEXT,
                    first_seen TEXT NOT NULL,
                    last_seen TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )
            connection.commit()
        finally:
            connection.close()

    def save(self, incidents: Sequence[Incident]) -> SaveResult:
        valid_incidents = [incident for incident in incidents if incident.id]
        if not valid_incidents:
            return SaveResult(inserted=0, updated=0)

        now = datetime.now(timezone.utc).isoformat()
        rows = [
            {
                "id": incident.id,
                "road": incident.road,
                "province": incident.province,
                "community": incident.community,
                "type": incident.type,
                "cause": incident.cause,
                "severity": incident.severity,
                "management_type": incident.management_type,
                "start_time": incident.start_time,
                "creation_time": incident.creation_time,
                "first_seen": now,
                "last_seen": now,
                "payload": json.dumps(incident.to_dict(), ensure_ascii=False),
            }
            for incident in valid_incidents
        ]
        sql = """
            INSERT INTO incidents (
                id, road, province, community, type, cause, severity,
                management_type, start_time, creation_time, first_seen, last_seen, payload
            ) VALUES (
                :id, :road, :province, :community, :type, :cause, :severity,
                :management_type, :start_time, :creation_time, :first_seen, :last_seen, :payload
            )
            ON CONFLICT(id) DO UPDATE SET
                road = excluded.road,
                province = excluded.province,
                community = excluded.community,
                type = excluded.type,
                cause = excluded.cause,
                severity = excluded.severity,
                management_type = excluded.management_type,
                start_time = excluded.start_time,
                creation_time = excluded.creation_time,
                last_seen = excluded.last_seen,
                payload = excluded.payload
        """

        with self._lock:
            connection = self._connect()
            try:
                connection.execute("BEGIN")
                known_ids: set[str] = set()
                inserted = 0
                updated = 0
                for row in rows:
                    exists = connection.execute(
                        "SELECT 1 FROM incidents WHERE id = ?", (row["id"],)
                    ).fetchone()
                    if exists or row["id"] in known_ids:
                        updated += 1
                    else:
                        inserted += 1
                    known_ids.add(row["id"])
                connection.executemany(sql, rows)
                connection.commit()
                return SaveResult(inserted=inserted, updated=updated)
            except Exception:
                connection.rollback()
                raise
            finally:
                connection.close()

    def load_all(self) -> list[Incident]:
        with self._lock:
            connection = self._connect()
            try:
                rows = connection.execute("SELECT payload FROM incidents").fetchall()
            finally:
                connection.close()
        incident_fields = {field.name for field in fields(Incident)}
        incidents = []
        for row in rows:
            payload = json.loads(row["payload"])
            values = {key: value for key, value in payload.items() if key in incident_fields}
            incidents.append(Incident(**values))
        return incidents

    def count(self) -> int:
        with self._lock:
            connection = self._connect()
            try:
                return connection.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
            finally:
                connection.close()


def build_incident_store() -> SqliteIncidentStore:
    """Build the SQLite incident store from INCIDENT_DB_PATH or its default."""
    return SqliteIncidentStore(os.getenv("INCIDENT_DB_PATH", "data/incidents.db"))
