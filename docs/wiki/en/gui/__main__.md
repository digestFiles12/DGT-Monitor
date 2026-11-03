# dgt_monitor/gui/__main__.py
Allows the desktop interface to be run as a Python module and starts Qt's event loop.
## Dependencies
Imports `run` from `dgt_monitor.gui.entrypoints`; `python -m dgt_monitor.gui` uses `SystemExit` to propagate the exit code.
## Contents
### Module entry
- Calls `run()` and exits the process with its returned integer.
