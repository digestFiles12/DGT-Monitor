# Render Deployment Guide

## Overview

DGT-Monitor is configured for automatic deployment to Render.com via `render.yaml` and GitHub Actions. Render serves the FastAPI API and browser dashboard/PWA; the PyQt6 desktop GUI is local-only.

## Prerequisites

1. **GitHub Account** with access to the repository
2. **Render Account** (https://render.com)
3. **Environment Variables** configured in Render dashboard

## Deployment Steps

### Step 1: Connect GitHub Repository to Render

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Select **"Deploy existing repo"** or **"Connect repository"**
4. Authorize GitHub and select the project repository
5. Select the branch to deploy

### Step 2: Configure Render Service

Render will auto-detect `render.yaml` and apply configuration:

- **Service Name:** `dgt-monitor`
- **Runtime:** Python 3.12 (`PYTHON_VERSION=3.12.0`)
- **Build Command:** `pip install -e ".[dev]" && python -m pytest tests -q --tb=no && python -m compileall -q src`
- **Start Command:** `uvicorn dgt_monitor.web.app:app --host 0.0.0.0 --port $PORT`
- **Health Check:** `GET /api/health`
- **Auto-deploy:** Enabled

### Step 3: Set Environment Variables

In Render Dashboard → Environment:

```
ACTIVITY_API_KEYS=<comma-separated-valid-keys>
ACTIVITY_REVOKED_API_KEYS=<comma-separated-revoked-keys>
ACTIVITY_DB_PATH=/tmp/activity.db
PYTHONUNBUFFERED=1
PYTHON_VERSION=3.12.0
```

Example:
```
ACTIVITY_API_KEYS=prod-key-1,prod-key-2
ACTIVITY_REVOKED_API_KEYS=old-key-1
```

### Step 4: Deploy

1. **Manual Deploy:**
   - Render Dashboard → Service → **Deploy Latest**

2. **Auto Deploy:**
   - Push to the configured deployment branch
   - GitHub Actions will run tests
   - On success, Render auto-deploys

### Step 5: Verify Deployment

1. **Check Service Status:** Render Dashboard → Status
2. **Test Health Endpoint:**
   ```bash
   curl https://<your-service>.onrender.com/api/health
   ```
3. **Test dashboard/PWA assets:**
   ```bash
   curl https://<your-service>.onrender.com/
   curl https://<your-service>.onrender.com/manifest.webmanifest
   curl https://<your-service>.onrender.com/sw.js
   ```
4. **Test Activity API:**
   ```bash
   curl -H "X-API-Key: <valid-key>" \
        https://<your-service>.onrender.com/api/activity/
   ```

## Monitoring

### Logs

- **Render Dashboard:** Logs tab (build and runtime logs)
- **GitHub Actions:** Actions tab (CI/CD pipeline logs)

### Health Check

Render performs periodic health checks on `GET /api/health`:
- **Interval:** 30 seconds
- **Timeout:** 10 seconds
- **Initial Delay:** 10 seconds

If health checks fail, service will be marked as unhealthy.

## Troubleshooting

### Build Fails

1. Check build log in Render Dashboard
2. Verify `pyproject.toml` dependencies
3. Ensure Python 3.12 compatibility
4. Run locally: `python -m pytest tests -q`

### Tests Fail During Build

1. Review test output in Render build logs
2. Check environment variables are set correctly
3. Verify API key format in `ACTIVITY_API_KEYS`

### Health Check Fails

1. Check runtime logs in Render Dashboard
2. Verify `dgt_monitor.web.app:app` is accessible
3. Confirm `GET /api/health` returns `{"status": "ok", ...}`

### Service Crashes

1. Review runtime logs
2. Check memory (512 MB) is sufficient
3. Verify environment variables (especially `ACTIVITY_API_KEYS`)
4. Look for uncaught exceptions in error logs

## Performance Notes

- **Build Time:** ~2-3 minutes (first deploy), ~30-60s (subsequent)
- **Startup Time:** ~10 seconds
- **Memory:** 512 MB (tunable via `memoryMB` in `render.yaml`)
- **CPU:** 0.5 CPU (tunable via `cpuCount` in `render.yaml`)

## Environment Variables Reference

| Variable | Type | Required | Example |
|----------|------|----------|---------|
| `ACTIVITY_API_KEYS` | String | No | `key1,key2,key3` |
| `ACTIVITY_REVOKED_API_KEYS` | String | No | `old-key` |
| `ACTIVITY_DB_PATH` | Path | No | `/tmp/activity.db` |
| `PYTHONUNBUFFERED` | Boolean | Yes | `1` |
| `PYTHON_VERSION` | String | Yes | `3.12.0` |

## API Endpoints (After Deployment)

```
Base URL: https://<service-name>.onrender.com

GET /                                    # Dashboard web
GET /manifest.webmanifest               # PWA manifest
GET /sw.js                              # Service worker
GET /api/health                          # Health check
GET /api/incidents?road=A-1              # List incidents
GET /api/incidents?road=A-1&match_mode=exact
GET /api/incidents?road=^A-\d+$&match_mode=regex
GET /api/cameras?road=A-1                # List cameras
GET /api/cameras?road=A-1&incident_coverage=true
WS /ws/incidents                         # WebSocket stream
GET /api/activity/                       # Activity log (requires X-API-Key)
GET /api/activity/stream                 # SSE stream (requires X-API-Key)
POST /api/activity/clear                 # Clear activity (requires X-API-Key)
GET /api/activity/export                 # CSV export (requires X-API-Key)
```

## Rollback

1. **Recent Changes:** Render Dashboard → Service → **Redeploy**
2. **Specific Commit:** Push alternate commit to branch
3. **Previous Deployment:** Check Render build history

## Production Deployment

To deploy to production:

1. Create `main` branch (protected)
2. Configure Render auto-deploy to track `main`
3. Merge the validated feature branch to main via pull request
4. Render will auto-deploy from `main` branch

## Functional Smoke Checklist

- `/` loads the dashboard shell and `sw.js` reports cache `dgt-monitor-v51`.
- `/api/incidents` accepts `match_mode=contains`, `exact` and `regex`.
- `/api/cameras` accepts `incident_coverage=true` and returns only cameras related to active incidents.
- The browser dashboard scrolls at page level on desktop/mobile, while incident table and camera grid keep internal scroll.
- Map counts match active incident and camera filters.

---

**Render Dashboard:** https://dashboard.render.com  
**Documentation:** https://render.com/docs
