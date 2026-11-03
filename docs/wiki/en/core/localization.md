# dgt_monitor/core/localization.py
Translates DATEX2 values for presentation layers into Spanish or English. It includes a translation catalog and a readable fallback for uncatalogued codes.
## Dependencies
Imports `re` from the standard library and no other project modules. `IncidentParser` uses `Translator` to label extracted values.
## Contents
### `DEFAULT_LOCALE`, `SUPPORTED_LOCALES`
- Set Spanish (`"es"`) as the default locale and Spanish and English as supported locales.
### `TRANSLATION_CATALOG`
- Bilingual dictionary indexed first by locale and then by DATEX2 code; it contains labels for types, causes, severity, direction, and other values. Listing every translation is unnecessary to understand its structure.
### `normalize_locale(locale: str | None) -> str`
- Takes the language portion before a regional hyphen, ignores case, and returns `es` when missing or unsupported.
### `Translator`
- Holds the normalized locale and selected translation catalog; supports translating individual and compound values.
### `Translator.__init__(self, locale: str | None = DEFAULT_LOCALE, translations: dict[str, str] | None = None) -> None`
- Normalizes the locale and uses the supplied custom catalog or the catalog for the selected locale.
### `Translator.translate(self, value: str | None) -> str`
- Returns the catalog label or a code converted to readable text. Empty values and `N/A`/`NA` are replaced by the missing-data label.
### `Translator.translate_compound(self, value: str | None, separator: str = " - ") -> str`
- Splits the value by the separator, translates each non-empty part, and joins them again; an empty value produces the missing-data label.
### `Translator.missing_label(self) -> str`
- Property returning `Sin dato` for Spanish and `N/A` for English.
### `humanize_code(value: str) -> str`
- Replaces hyphens and underscores, separates camel-case words, and normalizes whitespace; returns `N/A` if the result is empty.
