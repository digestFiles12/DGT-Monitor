# Deployment

## Render service

The service is defined in `render.yaml` as `dgt-monitor` on the free plan. It uses Python 3.12.0, installs the project with the `[dev]` extra, runs the test suite, and compiles `src` during the build. The start command runs `uvicorn dgt_monitor.web.app:app` on `0.0.0.0` and the port provided by Render. The configured health check is `GET /api/health`, and automatic deployment is enabled.

The application stores incidents at `INCIDENT_DB_PATH=/tmp/incidents.db` and activity at `ACTIVITY_DB_PATH=/tmp/activity.db`. On Render's free plan, these files are on ephemeral storage: they can be lost when the service restarts or is redeployed. The incident database is repopulated from DGT on the first request after its file is lost; it must not be treated as persistent storage. The activity log is temporary as well.

## Environment variables

`render.yaml` defines these values and secrets:

| Variable | Current configuration |
| --- | --- |
| `PYTHON_VERSION` | `3.12.0` |
| `PYTHONUNBUFFERED` | `1` |
| `ACTIVITY_API_KEYS` | Secret configured in Render; not synced from the file |
| `ACTIVITY_REVOKED_API_KEYS` | Secret configured in Render; not synced from the file |
| `INCIDENT_DB_PATH` | `/tmp/incidents.db` |
| `ACTIVITY_DB_PATH` | `/tmp/activity.db` |

Do not store real keys in the repository. Both `ACTIVITY_*KEYS` values are marked to be configured outside `render.yaml`.

## Integration and release flow

The GitHub Actions workflow installs `.[dev]` and runs tests on Ubuntu with Python 3.12. The deploy job only runs for a push to `release` or `main`, after the test job completes; that job reports that Render will auto-deploy and does not directly call a Render API. The branch watched by Render depends on the service configuration.

For a release, follow `develop` → `release` → `main` in the [Git workflow](gitflow.md). For local setup, see [Development](development.md).

## Smoke test

After deployment, replace the example domain with the domain assigned by Render and run these commands in PowerShell:

```powershell
$base = 'https://<service>.onrender.com'
Invoke-RestMethod "$base/api/health"
Invoke-WebRequest "$base/" -Method Get
Invoke-WebRequest "$base/manifest.webmanifest" -Method Get
Invoke-WebRequest "$base/sw.js" -Method Get
Invoke-WebRequest "$base/api/incidents" -Method Get
```

Check that the requests succeed, the health check reports that the service is operational, and the dashboard and static assets are served. The first incidents request may take longer while DGT data is downloaded or repopulated.
