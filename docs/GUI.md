# GUI PyQt6

La GUI todavía no está implementada en el proyecto nuevo. La referencia funcional es `DGT30_GUI/DGT_V2.py`.

## Estructura prevista

```text
dgt_monitor/gui/
  entrypoints.py
  main_window.py
  workers/{incidents,cameras,image}.py
  widgets/{header,controls,filters,statistics,incident_table,details,log}.py
  dialogs/{cameras,camera_image}.py
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