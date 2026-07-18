# Arquitectura

```mermaid
flowchart TD
    GUI[GUI PyQt6] --> APP[Servicios de aplicacion]
    API[FastAPI] --> APP
    APP --> CORE[Dominio y puertos]
    INFRA[HTTP, DATEX2 y cache] --> CORE
    APP --> INFRA
```

## Regla de dependencias

`core` no importa PyQt6, FastAPI ni requests. `infrastructure` implementa los puertos del dominio. `application` orquesta los casos de uso. `api` y `gui` solo adaptan entradas y salidas.
