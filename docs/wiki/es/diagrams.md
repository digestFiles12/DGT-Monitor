# Diagramas de arquitectura y flujo

Todos los diagramas usan Mermaid (se renderizan en GitHub y VS Code).

## 1. Arquitectura por capas

```mermaid
flowchart TD
    subgraph Presentacion
        WEB[Dashboard web / PWA<br/>web/static]
        GUI[GUI PyQt6 opcional<br/>gui/]
        MENU[Menu de consola<br/>menu.py]
    end
    subgraph Adaptadores
        API[FastAPI<br/>api/routes]
    end
    subgraph Aplicacion
        FACADE[DgtApplicationService<br/>facade.py]
        INC[IncidentService]
        CAM[CameraService]
        STATS[statistics.py]
    end
    subgraph Dominio
        CORE[core: modelos, puertos,<br/>regiones, texto, geometria]
    end
    subgraph Infraestructura
        HTTP[http.py - requests]
        PARSERS[parsers DATEX II]
        CACHE[cache TTL]
        STORE[(SQLite<br/>incident_store)]
    end
    DGT[(DGT NAP<br/>XML DATEX II)]

    WEB --> API
    GUI --> FACADE
    MENU --> FACADE
    API --> FACADE
    FACADE --> INC
    FACADE --> CAM
    FACADE --> STATS
    INC --> CORE
    CAM --> CORE
    STATS --> CORE
    INC --> CACHE
    INC --> STORE
    HTTP --> DGT
    PARSERS --> HTTP
    INC --> PARSERS
    HTTP -.implementa puertos.-> CORE
    STORE -.implementa puertos.-> CORE
```

Regla: `core` no importa FastAPI, PyQt6 ni requests; las capas externas dependen hacia dentro.

## 2. Flujo de datos: de la DGT al dashboard

```mermaid
flowchart LR
    A[DGT: XML DATEX II] -->|requests GET| B[Parser<br/>ElementTree + namespaces]
    B --> C[Incident<br/>modelo tipado]
    C --> D[Provincia a CCAA<br/>core/regions.py]
    C --> E[(SQLite<br/>upsert por id)]
    D --> F[group_incidents<br/>provincia, CCAA, tipo, dia]
    F --> G[find_extremes<br/>maximo y minimo]
    F --> H[grouped_incidents.json]
    G --> I["/api/stats"]
    F --> J["/api/stats/grouped"]
    I --> K[Dashboard: 4 barras + 4 quesos]
    J --> K
    H --> L[Menu de consola + matplotlib]
```

## 3. Secuencia de una peticion

```mermaid
sequenceDiagram
    actor U as Usuario
    participant W as Dashboard (app.js)
    participant R as FastAPI /api/stats
    participant F as Fachada
    participant S as IncidentService
    participant C as Cache 120 s
    participant D as DGT
    participant DB as SQLite

    U->>W: Abre pestana Graficas
    W->>R: GET /api/stats?level=region
    R->>F: get_statistics(level)
    F->>S: get_all()
    alt cache valida
        S->>C: lectura
        C-->>S: incidencias
    else cache caducada
        S->>D: GET XML
        D-->>S: DATEX II
        S->>S: parsear
        S->>DB: upsert por id (errores solo se registran)
    end
    S-->>F: lista de incidencias
    F->>F: agrupar + maximo/minimo
    F-->>R: estadisticas
    R-->>W: JSON
    W-->>U: Renderiza graficas Chart.js
```

## 4. Tiempo real (WebSocket)

```mermaid
sequenceDiagram
    participant W as Navegador
    participant WS as /ws/incidents
    participant S as Servicio
    W->>WS: conectar (interval, filtros)
    loop cada interval segundos
        WS->>S: get_incident_payload (hilo aparte)
        S-->>WS: payload
        WS-->>W: send_json
    end
    W--xWS: desconexion
```

## 5. Despliegue

```mermaid
flowchart LR
    DEV[feature/*] -->|PR| DEVELOP[develop]
    DEVELOP -->|PR| REL[release]
    REL -->|PR| MAIN[main]
    MAIN -->|CI verde| RENDER[Render<br/>uvicorn dgt_monitor.web.app:app]
    RENDER --> DB[(/tmp/incidents.db<br/>efimero)]
    RENDER --> DGT[(DGT)]
```

En el plan gratuito de Render el disco no es persistente: la base se recrea desde la DGT en la primera peticion.
