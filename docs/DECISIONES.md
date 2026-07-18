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

Una cámara cubre un incidente si comparte carretera normalizada, provincia compatible y está a un máximo de 1 km por punto kilométrico. Se indexa por carretera para reducir coste.

## ADR-007: compatibilidad de entradas

Render seguirá usando `dashboard.app:app`. Los wrappers pequeños `DGT.py` y `DGT_V2.py` se crearán sobre `gui.entrypoints`; no se restaurará código monolítico.

## ADR-009: Render no ejecuta PyQt6

Render sirve FastAPI y el dashboard web/PWA. La GUI PyQt6 queda como entrada local de escritorio y se valida con tests offscreen.

## ADR-008: pruebas herméticas

Toda prueba usa XML local, repositorios falsos o una fachada falsa. Las consultas live son smoke manual opcional.