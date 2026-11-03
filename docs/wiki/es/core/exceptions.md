# dgt_monitor/core/exceptions.py
Define excepciones del dominio sin depender del transporte ni de la interfaz de usuario. Las excepciones específicas comparten una clase base propia.
## Dependencias
No tiene dependencias de proyecto; las capas de infraestructura y aplicación pueden lanzar o capturar estas excepciones.
## Contenido
### `DgtError(Exception)`
- Excepción base de la aplicación para errores DGT.
### `DgtDownloadError(DgtError)`
- Indica que no se pudo descargar un recurso remoto DGT.
### `DgtParseError(DgtError)`
- Indica que no se pudo analizar un documento DATEX2.
### `DgtValidationError(DgtError)`
- Indica que una entrada no satisface el contrato de un caso de uso.
