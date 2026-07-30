# CBBO Waste Collection

Custom integration Home Assistant per la raccolta differenziata di Mazzano (CBBO), con scelta Zona Nord/Sud.

## Installazione manuale

1. Copia `custom_components/cbbo_waste_collection` in `/config/custom_components/`.
2. Riavvia Home Assistant.
3. Vai in **Impostazioni → Dispositivi e servizi → Aggiungi integrazione**.
4. Cerca **CBBO Waste Collection** e scegli la zona.

## Entità

- Rifiuti oggi
- Rifiuti domani
- Prossimo ritiro
- Giorni al prossimo ritiro
- Ritiro domani
- Esporre stasera
- Calendario raccolta

## Fonte

Ecocalendario ufficiale CBBO Mazzano 2026. I rifiuti vanno esposti dalle 22:00 della sera precedente ed entro le 05:00 del giorno di raccolta.

## Stato della versione 0.1.0

Prima versione dedicata a Mazzano. La logica annuale è inclusa localmente e non dipende dalla disponibilità del sito durante l'uso. Le variazioni eccezionali comunicate da CBBO richiederanno un aggiornamento del componente.
