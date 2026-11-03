# dgt_monitor/core/ports.py
Defines `Protocol`-based contracts so domain logic depends on interfaces rather than concrete adapters. Infrastructure clients and repositories provide implementations.
## Dependencies
Imports `Protocol`, `Sequence`, and the `Camera` and `Incident` models. Infrastructure repositories implement these contracts.
## Contents
### `XmlClient`
- Client contract for retrieving XML text from a URL.
### `XmlClient.get(self, url: str) -> str`
- Abstract operation returning the requested text content.
### `IncidentRepository`
- Incident repository contract.
### `IncidentRepository.fetch(self) -> Sequence[Incident]`
- Fetches a sequence of incidents.
### `CameraRepository`
- Camera repository contract.
### `CameraRepository.fetch(self) -> Sequence[Camera]`
- Fetches a sequence of cameras.
### `IncidentStore`
- Contract for saving, loading, and counting persisted incidents.
### `IncidentStore.save(self, incidents: Sequence[Incident]) -> object`
- Saves a sequence of incidents; the return type is deliberately abstract in this protocol.
### `IncidentStore.load_all(self) -> list[Incident]`
- Loads all stored incidents.
### `IncidentStore.count(self) -> int`
- Returns the number of stored incidents.
