# Changelog

## 2.4.0

- Aggiunta interfaccia Waste Center bilingue Italiano / English.
- Aggiunta nuova sezione Centro di raccolta / Recycling Center.
- Integrati gli orari standard dei Centri di Raccolta per tutti i 18 Comuni supportati.
- Stato dinamico Aperto ora / Chiuso, orari di oggi, prossima apertura e settimana completa.
- Gestione automatica degli orari stagionali di Barbariga e Mazzano.
- Gestiti gli avvisi di centro temporaneamente chiuso per Acquafredda e Nuvolento.
- Aggiunti indirizzo, informazioni di accesso e link alla fonte ufficiale CBBO.
- Migliorata la dicitura Tessili sanitari: pannolini e pannoloni / sanitary waste.
- README completamente bilingue IT/EN con screenshot reali.
- Suite GitHub resa stabile: Validate esegue solo tests/current per evitare vecchi test di release rimasti nel repository.
- Nessuna modifica agli entity ID esistenti o ai calendari di raccolta.

## 2.3.5

- Corretto definitivamente il Location Picker nella sezione Comune.
- Individuata la causa reale: gli aggiornamenti continui dello stato Home Assistant ricostruivano la vista mentre il menu era aperto.
- Lo stato aperto/chiuso del picker è ora persistente nel componente.
- Gli aggiornamenti ordinari di Home Assistant non ridisegnano più la sezione Comune mentre il picker è aperto.
- Il menu resta aperto fino alla selezione di un profilo o a un secondo tap sul trigger.
- Continuano a essere mostrati esclusivamente i profili CBBO già configurati dall'utente.
- Nessuna modifica ai calendari, entity ID o Config Entry.

## 2.3.4

- Corretto il Location Picker su iPhone/iOS.
- Il pannello dei Comuni non si richiude più subito dopo il tap di apertura.
- Rimosso il listener globale che intercettava il click sintetico di Safari/iOS.
- Il picker ora rimane aperto finché l'utente seleziona un profilo o ritocca il pulsante.
- Migliorato il comportamento touch e lo scrolling del menu su smartphone.
- Il menu continua a mostrare esclusivamente i profili CBBO già configurati.
- Nessuna modifica ai calendari, entity ID o Config Entry.

## 2.3.3

- Rifatta la selezione del Comune nella Waste Center.
- Rimossi i vecchi menu `<select>` nativi.
- Nuovo Location Picker moderno con apertura stabile e profilo attivo evidenziato.
- Vengono mostrati esclusivamente i Comuni e le zone già configurati dall'utente in Home Assistant.
- Il cambio profilo è immediato e viene ricordato localmente dalla dashboard.
- Migliorato il comportamento del selettore su desktop e mobile.
- Nessuna modifica ai calendari, alle Config Entry, agli entity ID o alla logica di raccolta.

## 2.3.1

- Restyling grafico della Waste Center senza modifiche alla logica dati.
- Icone dei rifiuti ingrandite in hero, riepiloghi, timeline e calendario.
- Badge delle tipologie più leggibili e visivamente distinti.
- Hero “Stasera si espone” più forte e immediato.
- Riepilogo prossimo ritiro più evidente.
- Timeline con icone grandi e maggiore gerarchia tipografica.
- Migliorata la leggibilità su mobile e nei temi chiaro/scuro.
- Struttura, menu, calendari, entity ID e configurazioni invariati.

## 2.3.0

- Corretta la validazione Hassfest: ordine delle chiavi del manifest conforme a Home Assistant.
- Aggiunto `CONFIG_SCHEMA` per dichiarare esplicitamente la configurazione solo tramite Config Flow.

- README e info HACS aggiornati alla release 2.3.0 con badge e documentazione coerenti.

- Aggiunti HACS Action e Hassfest con controlli su push, pull request, release e schedulazione giornaliera.
- Aggiunto controllo automatico di coerenza tra tag GitHub e versione del `manifest.json`.
- Aggiunta checklist di pubblicazione per ridurre errori di tag/release e rilevamento HACS.

- Nuovo Waste Center con shell grafica e geometria derivate da Inverter Dashboard v1.1.4.
- Testata sticky con hamburger mobile, icona, versione e sottotitolo.
- Menu interno orizzontale touch-friendly: Panoramica, Calendario, Comune, Diagnostica e Supporta il progetto.
- Panoramica completamente ridisegnata con hero “Stasera si espone”, prossimo ritiro, stato rapido e timeline.
- Calendario con rail visivo e agenda dei prossimi passaggi.
- Pagina Comune dedicata alla selezione del profilo e alle fonti CBBO.
- Diagnostica semplificata e separata dai dati quotidiani.
- Pagina Ko-fi dedicata, mantenendo Credits e disclaimer.
- Nessuna modifica a calendari, entity ID o configurazioni esistenti.

## 2.2.0

- Ridisegnata completamente la testata della dashboard CBBO in stile Home Assistant/PawBook.
- Rimosso il precedente hero verde.
- Aggiunto logo CBBO locale nell'header.
- Su mobile: hamburger a sinistra, logo e titolo compatti, versione e Ko-fi a destra.
- Separati i controlli (Comune/zona, sito CBBO e aggiornamento) dal branding.
- Migliorata la resa responsive e alleggerite ombre e bordi delle card.
- Nessuna modifica ai calendari, agli entity ID o alle configurazioni esistenti.

## 2.1.6

- Sostituito il precedente collegamento alla Dashboard con un vero pulsante hamburger `mdi:menu`.
- Su mobile il pulsante è posizionato in alto a sinistra nell'header CBBO, come in PawBook.
- Il pulsante apre direttamente il menu laterale di Home Assistant tramite l'evento `hass-toggle-menu`.
- Il pulsante resta nascosto su desktop.
- Nessuna modifica ai calendari, agli entity ID o alle configurazioni esistenti.

## 2.1.5

- Il pulsante per tornare alla Dashboard principale di Home Assistant viene ora mostrato solo su mobile.
- Su desktop il pulsante è nascosto perché la sidebar di Home Assistant è già disponibile.
- Nessuna modifica ai calendari, agli entity ID o alle configurazioni esistenti.

## 2.1.4

- Aggiunto nella dashboard laterale un pulsante rapido per tornare alla Dashboard principale di Home Assistant.
- Il pulsante utilizza l'icona `mdi:view-dashboard` ed è disponibile sia su desktop sia su mobile.
- Forzato il caricamento del nuovo frontend tramite nuovo web component e cache-busting.
- Nessuna modifica ai calendari, agli entity ID o alle configurazioni esistenti.

## 2.1.3

- Corretto definitivamente l'errore rosso mostrato nella sidebar quando un calendario locale 2026 o la cache forniscono dati validi.
- Il backend non espone più come errore attivo il fallimento del tentativo online quando è già attivo un fallback valido.
- Cambiato il nome del web component del pannello per forzare il caricamento del nuovo frontend anche nelle sessioni Home Assistant già aperte.
- Aggiornato `info.md` mostrato da HACS dalla vecchia dicitura "versione 2.0" a `2.1.3`.
- Nessuna modifica ai calendari, agli entity ID o alle configurazioni esistenti.

## 2.1.2

- Pulita la diagnostica della dashboard laterale.
- Quando un calendario locale 2026 viene caricato correttamente, il precedente errore del tentativo online non viene più mostrato in rosso nella dashboard.
- Aggiunto uno stato leggibile della sorgente: dati online, cache o calendario locale 2026.
- Gli errori tecnici restano disponibili nella diagnostica interna dell'integrazione.
- Nessuna modifica ai calendari, agli entity ID o alle configurazioni esistenti.

## 2.1.1

- Corretto il pannello CBBO nella barra laterale che in v2.1.0 poteva apparire completamente bianco.
- Il frontend viene ora registrato tramite il meccanismo `panel_custom` previsto da Home Assistant.
- Aggiunto cache-busting al modulo JavaScript del pannello per evitare il riutilizzo della versione 2.1.0 dal browser.
- Nessuna modifica ai calendari, agli entity ID o alle configurazioni esistenti.

## 2.1.0

- Aggiunta dashboard CBBO dedicata nella barra laterale di Home Assistant.
- Aggiunti pannelli per oggi, domani, prossimo ritiro, giorni mancanti e promemoria serale.
- Aggiunta vista delle prossime raccolte.
- Aggiunto selettore Comune/zona per installazioni con più configurazioni.
- Aggiunto aggiornamento manuale direttamente dalla dashboard.
- Aggiunti collegamenti rapidi al sito CBBO e a Ko-fi.
- Aggiunto endpoint WebSocket interno per alimentare il pannello senza dipendere dagli entity ID.
- Nessuna modifica agli entity ID o alle configurazioni esistenti.

## 2.0.2

- Corretti i calendari 2026 di Isorella, Montichiari, Montirone, Poncarale e San Zeno Naviglio.
- Aggiunti test di regressione per le date segnalate del 7, 8 e 10 agosto 2026.
- Aggiunto il supporto alle donazioni tramite Ko-fi e GitHub Funding.
- Nessuna modifica agli entity ID esistenti.

## 2.0.1

- Correzione completa dei profili 2026 dopo audit Comune per Comune sulle fonti CBBO ufficiali.
- Corretto Carpenedolo: venerdì solo vetro/lattine + tessili sanitari; organico spostato al sabato.
- Corretti Acquafredda, Calvisano, Capriano del Colle, Castenedolo, Flero, Montichiari e Nuvolera.
- Aggiunta matrice di regressione sul 7 agosto 2026 per tutti i 18 Comuni CBBO.
- Nessuna modifica agli entity ID o alle configurazioni esistenti.
- Credits invariati: idea originale di Riccardo Cosi.

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
