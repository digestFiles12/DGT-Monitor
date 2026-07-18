# Decisiones arquitectónicas

## ADR-001: repositorio nuevo

La refactorización vive en un repositorio independiente. El proyecto legado es solo una referencia funcional y no se fusiona ni se copia de forma monolítica.

## ADR-002: dependencias dirigidas

`core` no conoce frameworks. `infrastructure` implementa puertos; `application` orquesta; `api` y `gui` adaptan entrada/salida. Se evitan imports circulares y lógica de negocio en rutas o widgets.

## ADR-003: modelos internos únicos

El dominio usa dataclasses, no `Union[dict, objeto]`. La compatibilidad JSON se resuelve con `to_dict()` en el borde.

## ADR-004: inyección explícita

No se usan singletons globales. `build_application()` crea producción y `create_app(service=...)` permite dobles de prueba. La GUI recibirá la misma fachada por constructor.

## ADR-005: caché concurrente

`TtlCache` usa `RLock`, una carga por clave y copia profunda al leer. Existen instancias separadas para incidentes y cámaras.

## ADR-006: cobertura de cámaras

Una cámara cubre un incidente si comparte carretera normalizada, provincia compatible y está a un máximo de 1 km por punto kilométrico. Se indexa por carretera para reducir coste.

## ADR-007: compatibilidad de entradas

Render seguirá usando `dashboard.app:app`. Al implementar GUI se crearán wrappers pequeños `DGT.py` y `DGT_V2.py`; no se restaurará código monolítico.

## ADR-008: pruebas herméticas

Toda prueba usa XML local, repositorios falsos o una fachada falsa. Las consultas live son smoke manual opcional.