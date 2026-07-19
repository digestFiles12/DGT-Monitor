"""Shared configuration defaults for DGT data sources."""

DGT_INCIDENTS_URL = "https://nap.dgt.es/datex2/v3/dgt/SituationPublication/datex2_v36.xml"
DGT_CAMERAS_URL = "https://nap.dgt.es/datex2/v3/dgt/DevicePublication/camaras_datex2_v36.xml"

HTTP_TIMEOUT_SECONDS = 15
INCIDENT_CACHE_SECONDS = 120
CAMERA_CACHE_SECONDS = 300
CAMERA_MATCH_RANGE_KM = 2.0

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/xml,text/xml,*/*",
}