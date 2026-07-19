# API HTTP y WebSocket

La aplicación se construye con `dgt_monitor.api.factory.create_app()`. En producción, `dashboard/app.py` mantiene el punto ASGI `dashboard.app:app`.

## Endpoints

- `GET /`: dashboard web responsive.
- `GET /manifest.webmanifest`: manifiesto PWA.
- `GET /sw.js`: service worker del dashboard.
- `GET /static/*`: assets web versionados por el service worker.
- `GET /api/health`: estado y hora UTC.
- `GET /api/incidents`: filtros `province`, `municipality`, `road`, `severity`, `kind`, `camera` (`with`/`without`), `match_mode` (`contains`/`exact`/`regex`) y `lang` (`es`/`en`).
- `GET /api/cameras`: filtros `province`, `road`, `km`, `lat`, `lon`, `limit`, `all`, `max_km_delta`, `max_distance_km`, `incident_coverage` y `match_mode`.
- `GET /api/activity/`: log de actividad paginado; requiere `X-API-Key`.
- `GET /api/activity/stream`: stream SSE de actividad; soporta `replay` y `once=true`.
- `GET /api/activity/export`: export CSV de actividad; requiere `X-API-Key`.
- `POST /api/activity/clear`: limpia el log de actividad; requiere `X-API-Key`.
- `WS /ws/incidents`: entrega inmediata y refresco periódico; intervalo predeterminado de 120 segundos. Acepta los mismos filtros de incidencias, incluido `match_mode`, y `lang` que REST.

Las rutas no descargan ni parsean XML. Obtienen `DgtApplicationService` desde `app.state`, lo que permite sustituir toda la aplicación por un doble en pruebas.

Los errores `DgtError` se traducen a HTTP 502. El WebSocket envía un objeto con `error` sin cerrar la conexión por un fallo transitorio de DGT.

## Filtros de busqueda

Los filtros textuales de provincia, municipio y carretera aceptan tres modos:

- `contains` (por defecto): compara sin distinguir mayusculas y devuelve coincidencias parciales.
- `exact`: exige igualdad completa tras `casefold()`.
- `regex`: aplica `re.search()` insensible a mayusculas; una expresion regular invalida no rompe la API, simplemente no produce coincidencia.

Ejemplos:

```http
GET /api/incidents?road=A-52&match_mode=exact
GET /api/incidents?province=^Za&match_mode=regex
GET /api/cameras?road=^A-\d+$&match_mode=regex&incident_coverage=true
```

`/api/cameras` usa `incident_coverage=true` para devolver solo camaras que cubren alguna incidencia activa. La cobertura se calcula por carretera normalizada, provincia compatible y diferencia de punto kilometrico menor o igual a `CAMERA_MATCH_RANGE_KM`, actualmente 2.0 km. Si se combina con `limit`, la fachada elimina temporalmente el limite, calcula cobertura y luego recorta el resultado final para no perder coincidencias validas por truncado previo.

## Localizacion

Los valores DATEX2 se conservan en campos técnicos en inglés (`type`, `cause`, `severity`, etc.) y la fachada añade campos de presentación `*_label` según `lang`. El idioma por defecto es español (`es`) y también se soporta inglés (`en`). Si DGT introduce un código nuevo sin traducción explícita, el traductor lo humaniza para evitar mostrar camelCase o códigos internos en las interfaces.

## Autenticacion de Activity API

Los endpoints de actividad usan cabecera `X-API-Key`. Las claves aceptadas se configuran con `ACTIVITY_API_KEYS`; las revocadas con `ACTIVITY_REVOKED_API_KEYS`. La comparación de claves aceptadas usa `secrets.compare_digest()`.

## Dashboard web

El dashboard consume los endpoints REST desde el mismo origen y no contiene lógica DATEX2. Incluye vistas de incidencias, camaras y mapa, selector superior de idioma ES/EN, filtros por provincia, municipio, carretera, severidad, tipo, cobertura de camara, modo de busqueda y camaras con incidencia. Las celdas estadisticas son clicables por tipo, las filas de incidencia se despliegan con todos sus detalles disponibles y existe carga progresiva de incidencias para listas largas.

Los textos de incidencias usan campos `*_label` localizados, no codigos DATEX2. En la tabla de incidencias, el boton de camaras cercanas consulta `/api/cameras`; si solo hay una camara abre directamente su imagen en tamano contenido y, si hay varias, muestra un desplegable para elegir destino. Las incidencias sin cobertura visual muestran un icono `camera-off` rojo con etiqueta accesible localizada.

La pestaña de camaras puede filtrar por carretera/provincia/PK y activar `incident_coverage=true`. La pestaña de mapa reutiliza los filtros activos: para incidencias carga `/api/incidents` y para camaras calcula un scope relacionado, de forma que los contadores de tabs no diverjan. En escenarios como Zamora/A-52, una incidencia con una camara cercana debe reflejar 1 incidencia, 1 camara y 2 puntos en mapa.

La pagina conserva scroll general en movil y escritorio. La tabla y el grid de camaras mantienen scroll interno con `-webkit-overflow-scrolling: touch` y `scrollbar-gutter: stable` para que el contenido denso no rompa el layout.

Al pulsar la imagen del visor, se expande a pantalla completa; si la imagen falla o DGT devuelve un placeholder gris de no disponible, se reemplaza por un fallback propio con icono `wifi-off`, titulo y texto secundario en el idioma activo. Puede instalarse como PWA y conserva el shell estatico en cache (`dgt-monitor-v51`); las respuestas de `/api/` nunca se cachean.

## Desarrollo

```powershell
.\.venv\Scripts\python.exe -m uvicorn dashboard.app:app --reload
```