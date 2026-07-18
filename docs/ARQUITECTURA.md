# Arquitectura

```mermaid
flowchart TD
    WEB[Dashboard web/PWA] --> API[FastAPI]
    GUI[GUI PyQt6 local] --> APP[Servicios de aplicacion]
    API --> APP
    APP --> CORE[Dominio y puertos]
    INFRA[HTTP, DATEX2, cache y activity store] --> CORE
    APP --> INFRA
```

## Regla de dependencias

`core` no importa PyQt6, FastAPI ni requests. `infrastructure` implementa los puertos del dominio. `application` orquesta los casos de uso. `api`, `dashboard` y `gui` solo adaptan entradas y salidas.

El dashboard web consume la API desde el mismo origen y no contiene reglas DATEX2. La GUI de escritorio es local-only: Render ejecuta el dashboard/API, no PyQt6.
