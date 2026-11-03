# dgt_monitor/gui/__main__.py
Permite ejecutar la interfaz de escritorio como módulo de Python e inicia el event loop de Qt.
## Dependencias
Importa `run` desde `dgt_monitor.gui.entrypoints`; el comando `python -m dgt_monitor.gui` usa `SystemExit` para propagar el código de salida.
## Contenido
### Inicio del módulo
- Llama `run()` y termina el proceso con el entero que devuelve.

