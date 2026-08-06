# ♻️ CBBO Waste Collection

[![GitHub release](https://img.shields.io/github/v/release/fabiovit/cbbo-waste-collection)](https://github.com/fabiovit/cbbo-waste-collection/releases)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![Validate](https://github.com/fabiovit/cbbo-waste-collection/actions/workflows/validate.yml/badge.svg)](https://github.com/fabiovit/cbbo-waste-collection/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/fabiovit/cbbo-waste-collection)](LICENSE)

Custom integration for Home Assistant that exposes the public CBBO waste collection calendar as sensors, binary sensors and a calendar entity.

> **CBBO® e il relativo logo sono marchi dei rispettivi proprietari. Questa è un'integrazione indipendente per Home Assistant, non affiliata, sponsorizzata né approvata ufficialmente da CBBO.**

## Funzioni

- selezione del Comune tramite Config Flow;
- gestione della Zona Nord/Zona Sud per Mazzano;
- raccolte di oggi e domani;
- prossimo ritiro e giorni mancanti;
- avviso “esporre stasera”;
- calendario Home Assistant;
- aggiornamento automatico ogni 6 ore;
- cache locale dell'ultimo calendario valido;
- diagnostica scaricabile da Home Assistant;
- servizi per aggiornare i dati e svuotare la cache;
- traduzioni italiano e inglese.

## Comuni configurabili

Acquafredda, Barbariga, Calvisano, Capriano del Colle, Carpenedolo, Castenedolo, Flero, Ghedi, Isorella, Mazzano, Montichiari, Montirone, Nuvolento, Nuvolera, Poncarale, Remedello, San Zeno Naviglio e Visano.

## Installazione con HACS

1. Apri **HACS → Integrazioni → Repository personalizzati**.
2. Inserisci `https://github.com/fabiovit/cbbo-waste-collection` e scegli **Integration**.
3. Scarica **CBBO Waste Collection**.
4. Riavvia Home Assistant.
5. Apri **Impostazioni → Dispositivi e servizi → Aggiungi integrazione** e cerca **CBBO Waste Collection**.

## Entità

L'entity ID viene generato da Home Assistant usando il nome del dispositivo. Per Mazzano Zona Sud, ad esempio:

```text
sensor.differenziata_mazzano_zona_sud_rifiuti_oggi
sensor.differenziata_mazzano_zona_sud_rifiuti_domani
sensor.differenziata_mazzano_zona_sud_prossimo_ritiro
sensor.differenziata_mazzano_zona_sud_giorni_al_prossimo_ritiro
sensor.differenziata_mazzano_zona_sud_ultimo_aggiornamento
sensor.differenziata_mazzano_zona_sud_sorgente_dati
binary_sensor.differenziata_mazzano_zona_sud_ritiro_domani
binary_sensor.differenziata_mazzano_zona_sud_esporre_stasera
calendar.differenziata_mazzano_zona_sud_calendario_raccolta
```

## Servizi

### `cbbo_waste_collection.refresh`
Forza l'aggiornamento di tutte le configurazioni dell'integrazione.

### `cbbo_waste_collection.clear_cache`
Elimina la cache locale e forza un nuovo download. Usalo soltanto quando devi risolvere dati obsoleti o errati.

## Sorgente dati

Il sensore **Sorgente dati** può mostrare:

- `online`: calendario appena letto dal sito;
- `cache`: ultimo calendario valido salvato localmente;
- `memory`: dati mantenuti in memoria durante un errore temporaneo;
- `bundled_mazzano_2026`: fallback locale limitato a Mazzano 2026.

## Limiti

Il sito CBBO non pubblica un'API documentata per questa integrazione. Il parser interpreta i dati pubblici presenti nelle pagine comunali. Modifiche sostanziali al sito possono richiedere un aggiornamento dell'integrazione. La cache riduce l'impatto delle interruzioni temporanee.

## Segnalazioni

Per un calendario errato apri una issue includendo Comune, zona, data attesa, data mostrata e diagnostica dell'integrazione. Non pubblicare dati personali.

## Icona e identità visiva

Da Home Assistant 2026.3 l'integrazione include direttamente icona e logo locali. L'icona del progetto utilizza il simbolo universale del riciclo ♻️ e non il logo ufficiale CBBO.

## Credits

- 💡 Idea originale: Riccardo
- 👨‍💻 Sviluppo e manutenzione: Fabio Vittori
