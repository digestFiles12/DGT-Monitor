# dgt_monitor/core/ports.py
Define contratos basados en `Protocol` para que la lógica de dominio dependa de interfaces y no de adaptadores concretos. Los repositorios y clientes de infraestructura proporcionan las implementaciones.
## Dependencias
Importa `Protocol`, `Sequence` y los modelos `Camera` e `Incident`. Los repositorios de infraestructura implementan estos contratos.
## Contenido
### `XmlClient`
- Contrato de cliente que obtiene el texto de un recurso XML a partir de su URL.
### `XmlClient.get(self, url: str) -> str`
- Operación abstracta que devuelve el contenido textual solicitado.
### `IncidentRepository`
- Contrato de repositorio de incidencias.
### `IncidentRepository.fetch(self) -> Sequence[Incident]`
- Obtiene una secuencia de incidencias.
### `CameraRepository`
- Contrato de repositorio de cámaras.
### `CameraRepository.fetch(self) -> Sequence[Camera]`
- Obtiene una secuencia de cámaras.
### `IncidentStore`
- Contrato para guardar, cargar y contar incidencias persistidas.
### `IncidentStore.save(self, incidents: Sequence[Incident]) -> object`
- Guarda una secuencia de incidencias; el tipo de resultado queda deliberadamente abstracto en este protocolo.
### `IncidentStore.load_all(self) -> list[Incident]`
- Carga todas las incidencias almacenadas.
### `IncidentStore.count(self) -> int`
- Devuelve el número de incidencias almacenadas.
