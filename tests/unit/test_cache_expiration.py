"""Tests for cache expiration and invalidation."""

from concurrent.futures import ThreadPoolExecutor

from dgt_monitor.infrastructure.cache import TtlCache


def test_cache_expires_entries():
    """Verify cache expires entries after TTL."""
    now = [0.0]
    cache = TtlCache[str](ttl_seconds=1, clock=lambda: now[0])

    assert cache.get_or_load("key1", lambda: "value1") == "value1"

    now[0] = 1.1
    assert cache.get_or_load("key1", lambda: "value2") == "value2"


def test_cache_loads_missing_key():
    """Verify cache loads a missing key."""
    cache = TtlCache[str](ttl_seconds=10)
    assert cache.get_or_load("missing", lambda: "loaded") == "loaded"


def test_cache_clear_removes_entries():
    """Verify cache clear removes all entries."""
    cache = TtlCache[str](ttl_seconds=10)

    cache.get_or_load("key1", lambda: "value1")
    cache.get_or_load("key2", lambda: "value2")
    cache.clear()

    assert cache.get_or_load("key1", lambda: "new1") == "new1"
    assert cache.get_or_load("key2", lambda: "new2") == "new2"


def test_cache_invalidate_key():
    """Verify cache invalidate removes specific key."""
    cache = TtlCache[str](ttl_seconds=10)

    cache.get_or_load("key1", lambda: "value1")
    cache.get_or_load("key2", lambda: "value2")
    cache.invalidate("key1")

    assert cache.get_or_load("key1", lambda: "new1") == "new1"
    assert cache.get_or_load("key2", lambda: "new2") == "value2"


def test_cache_concurrent_access():
    """Verify cache is thread-safe with concurrent access."""
    cache = TtlCache[str](ttl_seconds=10)

    def load_value(key, value):
        return cache.get_or_load(key, lambda: value)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(load_value, f"key{i}", f"value{i}") for i in range(20)]
        results = [f.result() for f in futures]

    assert results == [f"value{i}" for i in range(20)]


def test_cache_retains_multiple_keys():
    """Verify independent keys remain cached."""
    cache = TtlCache[str](ttl_seconds=10)

    for i in range(50):
        cache.get_or_load(f"key{i}", lambda i=i: f"value{i}")

    assert cache.get_or_load("key0", lambda: "unexpected") == "value0"
    assert cache.get_or_load("key49", lambda: "unexpected") == "value49"
