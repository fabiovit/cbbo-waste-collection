# ♻️ CBBO Waste Collection

[![GitHub release](https://img.shields.io/github/v/release/fabiovit/cbbo-waste-collection)](https://github.com/fabiovit/cbbo-waste-collection/releases)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![Validate](https://github.com/fabiovit/cbbo-waste-collection/actions/workflows/validate.yml/badge.svg)](https://github.com/fabiovit/cbbo-waste-collection/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/fabiovit/cbbo-waste-collection)](LICENSE)

Custom integration for Home Assistant that exposes CBBO waste collection calendars as sensors, binary sensors and a calendar entity.

> **CBBO® e il relativo logo sono marchi dei rispettivi proprietari. Questa è un'integrazione indipendente per Home Assistant, non affiliata, sponsorizzata né approvata ufficialmente da CBBO.**

## Versione 2.0

La versione 2.0 introduce un profilo calendario 2026 integrato per **tutti i 18 Comuni CBBO**. L'integrazione prova comunque prima a leggere i dati pubblicati online da CBBO; se il calendario della pagina non è disponibile in un formato interpretabile, utilizza cache, memoria o il profilo locale del Comune.

Questo evita l'errore `Calendario non riconosciuto nella pagina CBBO` e permette a ogni Comune supportato di essere configurato anche quando il calendario web è renderizzato dinamicamente.

## Funzioni

- configurazione tramite Config Flow;
- tutti i 18 Comuni CBBO;
- Zona Nord/Zona Sud per Mazzano;
- raccolte di oggi e domani;
- prossimo ritiro e giorni mancanti;
- binary sensor **Ritiro domani**;
- binary sensor **Esporre stasera**;
- calendario Home Assistant con eventi giornalieri;
- aggiornamento automatico ogni 6 ore;
- cache locale dell'ultimo calendario valido;
- fallback 2026 specifico per Comune;
- sensore **Sorgente dati**;
- sensore **Ultimo aggiornamento**;
- diagnostica scaricabile da Home Assistant;
- individuazione dell'Ecocalendario PDF pubblicato da CBBO;
- servizi `refresh` e `clear_cache`;
- traduzioni italiano e inglese;
- branding locale per Home Assistant 2026.3+.

## Comuni supportati

- Acquafredda
- Barbariga
- Calvisano
- Capriano del Colle
- Carpenedolo
- Castenedolo
- Flero
- Ghedi
- Isorella
- Mazzano
- Montichiari
- Montirone
- Nuvolento
- Nuvolera
- Poncarale
- Remedello
- San Zeno Naviglio
- Visano

> Barbariga è gestito da CBBO dal 1° giugno 2026; il profilo locale parte da tale data.

## Installazione con HACS

1. Apri **HACS → Integrazioni → Repository personalizzati**.
2. Inserisci `https://github.com/fabiovit/cbbo-waste-collection` e scegli **Integration**.
3. Scarica **CBBO Waste Collection**.
4. Riavvia Home Assistant.
5. Vai in **Impostazioni → Dispositivi e servizi → Aggiungi integrazione**.
6. Cerca **CBBO Waste Collection** e scegli il Comune.
7. Per Mazzano scegli anche **Zona Nord** o **Zona Sud**.

## Entità

Home Assistant genera gli entity ID usando il nome del dispositivo. Per Mazzano Zona Sud, ad esempio:

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

## Sorgente dati

Il sensore **Sorgente dati** consente di capire immediatamente quali dati sono in uso:

- `online`: calendario letto e riconosciuto dal sito CBBO;
- `cache`: ultimo calendario online valido salvato localmente;
- `memory`: ultimo dataset valido mantenuto in memoria durante un errore temporaneo;
- `bundled_<comune>_2026`: profilo 2026 integrato nell'integrazione per quel Comune.

Esempi:

```text
bundled_castenedolo_2026
bundled_ghedi_2026
bundled_mazzano_2026
```

La sorgente online ha sempre priorità sul fallback integrato.

## Ecocalendario PDF

Quando la pagina del Comune contiene il collegamento all'Ecocalendario ufficiale, l'integrazione lo rileva e lo riporta nella diagnostica (`ecocalendar_pdf`). Questo è utile per confrontare rapidamente eventuali variazioni straordinarie.

## Servizi

### `cbbo_waste_collection.refresh`
Forza l'aggiornamento di tutte le configurazioni.

### `cbbo_waste_collection.clear_cache`
Elimina la cache locale e forza un nuovo tentativo di download. Non elimina il profilo locale 2026 incluso nell'integrazione.

## Audit dei profili 2026

Dalla versione **2.0.1** i profili locali sono accompagnati da test di regressione Comune per Comune. Il file [`AUDIT_2026.md`](AUDIT_2026.md) riporta la matrice di controllo usata per il 7 agosto 2026 e le correzioni effettuate dopo la 2.0.0.

## Note sui calendari

I profili integrati rappresentano i calendari e gli schemi di raccolta 2026 pubblicati da CBBO e servono da fallback quando la pagina online non è interpretabile dal client Home Assistant. **Le variazioni eccezionali legate a festività, recuperi o comunicazioni straordinarie possono essere aggiornate da CBBO durante l'anno:** quando disponibili, i dati online hanno quindi sempre la precedenza.

Se rilevi una data errata, apri una issue indicando Comune, data, raccolta attesa, raccolta mostrata e diagnostica dell'integrazione.

## Icona e identità visiva

L'integrazione include direttamente icona e logo locali. L'icona del progetto utilizza il simbolo universale del riciclo ♻️ e non il logo ufficiale CBBO.


## 🖥️ Dashboard dedicata nella barra laterale

Dalla versione **2.1.1**, CBBO Waste Collection aggiunge automaticamente una voce
**♻️ CBBO Waste Collection** nella barra laterale di Home Assistant.

La dashboard mostra rifiuti di oggi e domani, prossimo ritiro, giorni mancanti,
promemoria serale, prossime raccolte, sorgente dati e ultimo aggiornamento.
Con più Comuni configurati compare un selettore Comune/zona.

Sono inclusi anche aggiornamento manuale e collegamenti rapidi a CBBO e Ko-fi.
Non è richiesta alcuna configurazione Lovelace aggiuntiva.

## ☕ Supporta il progetto

CBBO Waste Collection è gratuito e open source.

Se trovi utile l'integrazione e vuoi contribuire al suo sviluppo e alla sua manutenzione, puoi offrirmi un caffè su Ko-fi:

https://ko-fi.com/fabvittori

## Credits

- 💡 Idea originale: Riccardo Cosi
- 👨‍💻 Sviluppo e manutenzione: Fabio Vittori
