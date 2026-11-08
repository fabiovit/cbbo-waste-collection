# ♻️ CBBO Waste Collection

[![Release](https://img.shields.io/badge/release-v3.0.1-blue)](https://github.com/fabiovit/cbbo-waste-collection/releases)
[![Open in Home Assistant Marketplace](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=fabiovit&repository=cbbo-waste-collection&category=integration)
[![Validate](https://img.shields.io/github/actions/workflow/status/fabiovit/cbbo-waste-collection/validate.yml?branch=main&label=Validate)](https://github.com/fabiovit/cbbo-waste-collection/actions/workflows/validate.yml)
[![Hassfest](https://img.shields.io/github/actions/workflow/status/fabiovit/cbbo-waste-collection/hassfest.yml?branch=main&label=Hassfest)](https://github.com/fabiovit/cbbo-waste-collection/actions/workflows/hassfest.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**🇮🇹 Italiano** · [🇬🇧 English](#-english)

Integrazione custom per Home Assistant dedicata ai calendari della raccolta differenziata CBBO e alla nuova **Waste Center**.

> CBBO® e il relativo logo appartengono ai rispettivi proprietari. Questa è un'integrazione indipendente per Home Assistant e non è affiliata né approvata ufficialmente da CBBO.

## 🇮🇹 Italiano


### 🛍️ Novità v3.0.1 — Home Assistant Marketplace

- Installazione e aggiornamenti documentati per **Home Assistant 2026.11+ → Marketplace**.
- Collegamento diretto **Apri nel Marketplace**.
- Supporto alle installazioni precedenti: Home Assistant migra automaticamente le integrazioni installate tramite HACS.
- Nessuna modifica ai calendari, agli entity ID o alle configurazioni esistenti.

### 🧹 Novità v3.0.0

La 3.0 è una release di consolidamento: stessa esperienza per l'utente, ma base tecnica molto più pulita e facile da mantenere.

- codice Python riformattato e tipizzato;
- eliminati import wildcard, righe compresse e duplicazioni nelle entità;
- gestione cache/fallback separata in metodi chiari;
- frontend ripulito rimuovendo il vecchio meccanismo duplicato degli stili;
- suite test con nomi permanenti, senza file legati alle singole versioni;
- workflow GitHub semplificati e coerenti;
- nessuna modifica agli entity ID, ai Comuni configurati o ai calendari.

### ✨ Funzioni principali

- calendario raccolta differenziata;
- sensori Oggi, Domani e Prossimo ritiro;
- promemoria **“Stasera si espone”**;
- supporto a più Comuni / zone configurati;
- pannello Waste Center responsive desktop/mobile;
- interfaccia **Italiano / English**;
- nuova pagina **Centro di raccolta** con stato aperto/chiuso, orari di oggi, prossima apertura, settimana completa, indirizzo e modalità di accesso;
- gestione automatica degli orari stagionali per i Comuni che li prevedono;
- collegamento diretto alla pagina CBBO ufficiale;
- diagnostica, cache e fallback locale dei calendari.

### 🏘️ Comuni supportati

Acquafredda, Barbariga, Calvisano, Capriano del Colle, Carpenedolo, Castenedolo, Flero, Ghedi, Isorella, Mazzano, Montichiari, Montirone, Nuvolento, Nuvolera, Poncarale, Remedello, San Zeno Naviglio e Visano.

Mazzano supporta **Zona Nord** e **Zona Sud**.

### ♻️ Centro di raccolta

La v3.0.0 mantiene la pagina dedicata agli orari standard dei Centri di Raccolta CBBO.

La pagina mostra:

- **Aperto ora / Chiuso**;
- orari della giornata;
- prossima apertura;
- orari settimanali;
- periodo stagionale attivo;
- indirizzo;
- informazioni di accesso quando disponibili;
- avvisi per centri temporaneamente chiusi e centri alternativi;
- link alla pagina ufficiale CBBO.

Gli orari inclusi nella v3.0.0 sono stati verificati sulle pagine ufficiali CBBO il **19/08/2026**. Festività e chiusure straordinarie possono modificare gli orari standard: verificare sempre la pagina CBBO prima di partire.

### 👶 Tessili sanitari

Nella Waste Center la voce viene resa più esplicita:

**Tessili sanitari (pannolini e pannoloni)**.

In inglese:

**Sanitary waste (diapers & incontinence products)**.

### 📸 Screenshot

#### Panoramica
![CBBO Waste Collection - Panoramica](docs/screenshots/overview.png)

#### Comune
![CBBO Waste Collection - Comune](docs/screenshots/municipality.png)

### 📦 Installazione — Home Assistant Marketplace (2026.11+)

[![Open in Home Assistant Marketplace](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=fabiovit&repository=cbbo-waste-collection&category=integration)

1. Apri **Impostazioni → Marketplace** e accetta l'avviso iniziale, se richiesto.
2. Se il progetto non è già nel catalogo, scegli **Add from link** in alto a destra.
3. Collega il tuo account GitHub se richiesto: è necessario per i repository personalizzati.
4. Inserisci `https://github.com/fabiovit/cbbo-waste-collection` (oppure `fabiovit/cbbo-waste-collection`).
5. Se il tipo non viene riconosciuto, seleziona **Integration**; quindi scegli **Add**.
6. Apri **CBBO Waste Collection** nel Marketplace e seleziona **Install**.
7. Completa la configurazione in **Impostazioni → Dispositivi e servizi → Aggiungi integrazione**. Se Home Assistant richiede il riavvio, eseguilo.

**Aggiornamenti:** disponibili in **Impostazioni → Aggiornamenti**. Per i repository aggiunti da link è necessaria la connessione GitHub per verificare le nuove versioni.

**Hai già installato CBBO tramite HACS?** Passando a Home Assistant 2026.11 o successivo, il Marketplace migra automaticamente l'installazione: **non disinstallare e non riconfigurare CBBO**.

**Home Assistant 2026.10 o precedente:** continua a utilizzare HACS e aggiungi il repository come integrazione personalizzata.

Documentazione ufficiale: https://www.home-assistant.io/integrations/marketplace

### ☕ Supporta il progetto

Se CBBO Waste Collection ti è utile puoi supportarne lo sviluppo:

`https://ko-fi.com/fabvittori`

💡 **Idea originale:** Riccardo Cosi  
👨‍💻 **Sviluppo e manutenzione:** Fabio Vittori

---

## 🇬🇧 English

[🇮🇹 Italiano](#-italiano) · **🇬🇧 English**

Custom Home Assistant integration for CBBO waste collection calendars and the **Waste Center** dashboard.

> CBBO® and its logo belong to their respective owners. This is an independent Home Assistant integration and is not affiliated with or officially endorsed by CBBO.


### 🛍️ What's new in v3.0.1 — Home Assistant Marketplace

- Installation and updates documented for **Home Assistant 2026.11+ → Marketplace**.
- Direct **Open in Marketplace** link.
- Existing HACS installations migrate automatically when Home Assistant upgrades.
- No changes to calendars, entity IDs or existing configuration.

### 🧹 What’s new in v3.0.0

v3.0 is a consolidation release: the user experience stays familiar while the technical foundation is significantly cleaner and easier to maintain.

- Python code reformatted and typed;
- wildcard imports, compressed one-line code and entity duplication removed;
- cache/fallback handling split into clear methods;
- frontend cleanup removes the old duplicated style rebuild mechanism;
- permanent test names replace release-specific test files;
- simplified and consistent GitHub workflows;
- no changes to entity IDs, configured municipalities or collection calendars.

### ✨ Main features

- waste collection calendar;
- Today, Tomorrow and Next collection sensors;
- **“Put it out tonight”** reminder;
- support for multiple configured municipalities / zones;
- responsive Waste Center panel for desktop and mobile;
- **Italian / English** interface;
- new **Recycling Center** page with open/closed status, today's hours, next opening, weekly schedule, address and access information;
- automatic seasonal schedule selection where applicable;
- direct link to the official CBBO municipality page;
- diagnostics, cache and bundled calendar fallback.

### 🏘️ Supported municipalities

Acquafredda, Barbariga, Calvisano, Capriano del Colle, Carpenedolo, Castenedolo, Flero, Ghedi, Isorella, Mazzano, Montichiari, Montirone, Nuvolento, Nuvolera, Poncarale, Remedello, San Zeno Naviglio and Visano.

Mazzano supports **North Zone** and **South Zone**.

### ♻️ Recycling Center

Version 3.0.0 keeps the dedicated page for CBBO recycling-center standard opening hours.

It shows:

- **Open now / Closed**;
- today's hours;
- next opening;
- full weekly schedule;
- active seasonal period;
- address;
- access requirements when available;
- notices for temporarily closed centers and alternative locations;
- link to the official CBBO page.

The opening hours bundled with v3.0.0 were verified against official CBBO pages on **2026-08-19**. Public holidays and exceptional closures may change standard hours, so always check the official CBBO page before travelling.

### 👶 Sanitary waste

The Waste Center uses the clearer label:

**Sanitary waste (diapers & incontinence products)**.

Italian:

**Tessili sanitari (pannolini e pannoloni)**.

### 📸 Screenshots

#### Overview
![CBBO Waste Collection - Overview](docs/screenshots/overview.png)

#### Municipality
![CBBO Waste Collection - Municipality](docs/screenshots/municipality.png)

### 📦 Installation — Home Assistant Marketplace (2026.11+)

[![Open in Home Assistant Marketplace](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=fabiovit&repository=cbbo-waste-collection&category=integration)

1. Open **Settings → Marketplace** and accept the initial warning if prompted.
2. If this project is not listed in the catalog, choose **Add from link** in the top-right corner.
3. Connect your GitHub account if prompted (required for custom repositories).
4. Enter `https://github.com/fabiovit/cbbo-waste-collection` (or `fabiovit/cbbo-waste-collection`).
5. If the type is not detected, select **Integration**, then **Add**.
6. Open **CBBO Waste Collection** in the Marketplace and select **Install**.
7. Complete setup under **Settings → Devices & services → Add integration**. Restart Home Assistant if requested.

**Updates:** available under **Settings → Updates**. A GitHub connection is required to check for updates to repositories added from a link.

**Already installed via HACS?** Home Assistant 2026.11+ migrates existing HACS installations automatically: **do not uninstall or reconfigure CBBO**.

**Home Assistant 2026.10 or earlier:** continue using HACS and add the repository as a custom integration.

Official documentation: https://www.home-assistant.io/integrations/marketplace

### ☕ Support the project

If CBBO Waste Collection is useful to you, you can support its development:

`https://ko-fi.com/fabvittori`

💡 **Original idea:** Riccardo Cosi  
👨‍💻 **Development & maintenance:** Fabio Vittori
