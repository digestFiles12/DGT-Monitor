# Continuidad para un nuevo chat

Este documento contiene el contexto mínimo suficiente para continuar la implementación sin consultar conversaciones anteriores ni memorias internas.

## Instrucción de reanudación

Usa este texto al abrir un chat nuevo:

> Continúa la implementación de `DGT-Monitor`. Lee primero `docs/CONTINUIDAD_NUEVO_CHAT.md`, después `docs/PLAN_REFACTORIZACION.md`, `docs/ARQUITECTURA.md` y `docs/DECISIONES.md`. Comprueba el estado Git y ejecuta la suite antes de editar. Continúa por el siguiente incremento indicado y mantén actualizados estos documentos.

## Repositorios y rutas

- Proyecto nuevo: `e:\Proyectos\digestFiles12\DGT-Monitor`.
- GitHub privado: `https://github.com/digestFiles12/DGT-Monitor`.
- Proyecto de referencia funcional: `e:\Proyectos\digestFiles12\DGT30_GUI`.
- GitHub de referencia: `https://github.com/digestFiles12/DGT30_GUI`.
- No copiar el monolito del proyecto antiguo. Consultarlo solo para reproducir comportamiento y assets.

## Estado Git verificado

- Rama activa: `feature/initial-oop-architecture`.
- Remoto seguido: `origin/feature/initial-oop-architecture`.
- Último commit: `651c56f Add modular FastAPI and WebSocket adapters`.
- Commit anterior estable: `8ccda9b Build shared DGT domain and application services`.
- El repositorio estaba limpio y sincronizado al crear este documento.

## Entorno

- Windows y PowerShell.
- Python 3.12.
- Entorno virtual exclusivo: `e:\Proyectos\digestFiles12\DGT-Monitor\.venv`.
- Ejecutar siempre Python, pip y pytest mediante `.\.venv\Scripts\python.exe`.
- Paquete instalado en modo editable.
- Dependencias web y `httpx2` ya instaladas en la venv local.
- En una instalación limpia usar `.\.venv\Scripts\python.exe -m pip install -e ".[dev]"`.
- Si Windows bloquea `__editable__.dgt_monitor-0.1.0.pth`, no reinstalar el paquete mientras otro proceso use la venv; instalar solo la dependencia necesaria o cerrar ese proceso.

## Validación conocida

Última validación completa:

```text
9 passed
compileall correcto
```

Comandos:

```powershell
Set-Location e:\Proyectos\digestFiles12\DGT-Monitor
.\.venv\Scripts\python.exe -m pytest test -q
.\.venv\Scripts\python.exe -m compileall -q dgt_monitor dashboard
git diff --check
```

Las pruebas no acceden a la red DGT.

## Implementado

### Dominio

- Dataclasses `Incident`, `Camera`, `IncidentStats`, `IncidentFilters` y `CameraFilters`.
- Serialización explícita mediante `to_dict()`.
- Traducción DATEX2, limpieza de texto, normalización de carretera y punto kilométrico.
- Distancia Haversine.
- Excepciones propias y puertos mediante `Protocol`.

### Infraestructura

- `RequestsXmlClient` con sesión, headers, timeout y `DgtDownloadError`.
- Parsers DATEX2 de incidentes y cámaras que producen modelos.
- Repositorios DGT inyectables.
- `TtlCache` genérica con `RLock`, carga única, invalidación y copia profunda.
- TTL: incidentes 120 segundos; cámaras 300 segundos.

### Aplicación

- `IncidentService`: caché, filtros y estadísticas.
- `CameraService`: filtros, distancia, límite y cobertura a 1 km.
- La cobertura usa un índice por carretera normalizada para evitar comparar cada incidente con todas las cámaras.
- `DgtApplicationService`: fachada serializable para API y futura GUI.
- `build_application()`: composition root de producción.

### API

- `create_app(service=None)` inyectable.
- CORS configurado.
- `GET /api/health`.
- `GET /api/incidents`.
- `GET /api/cameras`.
- `WS /ws/incidents`, intervalo predeterminado 120 segundos y límites 5-300.
- Errores de dominio convertidos en HTTP 502.
- Wrapper estable `dashboard.app:app`.

## Árbol implementado

```text
dgt_monitor/
  bootstrap.py
  core/{models,constants,exceptions,ports,localization,text,geometry}.py
  infrastructure/http.py
  infrastructure/cache.py
  infrastructure/repositories.py
  infrastructure/parsers/{base,incident,camera}.py
  application/{incidents,cameras,facade}.py
  api/factory.py
  api/dependencies.py
  api/routes/{health,incidents,cameras}.py
  gui/__init__.py
dashboard/{__init__,app}.py
test/unit/{test_core,test_parsers_cache}.py
test/integration/test_facade.py
test/api/test_api.py
```

## Siguiente incremento exacto

Completar la fase 5 con dashboard estático y PWA:

1. Consultar `DGT30_GUI/dashboard/static/` como referencia visual y funcional.
2. Crear `DGT-Monitor/dashboard/static/index.html`, `styles.css`, `app.js`, `manifest.webmanifest`, `sw.js` e iconos.
3. Crear rutas para `/`, `/manifest.webmanifest` y `/sw.js`, y montar `/static` desde la app factory.
4. Mantener la API y WebSocket actuales; el frontend solo los consume.
5. Añadir pruebas de rutas PWA y assets.
6. Ejecutar suite y compilación.
7. Actualizar `docs/API.md`, `docs/DESPLIEGUE.md`, este documento y el plan.
8. Crear un commit separado y publicarlo.

Después de PWA, iniciar la GUI modular según `docs/GUI.md`.

## Pendientes globales

- Dashboard HTML/CSS/JS/PWA.
- GUI PyQt6 modular completa.
- Wrappers raíz `DGT.py` y `DGT_V2.py`.
- Workers QThread de incidentes, cámaras e imágenes.
- Tests GUI offscreen y checklist manual.
- `render.yaml`, requisitos compatibles y GitHub Actions.
- Documentación final, smoke real opcional y PR hacia `main`.

## Restricciones

- No introducir FastAPI, PyQt6 o `requests` en `core`.
- No hacer peticiones reales a DGT desde pruebas.
- No mezclar diccionarios y modelos dentro del dominio.
- No restaurar el `DGT_V2.py` monolítico borrado.
- Mantener `dashboard.app:app` como punto ASGI.
- Conservar contratos JSON y nombres de query params del proyecto de referencia.
- No rediseñar visualmente el dashboard durante la migración; preservar su comportamiento y apariencia actual.