# DGT Monitor

Aplicacion modular para consultar incidentes y camaras de trafico de la DGT desde una GUI PyQt6 y un dashboard FastAPI/PWA.

El proyecto esta siendo implementado desde cero con arquitectura orientada a objetos. Consulta [docs/INDEX.md](docs/INDEX.md) para ver el plan y la documentacion tecnica.

## Desarrollo

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest
```
