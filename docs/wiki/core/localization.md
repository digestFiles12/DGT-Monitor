# dgt_monitor/core/localization.py
**ES:** Traduce valores DATEX2 para las capas de presentación a español o inglés. Incluye un catálogo de traducciones y una conversión legible para códigos no catalogados.
**EN:** Translates DATEX2 values for presentation layers into Spanish or English. It includes a translation catalog and a readable fallback for uncatalogued codes.
## Dependencies / Dependencias
Importa `re` de la biblioteca estándar y no importa otros módulos del proyecto. `IncidentParser` utiliza `Translator` para etiquetar valores extraídos.
## Contents / Contenido
### `DEFAULT_LOCALE`, `SUPPORTED_LOCALES`
- **ES:** Fijan español (`"es"`) como idioma predeterminado y español e inglés como idiomas admitidos.
- **EN:** Set Spanish (`"es"`) as the default locale and Spanish and English as supported locales.
### `TRANSLATION_CATALOG`
- **ES:** Diccionario bilingüe indexado primero por idioma y luego por código DATEX2; contiene etiquetas para tipos, causas, gravedad, dirección y otros valores. No es necesario enumerar cada traducción para entender su estructura.
- **EN:** Bilingual dictionary indexed first by locale and then by DATEX2 code; it contains labels for types, causes, severity, direction, and other values. Listing every translation is unnecessary to understand its structure.
### `normalize_locale(locale: str | None) -> str`
- **ES:** Extrae el idioma antes de un guion regional, ignora mayúsculas y minúsculas y devuelve `es` si está ausente o no está admitido.
- **EN:** Takes the language portion before a regional hyphen, ignores case, and returns `es` when missing or unsupported.
### `Translator`
- **ES:** Mantiene el idioma normalizado y el catálogo de traducciones seleccionado; permite traducir valores individuales o compuestos.
- **EN:** Holds the normalized locale and selected translation catalog; supports translating individual and compound values.
### `Translator.__init__(self, locale: str | None = DEFAULT_LOCALE, translations: dict[str, str] | None = None) -> None`
- **ES:** Normaliza el idioma y usa el catálogo personalizado proporcionado o el catálogo del idioma seleccionado.
- **EN:** Normalizes the locale and uses the supplied custom catalog or the catalog for the selected locale.
### `Translator.translate(self, value: str | None) -> str`
- **ES:** Devuelve la etiqueta catalogada o un código convertido a texto legible. Los valores vacíos y `N/A`/`NA` se sustituyen por la etiqueta de dato ausente.
- **EN:** Returns the catalog label or a code converted to readable text. Empty values and `N/A`/`NA` are replaced by the missing-data label.
### `Translator.translate_compound(self, value: str | None, separator: str = " - ") -> str`
- **ES:** Divide el valor por el separador, traduce cada parte no vacía y vuelve a unirlas; un valor vacío produce la etiqueta de dato ausente.
- **EN:** Splits the value by the separator, translates each non-empty part, and joins them again; an empty value produces the missing-data label.
### `Translator.missing_label(self) -> str`
- **ES:** Propiedad que devuelve `Sin dato` en español y `N/A` en inglés.
- **EN:** Property returning `Sin dato` for Spanish and `N/A` for English.
### `humanize_code(value: str) -> str`
- **ES:** Sustituye guiones y guiones bajos, separa palabras en camel case y normaliza espacios; devuelve `N/A` si el resultado queda vacío.
- **EN:** Replaces hyphens and underscores, separates camel-case words, and normalizes whitespace; returns `N/A` if the result is empty.
