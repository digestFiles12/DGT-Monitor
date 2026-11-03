# Architecture and flow diagrams

All diagrams use Mermaid (rendered by GitHub and VS Code).

## 1. Layered architecture

```mermaid
flowchart TD
    subgraph Presentation
        WEB[Web dashboard / PWA<br/>web/static]
        GUI[Optional PyQt6 GUI<br/>gui/]
        MENU[Console menu<br/>menu.py]
    end
    subgraph Adapters
        API[FastAPI<br/>api/routes]
    end
    subgraph Application
        FACADE[DgtApplicationService<br/>facade.py]
        INC[IncidentService]
        CAM[CameraService]
        STATS[statistics.py]
    end
    subgraph Domain
        CORE[core: models, ports,<br/>regions, text, geometry]
    end
    subgraph Infrastructure
        HTTP[http.py - requests]
        PARSERS[DATEX II parsers]
        CACHE[TTL cache]
        STORE[(SQLite<br/>incident_store)]
    end
    DGT[(DGT NAP<br/>DATEX II XML)]

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
    HTTP -.implements ports.-> CORE
    STORE -.implements ports.-> CORE
```

Rule: `core` never imports FastAPI, PyQt6 or requests; outer layers depend inwards.

## 2. Data flow: from the DGT to the dashboard

```mermaid
flowchart LR
    A[DGT: DATEX II XML] -->|requests GET| B[Parser<br/>ElementTree + namespaces]
    B --> C[Incident<br/>typed model]
    C --> D[Province to region<br/>core/regions.py]
    C --> E[(SQLite<br/>upsert by id)]
    D --> F[group_incidents<br/>province, region, type, weekday]
    F --> G[find_extremes<br/>max and min]
    F --> H[grouped_incidents.json]
    G --> I["/api/stats"]
    F --> J["/api/stats/grouped"]
    I --> K[Dashboard: 4 bar + 4 pie charts]
    J --> K
    H --> L[Console menu + matplotlib]
```

## 3. Request sequence

```mermaid
sequenceDiagram
    actor U as User
    participant W as Dashboard (app.js)
    participant R as FastAPI /api/stats
    participant F as Facade
    participant S as IncidentService
    participant C as 120 s cache
    participant D as DGT
    participant DB as SQLite

    U->>W: Opens Charts tab
    W->>R: GET /api/stats?level=region
    R->>F: get_statistics(level)
    F->>S: get_all()
    alt cache valid
        S->>C: read
        C-->>S: incidents
    else cache expired
        S->>D: GET XML
        D-->>S: DATEX II
        S->>S: parse
        S->>DB: upsert by id (errors are only logged)
    end
    S-->>F: incident list
    F->>F: group + max/min
    F-->>R: statistics
    R-->>W: JSON
    W-->>U: Renders Chart.js charts
```

## 4. Real time (WebSocket)

```mermaid
sequenceDiagram
    participant W as Browser
    participant WS as /ws/incidents
    participant S as Service
    W->>WS: connect (interval, filters)
    loop every interval seconds
        WS->>S: get_incident_payload (worker thread)
        S-->>WS: payload
        WS-->>W: send_json
    end
    W--xWS: disconnect
```

## 5. Deployment

```mermaid
flowchart LR
    DEV[feature/*] -->|PR| DEVELOP[develop]
    DEVELOP -->|PR| REL[release]
    REL -->|PR| MAIN[main]
    MAIN -->|green CI| RENDER[Render<br/>uvicorn dgt_monitor.web.app:app]
    RENDER --> DB[(/tmp/incidents.db<br/>ephemeral)]
    RENDER --> DGT[(DGT)]
```

On Render's free plan the disk is not persistent: the database is rebuilt from the DGT on the first request.
