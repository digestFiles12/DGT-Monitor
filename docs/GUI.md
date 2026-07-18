# GUI PyQt6

La primera versión modular de la GUI está operativa. Consume `DgtApplicationService` mediante un worker en `QThread`, sin incluir red, parsing ni caché en los widgets.

## Estructura actual

```text
dgt_monitor/gui/
  __main__.py
  entrypoints.py
  main_window.py
  workers.py
```

`MainWindow` ofrece filtros por provincia, municipio, carretera y gravedad, tarjetas estadísticas, tabla seleccionable y panel de detalle. `IncidentLoadWorker` ejecuta la carga fuera del hilo de interfaz y propaga payload, error y finalización mediante señales.

## Ejecución

```powershell
.\.venv\Scripts\python.exe -m dgt_monitor.gui
```

## Reglas

- Los workers llaman a `DgtApplicationService`; no descargan ni parsean XML.
- Los widgets no conocen repositorios ni cachés.
- `MainWindow` coordina estado, timer, selección, filtros y workers.
- Los diálogos de cámaras e imágenes son no modales e independientes.
- La imagen conserva aspecto y se centra dentro de su celda.
- Deben mantenerse referencias a diálogos/workers hasta su finalización.

## Compatibilidad final

`DGT.py` y `DGT_V2.py` serán wrappers mínimos que llaman a funciones de `gui.entrypoints`. `DGT_V2.py` define la paridad funcional completa.

## Pendiente

- Worker y diálogo no modal para cámaras cercanas.
- Visor de imágenes con conservación de aspecto.
- Temporizador configurable y registro de actividad visible.
- Wrappers de compatibilidad de escritorio.