# dgt_monitor/application/facade.py
Provides a single facade for adapters (API and GUI) to request localized incidents, statistics, groupings, and cameras without knowing the internal services.
## Dependencies
Composes `IncidentService` and `CameraService`, uses filter models and localization utilities, and delegates statistics calculations to `application.statistics`. The API factory builds/uses this facade, and routes access it through the facade.
## Contents
### `DgtApplicationService`
- Facade that combines incident and camera services and prepares responses for adapters.
### `DgtApplicationService.__init__(incidents, cameras)`
- Stores the incident and camera services that handle facade operations.
### `DgtApplicationService.get_incident_payload(filters=None, refresh=False, language="es")`
- Loads incidents and cameras, annotates coverage, returns filtered incidents and statistics computed with all filters except `kind`. Includes UTC time, count, normalized language, and translated labels.
### `DgtApplicationService._localized_incident(item, translator)`
- Copies an incident dictionary and adds translated labels for the listed fields; `cause` uses compound translation and the others use simple translation.
### `DgtApplicationService._filters_without_kind(filters)`
- Builds a new filter preserving province, municipality, road, severity, camera, match mode, and `community` while omitting `kind`; therefore the statistics count does not depend on the selected category.
### `DgtApplicationService.get_statistics(level="province", refresh=False)`
- Returns the six indicators (`total`, `accidents`, `roadworks`, `breakdowns`, `obstructions`, and `weather`) grouped by province or region, including maxima and minima; other levels are rejected by the delegated function.
### `DgtApplicationService.get_grouped_incidents(refresh=False)`
- Returns groupings by province, region, type, weekday, and type+geography (`by_province_type`, `by_region_type`), plus `region_provinces` (feed provinces by community) and localized `labels.by_type` in Spanish and English; keys remain DATEX II codes.
### `DgtApplicationService.get_cameras(filters=None, refresh=False)`
- Filters cameras and returns UTC time, count, and items. When incident coverage is requested, it postpones the limit until after coverage selection and then applies it.
