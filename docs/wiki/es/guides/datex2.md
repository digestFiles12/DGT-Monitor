# Integración DATEX II

La aplicación obtiene publicaciones XML de la DGT mediante las URL definidas en `core/constants.py`: `SituationPublication` para incidencias y `DevicePublication` para cámaras.

## Descarga y selección del parser

`RequestsXmlClient` realiza una petición HTTP con cabeceras y timeout configurados, establece UTF-8 y devuelve el texto XML. Los errores de `requests` se convierten en `DgtDownloadError`. `DgtIncidentRepository` y `DgtCameraRepository` enlazan el cliente con su parser y la URL de cada publicación.

## Análisis de incidencias

`IncidentParser` analiza `SituationPublication` con `xml.etree.ElementTree` y crea modelos `Incident` para las situaciones que contienen un `situationRecord`. `Datex2Parser` busca elementos por sufijo del nombre de etiqueta, de modo que no necesita conocer el prefijo del namespace. Un XML mal formado se informa como `DgtParseError`.

El parser obtiene el tipo del atributo XML Schema Instance, limpia los campos textuales, combina la causa con el detalle cuando existe y convierte latitud y longitud opcionales. Resuelve la comunidad desde la provincia con `region_for_province`; si no se reconoce, usa el campo `autonomousCommunity` del registro cuando está disponible. Los campos ausentes conservan valores predeterminados y una coordenada no numérica se convierte en `None`.

`CameraParser` analiza la publicación de dispositivos y produce modelos `Camera`. Las relaciones de cobertura no se leen como una asociación de la fuente: se calculan más tarde por el servicio de cámaras.

## Salida

Los parsers entregan modelos tipados a los repositorios y servicios; la API, el dashboard y la GUI consumen los resultados de aplicación en vez de descargar y analizar directamente el XML. Véase [Modelos](models.md) y [Servicios](services.md).
