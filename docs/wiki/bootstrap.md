# dgt_monitor/bootstrap.py
**ES:** Compone las dependencias de producción para construir el servicio principal de la aplicación. Configura los almacenes, clientes, repositorios, parsers y cachés concretos.
**EN:** Composes production dependencies to build the main application service. It configures concrete stores, clients, repositories, parsers, and caches.
## Dependencies / Dependencias
Importa servicios de `application`, actividad, constantes y modelos del núcleo, así como adaptadores de `infrastructure`. La aplicación usa `build_application` como punto de composición.
## Contents / Contenido
### `logger`
- **ES:** Logger del módulo usado para registrar fallos al inicializar persistencia de incidencias.
- **EN:** Module logger used to report failures while initializing incident persistence.
### `build_activity_store_and_init()`
- **ES:** Crea el almacén de actividad, lo registra en `core.activity` y devuelve la instancia.
- **EN:** Creates the activity store, registers it in `core.activity`, and returns the instance.
### `build_application() -> DgtApplicationService`
- **ES:** Inicializa actividad, crea un cliente HTTP y repositorios DGT, e intenta construir el almacén de incidencias. Si falla esa persistencia, registra la excepción y continúa con `store=None`; crea servicios con cachés TTL y devuelve `DgtApplicationService`.
- **EN:** Initializes activity, creates an HTTP client and DGT repositories, and attempts to build the incident store. If persistence initialization fails, it logs the exception and continues with `store=None`; it creates services with TTL caches and returns `DgtApplicationService`.
