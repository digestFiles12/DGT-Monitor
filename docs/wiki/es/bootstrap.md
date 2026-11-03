# dgt_monitor/bootstrap.py
Compone las dependencias de producción para construir el servicio principal de la aplicación. Configura los almacenes, clientes, repositorios, parsers y cachés concretos.
## Dependencias
Importa servicios de `application`, actividad, constantes y modelos del núcleo, así como adaptadores de `infrastructure`. La aplicación usa `build_application` como punto de composición.
## Contenido
### `logger`
- Logger del módulo usado para registrar fallos al inicializar persistencia de incidencias.
### `build_activity_store_and_init()`
- Crea el almacén de actividad, lo registra en `core.activity` y devuelve la instancia.
### `build_application() -> DgtApplicationService`
- Inicializa actividad, crea un cliente HTTP y repositorios DGT, e intenta construir el almacén de incidencias. Si falla esa persistencia, registra la excepción y continúa con `store=None`; crea servicios con cachés TTL y devuelve `DgtApplicationService`.
