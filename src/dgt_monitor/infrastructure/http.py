"""HTTP adapter for remote XML resources."""

import requests

from dgt_monitor.core.constants import HTTP_HEADERS, HTTP_TIMEOUT_SECONDS
from dgt_monitor.core.exceptions import DgtDownloadError


class RequestsXmlClient:
    def __init__(self, session: requests.Session | None = None, timeout: int = HTTP_TIMEOUT_SECONDS) -> None:
        self._session = session or requests.Session()
        self._timeout = timeout

    def get(self, url: str) -> str:
        try:
            response = self._session.get(url, headers=HTTP_HEADERS, timeout=self._timeout)
            response.raise_for_status()
            response.encoding = "utf-8"
            return response.text
        except requests.RequestException as exc:
            raise DgtDownloadError(f"No se pudo descargar {url}: {exc}") from exc