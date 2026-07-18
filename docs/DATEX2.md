# Integración DATEX2

## Fuentes

- Incidentes: `SituationPublication/datex2_v36.xml`.
- Cámaras: `DevicePublication/camaras_datex2_v36.xml`.

Las URL, cabeceras, timeout y tiempos de caché están centralizados en `dgt_monitor/core/constants.py`.

## Flujo

1. `RequestsXmlClient` descarga texto XML y traduce errores HTTP a `DgtDownloadError`.
2. Los repositorios seleccionan URL y parser.
3. `IncidentParser` y `CameraParser` buscan tags por sufijo para tolerar namespaces DATEX2.
4. Los parsers devuelven modelos de dominio, nunca diccionarios sin tipo.

Un XML mal formado produce `DgtParseError`. Los campos opcionales ausentes usan valores seguros y las coordenadas inválidas se convierten en `None`.

## Pruebas

La suite usa XML local reducido. Las pruebas automatizadas no acceden a los servidores DGT.