# dgt_monitor/infrastructure/http.py
Adapts `requests` to the XML-client contract and converts request failures into a domain exception. The response is treated as UTF-8 text.
## Dependencies
Imports `requests`, `HTTP_HEADERS`, and `HTTP_TIMEOUT_SECONDS` from [constants](../core/constants.md), and `DgtDownloadError` from [exceptions](../core/exceptions.md). DGT repositories use this client through the `XmlClient` port.
## Contents
### `RequestsXmlClient`
- HTTP adapter that retrieves remote documents as text.
### `RequestsXmlClient.__init__(self, session: requests.Session | None = None, timeout: int = HTTP_TIMEOUT_SECONDS) -> None`
- Uses the supplied session or creates a new `requests` session; stores the supplied timeout.
### `RequestsXmlClient.get(self, url: str) -> str`
- Requests the URL with configured headers and timeout, checks the status, sets UTF-8 encoding, and returns `response.text`. A `RequestException` is chained as `DgtDownloadError` including the URL.
