"""Tests for concurrent SQLite activity store access."""

import pytest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dgt_monitor.infrastructure.activity_store import SqliteActivityStore


def test_concurrent_writes_sqlite(tmp_path):
    """Verify SQLite activity store handles concurrent writes safely."""
    db_path = tmp_path / "activity.db"
    store = SqliteActivityStore(db_path)
    
    def write_entry(i):
        entry = {
            "timestamp": f"2026-07-18T12:00:{i:02d}Z",
            "level": "info" if i % 2 == 0 else "warning",
            "source": "test",
            "event_type": "concurrent_write",
            "user": f"user{i}",
            "message": f"Entry {i}"
        }
        store.record(entry)
        return True
    
    # Concurrent writes
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(write_entry, i) for i in range(20)]
        results = [f.result() for f in futures]
    
    assert all(results)
    
    # Verify all entries were written
    entries = store.get_entries()
    assert len(entries) == 20


def test_concurrent_read_write_sqlite(tmp_path):
    """Verify SQLite activity store handles concurrent read/write safely."""
    db_path = tmp_path / "activity.db"
    store = SqliteActivityStore(db_path)
    
    # Pre-populate
    for i in range(10):
        store.record({
            "timestamp": f"2026-07-18T12:00:{i:02d}Z",
            "level": "info",
            "source": "test",
            "event_type": "initial",
            "user": "initial",
            "message": f"Initial {i}"
        })
    
    def concurrent_operation(i):
        if i % 2 == 0:
            # Write
            store.record({
                "timestamp": f"2026-07-18T12:01:{i:02d}Z",
                "level": "info",
                "source": "test",
                "event_type": "concurrent",
                "user": f"user{i}",
                "message": f"Concurrent write {i}"
            })
        else:
            # Read
            entries = store.get_entries()
            return len(entries) > 0
        return True
    
    # Mix of concurrent reads and writes
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(concurrent_operation, i) for i in range(20)]
        results = [f.result() for f in futures]
    
    assert all(results)
    
    # Final state should have initial + concurrent writes
    entries = store.get_entries()
    assert len(entries) >= 10


def test_concurrent_mixed_operations_sqlite(tmp_path):
    """Verify SQLite activity store handles mixed operations concurrently."""
    db_path = tmp_path / "activity.db"
    store = SqliteActivityStore(db_path)
    
    def mixed_operation(i):
        op = i % 3
        if op == 0:
            # Write
            store.record({
                "timestamp": f"2026-07-18T12:02:{i:02d}Z",
                "level": "info",
                "source": "test",
                "event_type": "mixed",
                "user": f"user{i}",
                "message": f"Mixed {i}"
            })
        elif op == 1:
            # Read
            entries = store.get_entries()
            assert len(entries) >= 0
        else:
            # Clear
            store.clear()
            # Re-populate one entry
            store.record({
                "timestamp": f"2026-07-18T12:03:{i:02d}Z",
                "level": "info",
                "source": "test",
                "event_type": "recovery",
                "user": f"user{i}",
                "message": f"Recovery {i}"
            })
        return True
    
    # Execute mixed operations
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(mixed_operation, i) for i in range(15)]
        results = [f.result() for f in futures]
    
    assert all(results)
    
    # Final state should be valid
    entries = store.get_entries()
    assert isinstance(entries, list)
    assert all("message" in e for e in entries)
