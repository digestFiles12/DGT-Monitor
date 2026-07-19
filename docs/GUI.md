# GUI PyQt6

La GUI modular esta operativa. Consume `DgtApplicationService` mediante workers en `QThread`, sin incluir parsing, repositorios ni cache en los widgets. Incluye modo claro/oscuro en la ventana principal y en el dialogo de camaras. El dashboard web complementario muestra las incidencias sin cobertura con un icono de camara tachada rojo, reemplaza imagenes de camara no disponibles por un fallback visual localizado y anade busqueda exacta/regex, filtro de camaras con incidencia y scroll general/interno.

## Estructura actual

```text
dgt_monitor/gui/
  __main__.py
  dialogs/{__init__,cameras}.py
  entrypoints.py
  main_window.py
  workers.py
```

`MainWindow` ofrece filtros por provincia, municipio, carretera, modo de busqueda (`contains`, `exact`, `regex`), gravedad y cobertura de camara, tarjetas estadisticas clicables por tipo, tabla seleccionable, panel de detalle con fechas humanizadas y acceso a camaras cercanas. En el dashboard web, el contador de camaras de cada incidencia es accionable: abre la camara directamente cuando solo hay una y muestra un desplegable cuando hay varias. `IncidentLoadWorker` ejecuta la carga fuera del hilo de interfaz y propaga payload, error y finalizacion mediante senales.

El dashboard web no reemplaza a la GUI, pero comparte la misma fachada. Sus controles adicionales (`match_mode`, `incident_coverage`, mapa y scroll responsive) deben mantenerse en servicios/API antes de replicarse en escritorio; no deben implementarse como logica aislada en JavaScript.

`CamerasDialog` muestra cámaras cercanas de una incidencia seleccionada en un diálogo no modal. Construye `CameraFilters` con carretera, provincia, punto kilométrico y coordenadas de la incidencia, usa el rango compartido `CAMERA_MATCH_RANGE_KM` para no divergir del dashboard/API, ejecuta `CameraLoadWorker` en `QThread` y mantiene vivas las referencias hasta la finalización.

Las imágenes de cámaras se descargan con `ImageLoadWorker` en segundo plano. El diálogo renderiza miniaturas con `QPixmap`, conserva aspecto mediante escalado suave y muestra un estado legible cuando la imagen no está disponible. Al pulsar una miniatura cargada se abre un visor a pantalla completa; Escape o click cierran el visor. En el dashboard, el visor modal usa un tamaño contenido antes de fullscreen y sustituye fallos de carga o placeholders grises de DGT por un panel propio con icono `wifi-off`, titulo y texto secundario localizados.

El tema visual se centraliza en `dgt_monitor.gui.theme` y se aplica tanto a `MainWindow` como a `CamerasDialog`.

## Ejecución

```powershell
.\.venv\Scripts\python.exe -m dgt_monitor.gui
```

## Reglas

- Los workers llaman a `DgtApplicationService`; no descargan ni parsean XML.
- Los widgets no conocen repositorios ni cachés.
- `MainWindow` coordina estado, timer, selección, filtros, filtro estadístico y workers.
- Los diálogos de cámaras son no modales e independientes.
- La imagen conserva aspecto y se centra dentro de su celda.
- Deben mantenerse referencias a diálogos/workers hasta su finalización.

## Compatibilidad final

`DGT.py` y `DGT_V2.py` serán wrappers mínimos que llaman a funciones de `gui.entrypoints`. `DGT_V2.py` define la paridad funcional completa.

## Pendiente

- Temporizador configurable y registro de actividad visible.
- Valorar una vista dedicada de camaras en escritorio si se quiere replicar la pestana completa de camaras del dashboard.
- Wrappers de compatibilidad de escritorio.