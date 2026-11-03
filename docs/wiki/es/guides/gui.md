# GUI de escritorio (PyQt6)
La GUI vive en `src/dgt_monitor/gui/` y consume `DgtApplicationService` mediante workers en `QThread`; los widgets no contienen parsing, repositorios ni caché.
## Estructura
```text
src/dgt_monitor/gui/
  __main__.py          # python -m dgt_monitor.gui
  entrypoints.py       # run(): crea QApplication y MainWindow(build_application())
  main_window.py       # MainWindow
  workers.py           # IncidentLoadWorker, CameraLoadWorker, ImageLoadWorker
  theme.py             # temas claro/oscuro y hojas de estilo
  dialogs/cameras.py   # CamerasDialog y visor a pantalla completa
```
Los subpaquetes `widgets/` y `workers/` existen pero no contienen módulos.
## Ejecución
```powershell
.\.venv\Scripts\python.exe -m dgt_monitor.gui
```
## `MainWindow`
- Filtros: provincia, municipio, carretera, modo de búsqueda (`contains`, `exact`, `regex`), gravedad (`highest`, `high`, `medium`, `low`) y cámara (`with`, `without`), con botones «Aplicar filtros» y «Limpiar».
- Tarjetas estadísticas clicables por tipo, tabla de siete columnas con selección por fila y panel de detalle con fechas legibles.
- Botón «Ver cámaras» que abre `CamerasDialog` para la incidencia seleccionada.
- Botón «Actualizar» que lanza una nueva carga; modo claro/oscuro con `toggle_theme`/`set_theme`.
- No hay temporizador de refresco automático ni registro de actividad visible.
## `CamerasDialog`
- Diálogo no modal que construye `CameraFilters` con carretera, provincia, punto kilométrico y coordenadas de la incidencia, y usa `CAMERA_MATCH_RANGE_KM` para coincidir con la API y el dashboard.
- `CameraLoadWorker` carga las cámaras e `ImageLoadWorker` descarga las imágenes en segundo plano.
- Las miniaturas se escalan conservando el aspecto; si la imagen falla se muestra un estado legible.
- Al pulsar una miniatura se abre un visor a pantalla completa que se cierra con Escape o con un clic.
## Tema
`dgt_monitor.gui.theme` centraliza `normalize_theme`, `next_theme`, `main_window_stylesheet` y `camera_dialog_stylesheet`, aplicados a la ventana principal y al diálogo de cámaras.
## Reglas
- Los workers llaman a `DgtApplicationService`; no descargan ni parsean XML.
- Los widgets no conocen repositorios ni cachés.
- `MainWindow` coordina estado, selección, filtros, filtro estadístico y workers.
- Los diálogos de cámaras son no modales e independientes.
- Hay que conservar referencias a diálogos y workers hasta que terminen, y cerrar los hilos en `closeEvent`.
## Relación con el dashboard web
El dashboard (ver [la guía de la API](api.md)) comparte la misma fachada. Los controles adicionales de la web (pestañas de gráficas, mapa y favoritas) no existen en escritorio; si se replican, la lógica debe vivir en los servicios y no en la interfaz. Las gráficas en consola están disponibles con `python -m dgt_monitor.menu` (véase [el menú de consola](../menu.md)).
## Pruebas
Las pruebas de GUI están en `tests/gui/` y se ejecutan con `QT_QPA_PLATFORM=offscreen`; véase [la guía de pruebas](testing.md).
