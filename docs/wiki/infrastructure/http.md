# dgt_monitor/infrastructure/http.py
**ES:** Adapta `requests` al contrato de cliente XML y convierte fallos de petición en una excepción propia del dominio. La respuesta se interpreta como texto UTF-8.
**EN:** Adapts `requests` to the XML-client contract and converts request failures into a domain exception. The response is treated as UTF-8 text.
## Dependencies / Dependencias
Importa `requests`, `HTTP_HEADERS` y `HTTP_TIMEOUT_SECONDS` de [constants](../core/constants.md), y `DgtDownloadError` de [exceptions](../core/exceptions.md). Los repositorios DGT consumen este cliente mediante el puerto `XmlClient`.
## Contents / Contenido
### `RequestsXmlClient`
- **ES:** Adaptador HTTP que obtiene documentos remotos como texto.
- **EN:** HTTP adapter that retrieves remote documents as text.
### `RequestsXmlClient.__init__(self, session: requests.Session | None = None, timeout: int = HTTP_TIMEOUT_SECONDS) -> None`
- **ES:** Usa la sesión recibida o crea una nueva sesión de `requests`; conserva el tiempo de espera recibido.
- **EN:** Uses the supplied session or creates a new `requests` session; stores the supplied timeout.
### `RequestsXmlClient.get(self, url: str) -> str`
- **ES:** Solicita la URL con las cabeceras y timeout configurados, valida el estado, fuerza codificación UTF-8 y devuelve `response.text`. Una `RequestException` se encadena como `DgtDownloadError` con la URL.
- **EN:** Requests the URL with configured headers and timeout, checks the status, sets UTF-8 encoding, and returns `response.text`. A `RequestException` is chained as `DgtDownloadError` including the URL.
