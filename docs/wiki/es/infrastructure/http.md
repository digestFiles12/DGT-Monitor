# dgt_monitor/infrastructure/http.py
Adapta `requests` al contrato de cliente XML y convierte fallos de petición en una excepción propia del dominio. La respuesta se interpreta como texto UTF-8.
## Dependencias
Importa `requests`, `HTTP_HEADERS` y `HTTP_TIMEOUT_SECONDS` de [constants](../core/constants.md), y `DgtDownloadError` de [exceptions](../core/exceptions.md). Los repositorios DGT consumen este cliente mediante el puerto `XmlClient`.
## Contenido
### `RequestsXmlClient`
- Adaptador HTTP que obtiene documentos remotos como texto.
### `RequestsXmlClient.__init__(self, session: requests.Session | None = None, timeout: int = HTTP_TIMEOUT_SECONDS) -> None`
- Usa la sesión recibida o crea una nueva sesión de `requests`; conserva el tiempo de espera recibido.
### `RequestsXmlClient.get(self, url: str) -> str`
- Solicita la URL con las cabeceras y timeout configurados, valida el estado, fuerza codificación UTF-8 y devuelve `response.text`. Una `RequestException` se encadena como `DgtDownloadError` con la URL.
