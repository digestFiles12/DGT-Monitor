# dgt_monitor/core/exceptions.py
**ES:** Define excepciones del dominio sin depender del transporte ni de la interfaz de usuario. Las excepciones específicas comparten una clase base propia.
**EN:** Defines domain exceptions without depending on transport or user-interface frameworks. The specific exceptions share an application base class.
## Dependencies / Dependencias
No tiene dependencias de proyecto; las capas de infraestructura y aplicación pueden lanzar o capturar estas excepciones.
## Contents / Contenido
### `DgtError(Exception)`
- **ES:** Excepción base de la aplicación para errores DGT.
- **EN:** Application base exception for DGT-related errors.
### `DgtDownloadError(DgtError)`
- **ES:** Indica que no se pudo descargar un recurso remoto DGT.
- **EN:** Indicates that a remote DGT resource could not be downloaded.
### `DgtParseError(DgtError)`
- **ES:** Indica que no se pudo analizar un documento DATEX2.
- **EN:** Indicates that a DATEX2 document could not be parsed.
### `DgtValidationError(DgtError)`
- **ES:** Indica que una entrada no satisface el contrato de un caso de uso.
- **EN:** Indicates that input does not satisfy a use-case contract.
