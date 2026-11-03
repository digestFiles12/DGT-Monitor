# dgt_monitor/core/ports.py
**ES:** Define contratos basados en `Protocol` para que la lógica de dominio dependa de interfaces y no de adaptadores concretos. Los repositorios y clientes de infraestructura proporcionan las implementaciones.
**EN:** Defines `Protocol`-based contracts so domain logic depends on interfaces rather than concrete adapters. Infrastructure clients and repositories provide implementations.
## Dependencies / Dependencias
Importa `Protocol`, `Sequence` y los modelos `Camera` e `Incident`. Los repositorios de infraestructura implementan estos contratos.
## Contents / Contenido
### `XmlClient`
- **ES:** Contrato de cliente que obtiene el texto de un recurso XML a partir de su URL.
- **EN:** Client contract for retrieving XML text from a URL.
### `XmlClient.get(self, url: str) -> str`
- **ES:** Operación abstracta que devuelve el contenido textual solicitado.
- **EN:** Abstract operation returning the requested text content.
### `IncidentRepository`
- **ES:** Contrato de repositorio de incidencias.
- **EN:** Incident repository contract.
### `IncidentRepository.fetch(self) -> Sequence[Incident]`
- **ES:** Obtiene una secuencia de incidencias.
- **EN:** Fetches a sequence of incidents.
### `CameraRepository`
- **ES:** Contrato de repositorio de cámaras.
- **EN:** Camera repository contract.
### `CameraRepository.fetch(self) -> Sequence[Camera]`
- **ES:** Obtiene una secuencia de cámaras.
- **EN:** Fetches a sequence of cameras.
### `IncidentStore`
- **ES:** Contrato para guardar, cargar y contar incidencias persistidas.
- **EN:** Contract for saving, loading, and counting persisted incidents.
### `IncidentStore.save(self, incidents: Sequence[Incident]) -> object`
- **ES:** Guarda una secuencia de incidencias; el tipo de resultado queda deliberadamente abstracto en este protocolo.
- **EN:** Saves a sequence of incidents; the return type is deliberately abstract in this protocol.
### `IncidentStore.load_all(self) -> list[Incident]`
- **ES:** Carga todas las incidencias almacenadas.
- **EN:** Loads all stored incidents.
### `IncidentStore.count(self) -> int`
- **ES:** Devuelve el número de incidencias almacenadas.
- **EN:** Returns the number of stored incidents.
