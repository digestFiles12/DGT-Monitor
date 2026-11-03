# Despliegue

## Servicio de Render

El servicio está definido en `render.yaml` como `dgt-monitor`, con plan gratuito. Usa Python 3.12.0, instala el proyecto con el extra `[dev]`, ejecuta las pruebas y compila `src` durante la compilación. El proceso de inicio ejecuta `uvicorn dgt_monitor.web.app:app` en `0.0.0.0` y en el puerto proporcionado por Render. La comprobación de salud configurada es `GET /api/health` y el despliegue automático está habilitado.

La aplicación guarda las incidencias en `INCIDENT_DB_PATH=/tmp/incidents.db` y la actividad en `ACTIVITY_DB_PATH=/tmp/activity.db`. En el plan gratuito de Render, esos archivos están en almacenamiento efímero: pueden perderse al reiniciar o volver a desplegar el servicio. La base de incidencias se vuelve a rellenar desde DGT en la primera solicitud después de perderse el archivo; no debe tratarse como almacenamiento persistente. El registro de actividad también es temporal.

## Variables de entorno

`render.yaml` define estos valores y secretos:

| Variable | Configuración actual |
| --- | --- |
| `PYTHON_VERSION` | `3.12.0` |
| `PYTHONUNBUFFERED` | `1` |
| `ACTIVITY_API_KEYS` | Secreto configurado en Render; no se sincroniza desde el archivo |
| `ACTIVITY_REVOKED_API_KEYS` | Secreto configurado en Render; no se sincroniza desde el archivo |
| `INCIDENT_DB_PATH` | `/tmp/incidents.db` |
| `ACTIVITY_DB_PATH` | `/tmp/activity.db` |

No guardes claves reales en el repositorio. Los dos valores `ACTIVITY_*KEYS` están marcados para configurarse fuera de `render.yaml`.

## Flujo de integración y publicación

El flujo de GitHub Actions instala `.[dev]` y ejecuta las pruebas en Ubuntu con Python 3.12. El paso de publicación solo se activa para una inserción en `release` o `main`, después de que termine el trabajo de pruebas; ese paso informa que Render realizará el despliegue automático y no llama directamente a una API de Render. La selección efectiva de la rama observada por Render depende de la configuración del servicio.

Para preparar una publicación, sigue el flujo `develop` → `release` → `main` descrito en [Flujo de trabajo Git](gitflow.md). Para preparar el entorno local, consulta [Desarrollo](development.md).

## Prueba de humo

Después del despliegue, sustituye el dominio de ejemplo por el dominio asignado por Render y ejecuta en PowerShell:

```powershell
$base = 'https://<servicio>.onrender.com'
Invoke-RestMethod "$base/api/health"
Invoke-WebRequest "$base/" -Method Get
Invoke-WebRequest "$base/manifest.webmanifest" -Method Get
Invoke-WebRequest "$base/sw.js" -Method Get
Invoke-WebRequest "$base/api/incidents" -Method Get
```

Comprueba que las solicitudes responden correctamente, que la comprobación de salud indica que el servicio está operativo y que el panel y sus recursos estáticos se sirven. La primera solicitud de incidencias puede tardar mientras se descarga o se vuelve a cargar la información de DGT.
