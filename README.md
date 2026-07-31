# CBBO Waste Collection

Custom integration for Home Assistant that exposes the public waste collection calendars published by CBBO.

## Supported municipalities

Acquafredda, Barbariga, Calvisano, Capriano del Colle, Carpenedolo, Castenedolo, Flero, Ghedi, Isorella, Mazzano, Montichiari, Montirone, Nuvolento, Nuvolera, Poncarale, Remedello, San Zeno Naviglio and Visano.

Mazzano supports the **North** and **South** zones.

## Entities

- Waste today
- Waste tomorrow
- Next collection
- Days until next collection
- Collection tomorrow
- Put out tonight
- Collection calendar

## Data source and cache

The integration reads the public calendar on the selected municipality page every six hours. The latest valid calendar is cached locally, so Home Assistant can continue using it during a temporary CBBO outage.

## Installation with HACS

1. Open HACS.
2. Add `https://github.com/fabiovit/cbbo-waste-collection` as a custom repository of type **Integration**.
3. Download the integration.
4. Restart Home Assistant.
5. Add **CBBO Waste Collection** from Settings → Devices & services.

## Updating from v0.1.0

The existing Mazzano configuration is migrated automatically. Entity IDs and automations are preserved.

## Disclaimer

This is an unofficial community integration and is not affiliated with CBBO. Always verify exceptional service changes against official CBBO communications.
