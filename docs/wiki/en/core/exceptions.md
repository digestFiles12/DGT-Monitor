# dgt_monitor/core/exceptions.py
Defines domain exceptions without depending on transport or user-interface frameworks. The specific exceptions share an application base class.
## Dependencies
It has no project dependencies; infrastructure and application layers can raise or catch these exceptions.
## Contents
### `DgtError(Exception)`
- Application base exception for DGT-related errors.
### `DgtDownloadError(DgtError)`
- Indicates that a remote DGT resource could not be downloaded.
### `DgtParseError(DgtError)`
- Indicates that a DATEX2 document could not be parsed.
### `DgtValidationError(DgtError)`
- Indicates that input does not satisfy a use-case contract.
