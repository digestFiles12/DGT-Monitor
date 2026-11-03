# Integración DATEX2

## Fuentes

- Incidentes: `SituationPublication/datex2_v36.xml`.
- Cámaras: `DevicePublication/camaras_datex2_v36.xml`.

Las URL, cabeceras, timeout y tiempos de caché están centralizados en `src/dgt_monitor/core/constants.py`.

## Flujo

1. `RequestsXmlClient` descarga texto XML y traduce errores HTTP a `DgtDownloadError`.
2. Los repositorios seleccionan URL y parser.
3. `IncidentParser` y `CameraParser` buscan tags por sufijo para tolerar namespaces DATEX2.
4. Los parsers devuelven modelos de dominio, nunca diccionarios sin tipo.

FastAPI, el dashboard web y la GUI PyQt6 reciben datos ya normalizados desde `DgtApplicationService`; ninguna capa de presentacion descarga ni parsea DATEX2.

La relacion entre incidencias y camaras no viene directamente resuelta por DATEX2. El proyecto la calcula despues del parseo usando carretera normalizada, provincia compatible y punto kilometrico dentro de 2.0 km. Por eso el parser solo extrae datos crudos seguros; la cobertura pertenece a `CameraService`.

Un XML mal formado produce `DgtParseError`. Los campos opcionales ausentes usan valores seguros y las coordenadas inválidas se convierten en `None`.

## Pruebas

La suite usa XML local reducido. Las pruebas automatizadas no acceden a los servidores DGT. Los filtros exactos/regex y la cobertura de camaras se prueban con modelos y repositorios falsos, no con datos live.