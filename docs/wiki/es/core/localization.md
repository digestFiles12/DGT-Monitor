# dgt_monitor/core/localization.py
Traduce valores DATEX2 para las capas de presentación a español o inglés. Incluye un catálogo de traducciones y una conversión legible para códigos no catalogados.
## Dependencias
Importa `re` de la biblioteca estándar y no importa otros módulos del proyecto. `IncidentParser` utiliza `Translator` para etiquetar valores extraídos.
## Contenido
### `DEFAULT_LOCALE`, `SUPPORTED_LOCALES`
- Fijan español (`"es"`) como idioma predeterminado y español e inglés como idiomas admitidos.
### `TRANSLATION_CATALOG`
- Diccionario bilingüe indexado primero por idioma y luego por código DATEX2; contiene etiquetas para tipos, causas, gravedad, dirección y otros valores. No es necesario enumerar cada traducción para entender su estructura.
### `normalize_locale(locale: str | None) -> str`
- Extrae el idioma antes de un guion regional, ignora mayúsculas y minúsculas y devuelve `es` si está ausente o no está admitido.
### `Translator`
- Mantiene el idioma normalizado y el catálogo de traducciones seleccionado; permite traducir valores individuales o compuestos.
### `Translator.__init__(self, locale: str | None = DEFAULT_LOCALE, translations: dict[str, str] | None = None) -> None`
- Normaliza el idioma y usa el catálogo personalizado proporcionado o el catálogo del idioma seleccionado.
### `Translator.translate(self, value: str | None) -> str`
- Devuelve la etiqueta catalogada o un código convertido a texto legible. Los valores vacíos y `N/A`/`NA` se sustituyen por la etiqueta de dato ausente.
### `Translator.translate_compound(self, value: str | None, separator: str = " - ") -> str`
- Divide el valor por el separador, traduce cada parte no vacía y vuelve a unirlas; un valor vacío produce la etiqueta de dato ausente.
### `Translator.missing_label(self) -> str`
- Propiedad que devuelve `Sin dato` en español y `N/A` en inglés.
### `humanize_code(value: str) -> str`
- Sustituye guiones y guiones bajos, separa palabras en camel case y normaliza espacios; devuelve `N/A` si el resultado queda vacío.
