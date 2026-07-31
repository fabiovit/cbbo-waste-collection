# CBBO Waste Collection

Custom integration for Home Assistant for the waste-collection calendars published by CBBO.

## Version 0.2.1

- configuration of all 18 municipalities shown on the CBBO portal;
- optional North/South zone selection for Mazzano;
- parsing of Drupal/FullCalendar JSON and date-bearing HTML calendar markup;
- local cache of the last successful download;
- bundled 2026 fallback for Mazzano North/South, so existing Mazzano installations keep working if the website is unavailable or changes markup;
- sensors for today, tomorrow, next collection and days to next collection;
- binary sensors for tomorrow's collection and evening exposure;
- Home Assistant calendar entity.

The online calendar remains the authoritative source. For municipalities other than Mazzano, the first setup requires the CBBO page to return a recognisable online calendar. After the first successful refresh, cached data are used during temporary outages.

## Installation with HACS

Add `https://github.com/fabiovit/cbbo-waste-collection` as a custom repository of category **Integration**, download it and restart Home Assistant.

Then go to **Settings → Devices & services → Add integration → CBBO Waste Collection**.

## Data source diagnostic

Collection sensors expose `data_source`:

- `online`: current CBBO page;
- `cache`: last successful download;
- `memory`: previous data kept in memory;
- `bundled_mazzano_2026`: Mazzano 2026 emergency fallback.

## Disclaimer

This is an independent community project and is not affiliated with CBBO. Always check exceptional changes against the official CBBO calendar.
