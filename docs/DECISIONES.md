# Decisiones arquitectónicas

## ADR-001: refactorizacion aislada

La refactorización mantiene una arquitectura nueva y no copia código legado de forma monolítica. Las referencias históricas se documentan solo como comportamiento esperado.

## ADR-002: dependencias dirigidas

`core` no conoce frameworks. `infrastructure` implementa puertos; `application` orquesta; `api` y `gui` adaptan entrada/salida. Se evitan imports circulares y lógica de negocio en rutas o widgets.

## ADR-003: modelos internos únicos

El dominio usa dataclasses, no `Union[dict, objeto]`. La compatibilidad JSON se resuelve con `to_dict()` en el borde.

## ADR-004: inyección explícita

No se usan singletons globales para la aplicacion principal. `build_application()` crea producción y `create_app(service=...)` permite dobles de prueba. La GUI recibe la misma fachada por constructor. La actividad conserva una fachada global pequeña por compatibilidad operativa, con store intercambiable.

## ADR-005: caché concurrente

`TtlCache` usa `RLock`, una carga por clave y copia profunda al leer. Existen instancias separadas para incidentes y cámaras.

## ADR-006: cobertura de cámaras

Una camara cubre un incidente si comparte carretera normalizada, provincia compatible y esta a un maximo de `CAMERA_MATCH_RANGE_KM` por punto kilometrico. El valor actual es 2.0 km para cubrir casos reales donde la camara util queda fuera de un umbral demasiado estrecho. Se indexa por carretera para reducir coste.

El mismo criterio se usa para anotar incidencias (`has_camera_coverage`, `camera_coverage_count`, `nearest_camera_km_delta`) y para filtrar camaras con `incident_coverage=true`.

## ADR-010: modos de busqueda textual

La busqueda textual se centraliza en `core.text.matches_text()` y se expresa mediante `match_mode`. Los modos soportados son `contains`, `exact` y `regex`. Un regex invalido devuelve no coincidencia en lugar de romper la peticion, porque el dashboard debe tolerar entradas exploratorias del usuario.

## ADR-011: scroll del dashboard

El dashboard conserva scroll general en `body/main` y scroll interno solo en superficies densas como tabla y grid de camaras. Esta decision evita bloquear la navegacion en movil o escritorio y mantiene usable la pestaña de camaras cuando hay muchas tarjetas.

## ADR-007: compatibilidad de entradas

Render seguirá usando `dashboard.app:app`. Los wrappers pequeños `DGT.py` y `DGT_V2.py` se crearán sobre `gui.entrypoints`; no se restaurará código monolítico.

## ADR-009: Render no ejecuta PyQt6

Render sirve FastAPI y el dashboard web/PWA. La GUI PyQt6 queda como entrada local de escritorio y se valida con tests offscreen.

## ADR-008: pruebas herméticas

Toda prueba usa XML local, repositorios falsos o una fachada falsa. Las consultas live son smoke manual opcional.