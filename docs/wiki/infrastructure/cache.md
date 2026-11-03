# dgt_monitor/infrastructure/cache.py
**ES:** Implementa una caché genérica en memoria con tiempo de vida, acceso sincronizado y copias profundas de valores. El cargador solo se invoca cuando la clave no tiene una entrada válida.
**EN:** Implements a generic in-memory time-to-live cache with synchronized access and deep copies of values. The loader is called only when the key has no valid entry.
## Dependencies / Dependencias
Importa `deepcopy`, `dataclass`, `RLock`, `monotonic` y herramientas genéricas de tipado. Bootstrap crea estas cachés para cámaras e incidencias.
## Contents / Contenido
### `T`
- **ES:** Parámetro genérico de tipo para los valores almacenados.
- **EN:** Generic type parameter for stored values.
### `_Entry[T]`
- **ES:** Dataclass privada que agrupa un valor cacheado y su instante de expiración.
- **EN:** Private dataclass grouping a cached value and its expiration time.
### `_Entry.value`, `_Entry.expires_at`
- **ES:** Valor de tipo `T` e instante de expiración según el reloj configurado.
- **EN:** Value of type `T` and expiration instant according to the configured clock.
### `TtlCache[T]`
- **ES:** Caché con TTL configurado por instancia; usa un `RLock` reentrante para proteger el diccionario.
- **EN:** Cache with a per-instance TTL; uses an `RLock` to protect its dictionary.
### `TtlCache.__init__(self, ttl_seconds: float, clock: Callable[[], float] = monotonic) -> None`
- **ES:** Guarda la duración y el reloj (por defecto `monotonic`), y crea el diccionario y bloqueo.
- **EN:** Stores the duration and clock (defaulting to `monotonic`), and creates the dictionary and lock.
### `TtlCache.get_or_load(self, key: str, loader: Callable[[], T]) -> T`
- **ES:** Bajo bloqueo, carga y almacena una copia profunda si no hay entrada o ya expiró; devuelve otra copia profunda. La expiración se calcula como hora actual más TTL.
- **EN:** Under lock, loads and stores a deep copy when there is no entry or it has expired; returns another deep copy. Expiration is current time plus TTL.
### `TtlCache.invalidate(self, key: str) -> None`
- **ES:** Elimina la clave si existe; si no existe, no produce error.
- **EN:** Removes the key if present; it does not raise if absent.
### `TtlCache.clear(self) -> None`
- **ES:** Elimina todas las entradas bajo bloqueo.
- **EN:** Removes all entries under the lock.
