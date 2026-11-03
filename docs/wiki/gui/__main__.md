# dgt_monitor/gui/__main__.py
**ES:** Permite ejecutar la interfaz de escritorio como módulo de Python e inicia el event loop de Qt.
**EN:** Allows the desktop interface to be run as a Python module and starts Qt's event loop.
## Dependencies / Dependencias
Importa `run` desde `dgt_monitor.gui.entrypoints`; el comando `python -m dgt_monitor.gui` usa `SystemExit` para propagar el código de salida.
Imports `run` from `dgt_monitor.gui.entrypoints`; `python -m dgt_monitor.gui` uses `SystemExit` to propagate the exit code.
## Contents / Contenido
### Module entry
- **ES:** Llama `run()` y termina el proceso con el entero que devuelve.
- **EN:** Calls `run()` and exits the process with its returned integer.
