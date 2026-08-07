# Changelog

## 2.0.0

- Supporto operativo a tutti i 18 Comuni CBBO tramite profili calendario 2026 integrati.
- La sorgente online resta prioritaria; fallback automatico su cache, memoria e profilo locale del Comune.
- Rimossi i fallback separati di Mazzano e Castenedolo in favore di un unico motore `bundled_2026`.
- Mantenuta la gestione Zona Nord/Zona Sud per Mazzano.
- Aggiunto supporto a Barbariga dal 1° giugno 2026.
- Aggiornati gli schemi 2026 di Acquafredda, Calvisano, Capriano del Colle, Carpenedolo, Castenedolo, Flero, Ghedi, Isorella, Mazzano, Montichiari, Montirone, Nuvolento, Nuvolera, Poncarale, Remedello, San Zeno Naviglio e Visano.
- Cache schema aggiornata alla versione 2 e Config Flow alla versione 3.
- Diagnostica mantiene sorgente dati, ultimo errore e link Ecocalendario PDF.
- Nessuna modifica agli entity ID esistenti.
- Credits: idea originale di Riccardo Cosi.

## 1.0.2

- Aggiunto fallback 2026 per Castenedolo basato sull'Ecocalendario CBBO ufficiale.
- Aggiunta scoperta automatica del link all'Ecocalendario PDF nelle pagine dei Comuni.
- Aggiunto `ecocalendar_pdf` alla diagnostica e al sensore sorgente dati.
- Gli eventi calendario sono ora veri eventi giornalieri (all-day).
- Credits aggiornati: idea originale di Riccardo Cosi.
- Nessuna modifica agli entity ID esistenti.

## 1.0.1

- Aggiunte icona e logo locali per Home Assistant 2026.3 e versioni successive.
- Aggiunte varianti per tema chiaro, tema scuro e display ad alta densità.
- Nessuna modifica agli entity ID o alla configurazione esistente.

## 1.0.0

- Prima release stabile.
- Configurazione dei 18 Comuni CBBO.
- Zona Nord/Sud per Mazzano.
- Sensori, binary sensor e calendario.
- Cache locale e diagnostica.
- Servizi `refresh` e `clear_cache`.
- Traduzioni italiano e inglese.
- Test del parser e workflow GitHub Actions.
- README, template issue/PR, linee guida e credits.
