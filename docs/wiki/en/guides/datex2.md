# DATEX II integration

The application retrieves DGT XML publications through the URLs defined in `core/constants.py`: `SituationPublication` for incidents and `DevicePublication` for cameras.

## Download and parser selection

`RequestsXmlClient` makes an HTTP request with configured headers and timeout, sets UTF-8, and returns the XML text. `requests` errors are converted to `DgtDownloadError`. `DgtIncidentRepository` and `DgtCameraRepository` connect the client to the parser and URL for each publication.

## Incident parsing

`IncidentParser` parses `SituationPublication` with `xml.etree.ElementTree` and creates `Incident` models for situations containing a `situationRecord`. `Datex2Parser` finds elements by tag-name suffix, so it does not need to know the namespace prefix. Malformed XML is reported as `DgtParseError`.

The parser reads the type from the XML Schema Instance attribute, cleans text fields, combines the cause with its detail when available, and parses optional latitude and longitude. It resolves the community from the province with `region_for_province`; when that province is unrecognized, it uses the record's `autonomousCommunity` field if present. Missing fields retain defaults, and a non-numeric coordinate becomes `None`.

`CameraParser` parses the device publication into `Camera` models. Coverage relationships are not read as source associations; they are calculated later by the camera service.

## Output

Parsers return typed models to repositories and services; the API, dashboard, and GUI consume application results rather than downloading and parsing XML directly. See [Models](models.md) and [Services](services.md).
