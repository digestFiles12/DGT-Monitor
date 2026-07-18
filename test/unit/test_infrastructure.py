"""Tests for HTTP client and repository adapters."""

from unittest.mock import MagicMock

import pytest
import requests

from dgt_monitor.core.exceptions import DgtDownloadError
from dgt_monitor.core.models import Camera, Incident
from dgt_monitor.infrastructure.http import RequestsXmlClient
from dgt_monitor.infrastructure.repositories import DgtCameraRepository, DgtIncidentRepository


def test_requests_xml_client_returns_text_on_success():
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "<payload/>"
    mock_session.get.return_value = mock_response

    client = RequestsXmlClient(session=mock_session, timeout=5)
    result = client.get("https://example.test/data.xml")

    assert result == "<payload/>"
    mock_response.raise_for_status.assert_called_once()
    assert mock_response.encoding == "utf-8"


def test_requests_xml_client_raises_download_error_on_failure():
    mock_session = MagicMock()
    mock_session.get.side_effect = requests.RequestException("connection refused")

    client = RequestsXmlClient(session=mock_session)
    with pytest.raises(DgtDownloadError, match="connection refused"):
        client.get("https://example.test/data.xml")


def test_incident_repository_delegates_to_client_and_parser():
    mock_client = MagicMock()
    mock_client.get.return_value = "<xml/>"
    mock_parser = MagicMock()
    mock_parser.parse.return_value = [Incident(id="sit-1")]

    repo = DgtIncidentRepository(mock_client, mock_parser, url="https://example.test/incidents.xml")
    result = repo.fetch()

    mock_client.get.assert_called_once_with("https://example.test/incidents.xml")
    mock_parser.parse.assert_called_once_with("<xml/>")
    assert result[0].id == "sit-1"


def test_camera_repository_delegates_to_client_and_parser():
    mock_client = MagicMock()
    mock_client.get.return_value = "<xml/>"
    mock_parser = MagicMock()
    mock_parser.parse.return_value = [Camera(id="cam-1")]

    repo = DgtCameraRepository(mock_client, mock_parser, url="https://example.test/cameras.xml")
    result = repo.fetch()

    mock_client.get.assert_called_once_with("https://example.test/cameras.xml")
    mock_parser.parse.assert_called_once_with("<xml/>")
    assert result[0].id == "cam-1"
