# dgt_monitor/web/static/manifest.webmanifest
Provides installation metadata for the DGT Monitor progressive web app.
## Dependencies
Web App Manifest JSON format; the browser reads it through the `rel="manifest"` link in `index.html`.
## Contents
### PWA fields
- `name` and `short_name` are “DGT Monitor”; `description` describes the incident/camera monitor. `start_url: "/"` sets the launch URL, `display: "standalone"` requests a standalone presentation, and `background_color` is `#f5f6f4` and `theme_color` is `#b91c1c`. `lang: "es"` declares the language.
