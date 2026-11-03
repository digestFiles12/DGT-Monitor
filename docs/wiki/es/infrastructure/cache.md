# dgt_monitor/infrastructure/cache.py
Implementa una caché genérica en memoria con tiempo de vida, acceso sincronizado y copias profundas de valores. El cargador solo se invoca cuando la clave no tiene una entrada válida.
## Dependencias
Importa `deepcopy`, `dataclass`, `RLock`, `monotonic` y herramientas genéricas de tipado. Bootstrap crea estas cachés para cámaras e incidencias.
## Contenido
### `T`
- Parámetro genérico de tipo para los valores almacenados.
### `_Entry[T]`
- Dataclass privada que agrupa un valor cacheado y su instante de expiración.
### `_Entry.value`, `_Entry.expires_at`
- Valor de tipo `T` e instante de expiración según el reloj configurado.
### `TtlCache[T]`
- Caché con TTL configurado por instancia; usa un `RLock` reentrante para proteger el diccionario.
### `TtlCache.__init__(self, ttl_seconds: float, clock: Callable[[], float] = monotonic) -> None`
- Guarda la duración y el reloj (por defecto `monotonic`), y crea el diccionario y bloqueo.
### `TtlCache.get_or_load(self, key: str, loader: Callable[[], T]) -> T`
- Bajo bloqueo, carga y almacena una copia profunda si no hay entrada o ya expiró; devuelve otra copia profunda. La expiración se calcula como hora actual más TTL.
### `TtlCache.invalidate(self, key: str) -> None`
- Elimina la clave si existe; si no existe, no produce error.
### `TtlCache.clear(self) -> None`
- Elimina todas las entradas bajo bloqueo.
