# Desarrollo

## Requisitos

- Python 3.12 o posterior, conforme a `requires-python` en `pyproject.toml`.
- Git.

## Preparar el entorno

Desde la raíz del repositorio, crea un entorno virtual e instala las dependencias de desarrollo:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

El proyecto usa el diseño `src/`: el paquete está en `src/dgt_monitor`. El extra `[dev]` instala los extras `[web]`, `[gui]` y `[console]`, además de las dependencias de pruebas. Para instalar solo las dependencias opcionales de una modalidad, los extras disponibles son `[web]`, `[gui]` y `[console]`.

## Pruebas y comprobaciones

Ejecuta la suite desde la raíz del repositorio con Qt en modo sin pantalla:

```powershell
$env:QT_QPA_PLATFORM='offscreen'
.\.venv\Scripts\python.exe -m pytest tests -q
```

La integración continua también comprueba la compilación sintáctica con `compileall`, la importación de los paquetes y los cambios de espacios en blanco. La comprobación de compilación y `git diff --check` están marcadas como no bloqueantes en el flujo actual.

## Ejecutar la aplicación web en local

El punto de entrada ASGI es `dgt_monitor.web.app:app`:

```powershell
.\.venv\Scripts\python.exe -m uvicorn dgt_monitor.web.app:app --reload
```

## Documentación relacionada

- [Despliegue](deployment.md)
- [Flujo de trabajo Git](gitflow.md)
