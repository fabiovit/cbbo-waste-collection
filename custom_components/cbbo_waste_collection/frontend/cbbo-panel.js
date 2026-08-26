const CBBO_PANEL_VERSION = "3.0.0";

const WASTE_META = {
  organic:   { icon:"mdi:food-apple-outline", it:"Frazione organica", en:"Organic waste", cls:"organic" },
  paper:     { icon:"mdi:package-variant-closed", it:"Carta e cartone", en:"Paper & cardboard", cls:"paper" },
  plastic:   { icon:"mdi:bottle-soda-outline", it:"Imballaggi in plastica", en:"Plastic packaging", cls:"plastic" },
  glass_cans:{ icon:"mdi:glass-mug-variant", it:"Vetro e lattine", en:"Glass & cans", cls:"glass" },
  residual:  { icon:"mdi:delete-outline", it:"Rifiuti non differenziabili", en:"Residual waste", cls:"residual" },
  sanitary:  { icon:"mdi:medical-bag", it:"Tessili sanitari (pannolini e pannoloni)", en:"Sanitary waste (diapers & incontinence products)", cls:"sanitary" },
  green:     { icon:"mdi:leaf", it:"Verde", en:"Green waste", cls:"green" },
};

const I18N = {
  it: {
    overview:"Panoramica", calendar:"Calendario", municipality:"Comune", center:"Centro di raccolta", diagnostics:"Diagnostica",
    support:"Supporta il progetto", loading:"Caricamento…", updating:"Aggiornamento in corso…", retry:"Riprova",
    noMunicipality:"Nessun Comune configurato", addIntegration:"Aggiungi CBBO Waste Collection da Impostazioni → Dispositivi e servizi.",
    loadError:"Impossibile caricare i dati", tryAgain:"Riprova tra qualche secondo.",
    headline:"La differenziata, a colpo d’occhio.", headlineSub:"Quello che serve sapere oggi, domani e per il prossimo passaggio.",
    expose:"Stasera si espone", nothingTonight:"Oggi non devi esporre nulla", exposeReminder:"Promemoria esposizione", allQuiet:"Tutto tranquillo",
    prepareTomorrow:"Per la raccolta di domani prepara: {waste}.", noTomorrow:"Nessun ritiro previsto domani. Puoi controllare il prossimo passaggio qui sotto.",
    nextCollection:"Prossimo ritiro", day:"giorno", days:"giorni", untilCollection:"al passaggio", refreshData:"Aggiorna dati",
    openCalendar:"Apri calendario", wasteToday:"Rifiuti oggi", wasteTomorrow:"Rifiuti domani", putOutTonight:"Esporre stasera",
    yes:"Sì", no:"No", prepareBins:"Prepara i contenitori", noExposure:"Nessuna esposizione", source:"Sorgente",
    upcoming:"Prossime raccolte", agenda:"Agenda", nextPassage:"prossimo passaggio", noEvents:"Nessun evento disponibile",
    calendarTitle:"I prossimi passaggi.", calendarSub:"Una lettura più visiva della settimana e dell'agenda di raccolta.",
    sevenCollections:"Sette prossime raccolte", fullAgenda:"Agenda completa",
    areaTitle:"La tua zona di raccolta.", areaSub:"Passa rapidamente tra i profili CBBO già configurati in Home Assistant.",
    activeProfile:"Profilo attivo", municipalityZone:"Comune / zona", configuredProfiles:"{count} profili CBBO configurati. Tocca il profilo attivo per cambiarlo.",
    oneProfile:"È configurato un solo profilo CBBO.", officialCbbo:"Pagina CBBO di {name}", officialCalendar:"Ecocalendario ufficiale",
    refreshNow:"Aggiorna ora", profileInfo:"La Waste Center mostra solo i Comuni e le zone che hai già configurato nell’integrazione CBBO.",
    diagTitle:"Dati chiari, senza rumore.", diagSub:"Le informazioni tecniche utili per capire da dove arriva il calendario e quando è stato aggiornato.",
    dataSource:"Sorgente dati", lastUpdate:"Ultimo aggiornamento", autoUpdate:"Aggiornamento automatico ogni 6 ore", integrationVersion:"Versione integrazione",
    lastError:"Ultimo errore", localCalendar:"Calendario locale 2026", cachedData:"Dati in cache", onlineData:"Dati online",
    supportTitle:"Supporta il progetto.", supportSub:"CBBO Waste Collection è gratuito e open source.",
    useful:"Ti è utile?", coffee:"Offrimi un caffè. ☕", supportText:"Il supporto aiuta a mantenere l'integrazione aggiornata, verificare i calendari dei Comuni e continuare a migliorarne l'esperienza su Home Assistant.",
    supportKofi:"Supporta su Ko-fi", credits:"💡 Idea originale: Riccardo Cosi<br>👨‍💻 Sviluppo e manutenzione: Fabio Vittori",
    disclaimer:"CBBO® e il relativo logo appartengono ai rispettivi proprietari. Progetto indipendente non affiliato né approvato ufficialmente da CBBO.",
    noCollection:"Nessun ritiro",
    centerEyebrow:"Centro di raccolta", centerTitle:"Isola ecologica, senza sorprese.", centerSub:"Orari standard, stato attuale e prossima apertura per il Comune selezionato.",
    openNow:"Aperto ora", closedNow:"Chiuso", closesAt:"Chiude alle {time}", opensAt:"Apre alle {time}", nextOpen:"Prossima apertura",
    todayHours:"Orari di oggi", weeklyHours:"Orari settimanali", address:"Indirizzo", access:"Accesso", officialSource:"Fonte ufficiale CBBO",
    closed:"Chiuso", standardHours:"Orari standard", verified:"Dati verificati il {date}", holidayWarning:"Gli orari possono variare in caso di festività o chiusure straordinarie. Verifica sempre la pagina CBBO prima di partire.",
    mon:"Lunedì", tue:"Martedì", wed:"Mercoledì", thu:"Giovedì", fri:"Venerdì", sat:"Sabato", sun:"Domenica",
    tomorrow:"Domani", language:"Lingua"
  },
  en: {
    overview:"Overview", calendar:"Calendar", municipality:"Municipality", center:"Recycling Center", diagnostics:"Diagnostics",
    support:"Support the project", loading:"Loading…", updating:"Updating…", retry:"Retry",
    noMunicipality:"No municipality configured", addIntegration:"Add CBBO Waste Collection from Settings → Devices & services.",
    loadError:"Unable to load data", tryAgain:"Try again in a few seconds.",
    headline:"Waste collection, at a glance.", headlineSub:"Everything you need for today, tomorrow and the next collection.",
    expose:"Put it out tonight", nothingTonight:"Nothing to put out today", exposeReminder:"Collection reminder", allQuiet:"All clear",
    prepareTomorrow:"Prepare for tomorrow: {waste}.", noTomorrow:"No collection is scheduled for tomorrow. Check the next collection below.",
    nextCollection:"Next collection", day:"day", days:"days", untilCollection:"until collection", refreshData:"Refresh data",
    openCalendar:"Open calendar", wasteToday:"Today", wasteTomorrow:"Tomorrow", putOutTonight:"Put out tonight",
    yes:"Yes", no:"No", prepareBins:"Prepare the containers", noExposure:"Nothing to put out", source:"Source",
    upcoming:"Upcoming collections", agenda:"Schedule", nextPassage:"next collection", noEvents:"No events available",
    calendarTitle:"Upcoming collections.", calendarSub:"A visual view of the next week and collection schedule.",
    sevenCollections:"Next seven collections", fullAgenda:"Full schedule",
    areaTitle:"Your collection area.", areaSub:"Quickly switch between CBBO profiles already configured in Home Assistant.",
    activeProfile:"Active profile", municipalityZone:"Municipality / zone", configuredProfiles:"{count} CBBO profiles configured. Tap the active profile to switch.",
    oneProfile:"Only one CBBO profile is configured.", officialCbbo:"CBBO page for {name}", officialCalendar:"Official Eco-calendar",
    refreshNow:"Refresh now", profileInfo:"Waste Center only shows municipalities and zones you have already configured in the CBBO integration.",
    diagTitle:"Clear data, no noise.", diagSub:"Technical information about the calendar source and its latest update.",
    dataSource:"Data source", lastUpdate:"Last update", autoUpdate:"Automatic update every 6 hours", integrationVersion:"Integration version",
    lastError:"Last error", localCalendar:"Local 2026 calendar", cachedData:"Cached data", onlineData:"Online data",
    supportTitle:"Support the project.", supportSub:"CBBO Waste Collection is free and open source.",
    useful:"Finding it useful?", coffee:"Buy me a coffee. ☕", supportText:"Your support helps keep the integration updated, verify municipality calendars and continue improving the Home Assistant experience.",
    supportKofi:"Support on Ko-fi", credits:"💡 Original idea: Riccardo Cosi<br>👨‍💻 Development & maintenance: Fabio Vittori",
    disclaimer:"CBBO® and its logo belong to their respective owners. Independent project, not affiliated with or officially endorsed by CBBO.",
    noCollection:"No collection",
    centerEyebrow:"Recycling Center", centerTitle:"Recycling center, without surprises.", centerSub:"Standard opening hours, current status and next opening for the selected municipality.",
    openNow:"Open now", closedNow:"Closed", closesAt:"Closes at {time}", opensAt:"Opens at {time}", nextOpen:"Next opening",
    todayHours:"Today's hours", weeklyHours:"Weekly hours", address:"Address", access:"Access", officialSource:"Official CBBO source",
    closed:"Closed", standardHours:"Standard hours", verified:"Data verified on {date}", holidayWarning:"Hours may change on holidays or during exceptional closures. Always check the CBBO page before travelling.",
    mon:"Monday", tue:"Tuesday", wed:"Wednesday", thu:"Thursday", fri:"Friday", sat:"Saturday", sun:"Sunday",
    tomorrow:"Tomorrow", language:"Language"
  }
};

const PANEL_STYLES = `
:host{display:block;min-height:100vh;background:var(--primary-background-color);color:var(--primary-text-color);font-family:var(--paper-font-body1_-_font-family,Roboto,Arial,sans-serif);--cbbo:#68a82d;--cbbo-deep:#4d8720;--paper:#4f9ad5;--plastic:#eabf2d;--organic:#72b743;--glass:#49abc5;--residual:#6d7278;--sanitary:#8f7ad6;--green:#4ba85c;--orange:#df7b34}*{box-sizing:border-box}button,select{font:inherit}.app{width:100%;min-height:100vh;padding:0 0 56px}.topbar{--casa-accent:var(--cbbo);position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--primary-background-color) 96%,transparent);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid color-mix(in srgb,var(--divider-color) 78%,transparent);box-shadow:0 10px 28px color-mix(in srgb,#000 4%,transparent)}.topbar-main{max-width:1480px;margin:auto;min-height:72px;padding:15px 18px 9px;display:flex;align-items:center;gap:12px}.menu-btn{display:none;border:0;background:transparent;color:var(--primary-text-color);width:42px;height:42px;border-radius:13px;align-items:center;justify-content:center;cursor:pointer;flex:none}.menu-btn ha-icon{--mdc-icon-size:27px}.menu-btn:active{background:var(--secondary-background-color)}.app-identity{display:flex;align-items:center;gap:11px;min-width:0}.app-icon{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;flex:none;border:1px solid color-mix(in srgb,var(--cbbo) 30%,var(--divider-color));background:color-mix(in srgb,var(--cbbo) 9%,var(--card-background-color));overflow:hidden}.app-icon img{width:34px;height:34px;object-fit:contain}.brand{min-width:0}.brand-line{display:flex;align-items:center;gap:8px;min-width:0}.brand-title{font-size:21px;line-height:1.05;font-weight:850;letter-spacing:-.025em}.version-badge{display:inline-flex;align-items:center;justify-content:center;padding:3px 7px;border-radius:999px;border:1px solid color-mix(in srgb,var(--cbbo) 30%,var(--divider-color));background:color-mix(in srgb,var(--cbbo) 9%,var(--card-background-color));color:var(--cbbo-deep);font-size:9px;font-weight:900;line-height:1;white-space:nowrap}.brand-subtitle{font-size:11px;color:var(--secondary-text-color);margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.nav-scroller{max-width:1480px;margin:auto;overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;scrollbar-width:none;touch-action:pan-x;padding:0 18px}.nav-scroller::-webkit-scrollbar{display:none}.nav{display:flex;align-items:stretch;gap:22px;width:max-content;min-width:max-content}.nav-btn{position:relative;border:0;background:transparent;color:var(--secondary-text-color);padding:10px 1px 12px;min-height:44px;display:flex;align-items:center;gap:7px;cursor:pointer;white-space:nowrap;font-size:12px;font-weight:720;transition:color .16s ease,transform .12s ease;-webkit-tap-highlight-color:transparent;user-select:none}.nav-btn::after{content:"";position:absolute;left:50%;right:50%;bottom:0;height:3px;border-radius:3px 3px 0 0;background:var(--cbbo);opacity:0;transition:left .18s ease,right .18s ease,opacity .18s ease}.nav-btn ha-icon{--mdc-icon-size:19px;opacity:.78}.nav-btn:active{transform:translateY(1px)}.nav-btn.active{color:var(--cbbo-deep);font-weight:850}.nav-btn.active ha-icon{opacity:1;color:var(--cbbo)}.nav-btn.active::after{left:0;right:0;opacity:1}.support-nav{color:color-mix(in srgb,var(--cbbo) 85%,var(--primary-text-color))}
main{width:min(1480px,100%);margin:auto;padding:22px 22px 0}.footer{width:min(1480px,100%);margin:34px auto 0;padding:0 22px;text-align:center;color:var(--secondary-text-color);font-size:10px}.eyebrow{font-size:10px;font-weight:850;letter-spacing:.18em;text-transform:uppercase;color:var(--secondary-text-color);margin-bottom:8px}.view-head{margin:4px 0 24px}.view-head h1{margin:0;font-size:34px;line-height:1.04;letter-spacing:-.04em}.view-head p{margin:7px 0 0;color:var(--secondary-text-color);max-width:760px}
.hero{position:relative;overflow:hidden;border-radius:32px;border:1px solid var(--divider-color);background:linear-gradient(135deg,color-mix(in srgb,var(--cbbo) 11%,var(--card-background-color)),var(--card-background-color) 44%,color-mix(in srgb,var(--orange) 5%,var(--card-background-color)));min-height:340px;padding:36px;display:grid;grid-template-columns:minmax(0,1.25fr) minmax(310px,.75fr);gap:32px;align-items:center}.hero:before{content:"";position:absolute;width:430px;height:430px;border-radius:50%;right:-180px;top:-220px;border:72px solid color-mix(in srgb,var(--cbbo) 8%,transparent)}.hero-copy,.hero-side{position:relative;z-index:1}.hero-kicker{display:inline-flex;align-items:center;gap:8px;padding:7px 11px;border-radius:999px;background:color-mix(in srgb,var(--cbbo) 10%,var(--card-background-color));border:1px solid color-mix(in srgb,var(--cbbo) 25%,var(--divider-color));color:var(--cbbo-deep);font-size:10px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}.hero-copy h1{font-size:56px;line-height:.98;letter-spacing:-.055em;margin:18px 0 10px;max-width:780px}.hero-copy p{font-size:15px;color:var(--secondary-text-color);margin:0;max-width:680px}.waste-tokens{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}.waste-token{display:inline-flex;align-items:center;gap:12px;padding:14px 16px;border-radius:18px;border:1px solid color-mix(in srgb,var(--divider-color) 78%,transparent);background:color-mix(in srgb,var(--card-background-color) 94%,transparent);font-size:14px;font-weight:780;box-shadow:0 4px 14px color-mix(in srgb,#000 4%,transparent)}.waste-token ha-icon{--mdc-icon-size:42px}.waste-token.organic{color:var(--organic)}.waste-token.paper{color:var(--paper)}.waste-token.plastic{color:#ad8700}.waste-token.glass{color:var(--glass)}.waste-token.residual{color:var(--residual)}.waste-token.sanitary{color:var(--sanitary)}.waste-token.green{color:var(--green)}.hero-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:25px}.action-btn{border:1px solid var(--divider-color);background:var(--card-background-color);color:var(--primary-text-color);border-radius:15px;padding:12px 15px;display:inline-flex;gap:8px;align-items:center;cursor:pointer;text-decoration:none;font-size:12px;font-weight:800}.action-btn.primary{background:var(--cbbo-deep);color:white;border-color:transparent}.action-btn ha-icon{--mdc-icon-size:19px}.hero-side{display:grid;gap:12px}.next-orbit{border-radius:28px;background:color-mix(in srgb,var(--primary-background-color) 45%,transparent);border:1px solid color-mix(in srgb,var(--divider-color) 85%,transparent);padding:25px;backdrop-filter:blur(8px)}.next-orbit span{display:block;font-size:9px;font-weight:900;letter-spacing:.15em;text-transform:uppercase;color:var(--secondary-text-color)}.next-orbit strong{display:block;font-size:27px;line-height:1.05;margin-top:10px;letter-spacing:-.025em}.next-orbit small{display:block;margin-top:7px;color:var(--secondary-text-color);font-size:11px}.day-count{display:flex;align-items:end;gap:10px;margin-top:18px}.day-count b{font-size:58px;line-height:.8;color:var(--cbbo-deep);letter-spacing:-.06em}.day-count em{font-style:normal;color:var(--secondary-text-color);font-size:12px}.status-strip{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--divider-color);border-radius:25px;overflow:hidden;margin-top:14px;background:var(--card-background-color)}.status-item{padding:20px 22px;border-right:1px solid var(--divider-color)}.status-item:last-child{border-right:0}.status-item span{display:block;font-size:9px;font-weight:850;letter-spacing:.12em;text-transform:uppercase;color:var(--secondary-text-color)}.status-item strong{display:block;font-size:18px;margin-top:8px}.status-item small{display:block;color:var(--secondary-text-color);font-size:10px;margin-top:4px}.status-item.good strong{color:var(--cbbo-deep)}
.schedule-stage{margin-top:28px;border-radius:30px;border:1px solid var(--divider-color);background:var(--card-background-color);overflow:hidden}.stage-head{padding:25px 28px 19px;display:flex;align-items:end;justify-content:space-between;gap:18px}.stage-head h2{margin:0;font-size:24px;letter-spacing:-.03em}.stage-head p{margin:5px 0 0;color:var(--secondary-text-color);font-size:12px}.timeline{display:grid}.timeline-row{display:grid;grid-template-columns:170px 1fr auto;gap:20px;align-items:center;padding:17px 28px;border-top:1px solid var(--divider-color)}.timeline-date{font-size:12px;font-weight:800;text-transform:capitalize}.timeline-date small{display:block;margin-top:4px;color:var(--secondary-text-color);font-weight:500}.timeline-main strong{display:block;font-size:17px;line-height:1.25}.timeline-dots{display:flex;gap:9px;flex-wrap:wrap}.waste-dot{width:48px;height:48px;border-radius:15px;display:grid;place-items:center;border:1px solid color-mix(in srgb,var(--divider-color) 78%,transparent);background:var(--secondary-background-color);box-shadow:0 3px 10px color-mix(in srgb,#000 4%,transparent)}.waste-dot ha-icon{--mdc-icon-size:30px}.waste-dot.organic{color:var(--organic)}.waste-dot.paper{color:var(--paper)}.waste-dot.plastic{color:#ad8700}.waste-dot.glass{color:var(--glass)}.waste-dot.residual{color:var(--residual)}.waste-dot.sanitary{color:var(--sanitary)}.waste-dot.green{color:var(--green)}
.calendar-hero{border-radius:30px;border:1px solid var(--divider-color);background:var(--card-background-color);padding:28px}.month-rail{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:22px}.rail-day{min-height:128px;border-radius:18px;background:var(--secondary-background-color);border:1px solid color-mix(in srgb,var(--divider-color) 75%,transparent);padding:14px}.rail-day.today{border-color:color-mix(in srgb,var(--cbbo) 55%,var(--divider-color));background:color-mix(in srgb,var(--cbbo) 7%,var(--card-background-color))}.rail-day span{font-size:9px;text-transform:uppercase;letter-spacing:.08em;color:var(--secondary-text-color);font-weight:800}.rail-day b{display:block;font-size:21px;margin-top:4px}.rail-dots{display:flex;gap:4px;flex-wrap:wrap;margin-top:16px}.rail-dots .waste-dot{width:40px;height:40px;border-radius:12px}.rail-dots .waste-dot ha-icon{--mdc-icon-size:25px}
.control-deck{display:grid;grid-template-columns:1.2fr .8fr;gap:14px}.control-panel,.info-panel,.support-stage{border-radius:28px;border:1px solid var(--divider-color);background:var(--card-background-color);padding:28px}.control-panel label{display:block;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--secondary-text-color);font-weight:850;margin-bottom:9px}.select{width:100%;min-height:48px;border:1px solid var(--divider-color);border-radius:15px;background:var(--secondary-background-color);color:var(--primary-text-color);padding:0 14px}.link-stack{display:grid;gap:9px;margin-top:20px}.wide-link{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:15px 16px;border:1px solid var(--divider-color);border-radius:16px;text-decoration:none;color:var(--primary-text-color);background:var(--secondary-background-color);font-size:12px;font-weight:800}.wide-link ha-icon{--mdc-icon-size:20px;color:var(--cbbo)}.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--divider-color);border:1px solid var(--divider-color);border-radius:23px;overflow:hidden}.info-cell{background:var(--card-background-color);padding:22px}.info-cell span{display:block;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--secondary-text-color);font-weight:850}.info-cell strong{display:block;font-size:17px;margin-top:8px;word-break:break-word}.info-cell small{display:block;color:var(--secondary-text-color);margin-top:5px;font-size:10px}.support-stage{min-height:340px;display:grid;grid-template-columns:1fr 250px;align-items:center;gap:28px;background:linear-gradient(145deg,color-mix(in srgb,var(--cbbo) 9%,var(--card-background-color)),var(--card-background-color))}.support-stage h1{font-size:44px;letter-spacing:-.045em;margin:0}.support-stage p{color:var(--secondary-text-color);max-width:650px;line-height:1.6}.coffee-orb{width:210px;height:210px;border-radius:50%;margin:auto;display:grid;place-items:center;background:color-mix(in srgb,var(--cbbo) 10%,var(--secondary-background-color));border:1px solid color-mix(in srgb,var(--cbbo) 30%,var(--divider-color));font-size:78px}.credits{margin-top:20px;color:var(--secondary-text-color);font-size:11px;line-height:1.8}
.empty-state{padding:80px 24px;text-align:center}.empty-state ha-icon{--mdc-icon-size:52px;color:var(--cbbo)}.empty-state h2{font-size:28px}.empty-state p{color:var(--secondary-text-color)}
@media(max-width:980px){.hero{grid-template-columns:1fr}.status-strip{grid-template-columns:1fr 1fr}.status-item:nth-child(2){border-right:0}.status-item:nth-child(-n+2){border-bottom:1px solid var(--divider-color)}.month-rail{grid-template-columns:repeat(4,1fr)}.control-deck{grid-template-columns:1fr}.support-stage{grid-template-columns:1fr}}
@media(max-width:620px){.waste-token{width:100%;padding:13px 14px}.waste-token ha-icon{--mdc-icon-size:40px}.waste-dot{width:44px;height:44px}.waste-dot ha-icon{--mdc-icon-size:28px}.rail-dots .waste-dot{width:38px;height:38px}.rail-dots .waste-dot ha-icon{--mdc-icon-size:24px}.app{padding:0 0 42px}.menu-btn{display:flex}.topbar-main{min-height:62px;padding:9px 10px 7px;gap:7px}.app-identity{gap:8px}.app-icon{width:39px;height:39px;border-radius:12px}.app-icon img{width:30px;height:30px}.brand-title{font-size:19px}.brand-subtitle{font-size:10px;margin-top:3px}.version-badge{font-size:8px;padding:3px 6px}.nav-scroller{padding:0 10px}.nav{gap:18px}.nav-btn{padding:9px 1px 11px;font-size:12px;min-height:42px}.nav-btn ha-icon{--mdc-icon-size:18px}main{padding:12px 10px 0}.footer{padding:0 10px}.hero{padding:23px 19px;border-radius:26px;min-height:auto}.hero-copy h1{font-size:39px}.hero-side{gap:9px}.next-orbit{padding:21px}.next-orbit strong{font-size:24px}.status-strip{grid-template-columns:1fr 1fr;border-radius:22px}.status-item{padding:17px 16px}.status-item strong{font-size:15px}.stage-head{padding:21px 19px 15px}.timeline-row{grid-template-columns:1fr auto;padding:15px 19px;gap:12px}.timeline-main{grid-column:1/-1;grid-row:2}.month-rail{grid-template-columns:repeat(2,1fr);gap:7px}.rail-day{min-height:115px}.control-panel,.info-panel,.support-stage,.calendar-hero{padding:21px 18px;border-radius:24px}.info-grid{grid-template-columns:1fr}.support-stage h1{font-size:36px}.coffee-orb{width:150px;height:150px;font-size:58px}.view-head h1{font-size:29px}}
.status-item small{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.status-item small .waste-dot{width:42px;height:42px;border-radius:13px}.status-item small .waste-dot ha-icon{--mdc-icon-size:27px}.next-orbit{border-radius:26px!important}.next-orbit strong{font-size:28px!important;line-height:1.05}.day-count b{font-size:46px!important}.hero-side .next-orbit{box-shadow:0 10px 26px color-mix(in srgb,#000 5%,transparent)}
.location-picker{position:relative;margin-top:8px}
.location-picker-trigger{
  width:100%;display:flex;align-items:center;gap:14px;
  padding:14px 16px;border-radius:18px;
  border:1px solid color-mix(in srgb,var(--divider-color) 78%,transparent);
  background:color-mix(in srgb,var(--card-background-color) 96%,transparent);
  color:var(--primary-text-color);cursor:pointer;text-align:left;
  box-shadow:0 6px 20px color-mix(in srgb,#000 5%,transparent);
  transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease;
}
.location-picker-trigger:hover{
  border-color:color-mix(in srgb,var(--primary-color) 42%,var(--divider-color));
  box-shadow:0 9px 24px color-mix(in srgb,#000 7%,transparent)
}
.location-picker-trigger:active{transform:scale(.992)}
.location-picker-icon{
  width:48px;height:48px;border-radius:15px;display:grid;place-items:center;
  background:color-mix(in srgb,var(--primary-color) 12%,var(--secondary-background-color));
  color:var(--primary-color);flex:0 0 auto
}
.location-picker-icon ha-icon{--mdc-icon-size:27px}
.location-picker-copy{min-width:0;flex:1}
.location-picker-copy small{
  display:block;font-size:11px;font-weight:800;letter-spacing:.09em;
  text-transform:uppercase;color:var(--secondary-text-color);margin-bottom:4px
}
.location-picker-copy strong{
  display:block;font-size:17px;line-height:1.2;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis
}
.location-picker-chevron{
  width:36px;height:36px;border-radius:12px;display:grid;place-items:center;
  background:var(--secondary-background-color);transition:transform .18s ease
}
.location-picker.open .location-picker-chevron{transform:rotate(180deg)}
.location-picker-menu{
  display:none;position:absolute;z-index:30;left:0;right:0;top:calc(100% + 10px);
  padding:8px;border-radius:20px;
  background:color-mix(in srgb,var(--card-background-color) 98%,transparent);
  border:1px solid color-mix(in srgb,var(--divider-color) 80%,transparent);
  box-shadow:0 18px 45px rgba(0,0,0,.18);
  backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)
}
.location-picker.open .location-picker-menu{display:block}
.location-option{
  width:100%;display:flex;align-items:center;gap:12px;padding:12px;
  border:0;border-radius:15px;background:transparent;color:var(--primary-text-color);
  cursor:pointer;text-align:left;transition:background .14s ease
}
.location-option:hover{background:var(--secondary-background-color)}
.location-option.active{
  background:color-mix(in srgb,var(--primary-color) 11%,var(--secondary-background-color))
}
.location-option-icon{
  width:40px;height:40px;border-radius:12px;display:grid;place-items:center;
  background:var(--secondary-background-color);flex:0 0 auto
}
.location-option.active .location-option-icon{
  color:var(--primary-color);
  background:color-mix(in srgb,var(--primary-color) 13%,var(--secondary-background-color))
}
.location-option-icon ha-icon{--mdc-icon-size:23px}
.location-option-copy{min-width:0;flex:1}
.location-option-copy strong{display:block;font-size:14px}
.location-option-copy small{
  display:block;margin-top:3px;color:var(--secondary-text-color);
  font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis
}
.location-option-check{color:var(--primary-color)}
.location-option-check ha-icon{--mdc-icon-size:22px}
.location-picker-hint{
  margin-top:10px;font-size:12px;color:var(--secondary-text-color);line-height:1.45
}
@media(max-width:620px){
  .location-picker-trigger{padding:12px 13px;border-radius:16px}
  .location-picker-icon{width:44px;height:44px;border-radius:13px}
  .location-picker-menu{
    position:absolute;left:0;right:0;top:calc(100% + 8px);bottom:auto;
    max-height:52vh;overflow:auto;border-radius:18px;
    -webkit-overflow-scrolling:touch
  }
}

.location-picker-trigger,.location-option{
  touch-action:manipulation;
  -webkit-tap-highlight-color:transparent;
}
.location-picker-menu{
  overscroll-behavior:contain;
}

.lang-switch{margin-left:auto;display:flex;gap:4px;padding:3px;border-radius:12px;border:1px solid var(--divider-color);background:var(--secondary-background-color)}
.lang-btn{border:0;background:transparent;color:var(--secondary-text-color);border-radius:9px;padding:6px 9px;font-size:10px;font-weight:900;cursor:pointer}
.lang-btn.active{background:var(--card-background-color);color:var(--primary-text-color);box-shadow:0 2px 8px rgba(0,0,0,.08)}
.center-hero{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(310px,.9fr);gap:14px;margin-bottom:14px}
.center-status,.center-info{border:1px solid var(--divider-color);background:var(--card-background-color);border-radius:26px;padding:24px}
.center-status-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 11px;border-radius:999px;font-size:11px;font-weight:900;letter-spacing:.08em;text-transform:uppercase}
.center-status-badge.open{color:#2e7d32;background:color-mix(in srgb,#4caf50 12%,var(--card-background-color));border:1px solid color-mix(in srgb,#4caf50 28%,var(--divider-color))}
.center-status-badge.closed{color:var(--secondary-text-color);background:var(--secondary-background-color);border:1px solid var(--divider-color)}
.center-status h2{font-size:31px;letter-spacing:-.035em;margin:16px 0 7px}
.center-status .status-line{font-size:15px;color:var(--secondary-text-color)}
.center-kpis{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:20px}
.center-kpi{padding:14px;border-radius:17px;background:var(--secondary-background-color);border:1px solid color-mix(in srgb,var(--divider-color) 80%,transparent)}
.center-kpi span{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--secondary-text-color);font-weight:850;margin-bottom:6px}
.center-kpi strong{font-size:17px;line-height:1.25}
.center-address{display:flex;gap:12px;align-items:flex-start;margin-top:16px}
.center-address ha-icon{color:var(--cbbo);--mdc-icon-size:23px;margin-top:1px}
.center-notice{margin-top:16px;padding:14px 15px;border-radius:16px;background:color-mix(in srgb,#ff9800 10%,var(--card-background-color));border:1px solid color-mix(in srgb,#ff9800 27%,var(--divider-color));line-height:1.45}
.center-access{margin-top:16px;padding:14px 15px;border-radius:16px;background:var(--secondary-background-color);line-height:1.45}
.hours-stage{border:1px solid var(--divider-color);background:var(--card-background-color);border-radius:26px;overflow:hidden}
.hours-head{padding:20px 22px;border-bottom:1px solid var(--divider-color);display:flex;justify-content:space-between;gap:14px;align-items:end}
.hours-head h2{margin:0;font-size:21px}.hours-head p{margin:5px 0 0;color:var(--secondary-text-color);font-size:12px}
.hours-row{display:grid;grid-template-columns:160px 1fr;gap:18px;padding:14px 22px;border-bottom:1px solid color-mix(in srgb,var(--divider-color) 78%,transparent);align-items:center}
.hours-row:last-child{border-bottom:0}.hours-row.today{background:color-mix(in srgb,var(--cbbo) 7%,var(--card-background-color))}
.hours-day{font-weight:820}.hours-slots{display:flex;gap:8px;flex-wrap:wrap}
.hour-pill{display:inline-flex;padding:7px 10px;border-radius:10px;background:var(--secondary-background-color);border:1px solid var(--divider-color);font-size:12px;font-weight:750}
.hour-pill.closed{color:var(--secondary-text-color)}
.center-footnote{margin:12px 2px 0;color:var(--secondary-text-color);font-size:11px;line-height:1.5}
@media(max-width:760px){.center-hero{grid-template-columns:1fr}.center-status,.center-info{padding:19px;border-radius:21px}.center-kpis{grid-template-columns:1fr}.hours-row{grid-template-columns:1fr;gap:8px;padding:13px 16px}.lang-switch{margin-left:auto}}
`;

class CBBOWasteCollectionPanel extends HTMLElement {
  constructor(){
    super();
    this.attachShadow({mode:'open'});
    this._hass=null;
    this._data=null;
    this._loading=false;
    this._lastLoad=0;
    this._view=localStorage.getItem('cbbo-panel-view')||'home';
    this._selectedEntryId=localStorage.getItem('cbbo-panel-entry')||null;
    this._shellMounted=false;
    this._refreshTimer=null;
    this._locationPickerOpen=false;
    const storedLang=localStorage.getItem('cbbo-panel-lang');
    this._lang=storedLang||null;
  }
  lang(){
    if(this._lang)return this._lang;
    const haLang=(this._hass?.language||this._hass?.locale?.language||'it').toLowerCase();
    return haLang.startsWith('en')?'en':'it';
  }
  setLanguage(lang){
    this._lang=lang==='en'?'en':'it';
    localStorage.setItem('cbbo-panel-lang',this._lang);
    this.renderShell();
  }
  t(key,vars={}){
    let value=I18N[this.lang()]?.[key]??I18N.it[key]??key;
    Object.entries(vars).forEach(([k,v])=>value=value.replaceAll(`{${k}}`,String(v)));
    return value;
  }
  locale(){return this.lang()==='en'?'en-GB':'it-IT'}
  wasteLabel(type,fallback=''){
    const meta=WASTE_META[type];
    return meta?.[this.lang()]||fallback||type;
  }
  dayLabels(){return [this.t('mon'),this.t('tue'),this.t('wed'),this.t('thu'),this.t('fri'),this.t('sat'),this.t('sun')]}
  set hass(v){
    this._hass=v;
    if(!this._shellMounted) this.renderShell();
    if(!this._data || Date.now()-this._lastLoad>30000){
      clearTimeout(this._refreshTimer);
      this._refreshTimer=setTimeout(()=>this.loadData(),30);
    }else if(!(this._view==='place' && this._locationPickerOpen)){
      this.renderMain();
    }
  }
  get hass(){return this._hass}
  set narrow(v){this._narrow=v}
  set route(v){this._route=v}
  set panel(v){this._panel=v}
  connectedCallback(){ if(!this._shellMounted) this.renderShell(); if(this._hass) this.loadData(); }

  async loadData(force=false){
    if(!this._hass||this._loading) return;
    if(!force&&this._data&&Date.now()-this._lastLoad<30000){if(!(this._view==='place'&&this._locationPickerOpen))this.renderMain();return}
    this._loading=true; this.renderMain();
    try{
      this._data=await this._hass.callWS({type:'cbbo_waste_collection/panel_data'});
      this._lastLoad=Date.now();
      const entries=this._data?.entries||[];
      if(!entries.some(x=>x.entry_id===this._selectedEntryId)) this._selectedEntryId=entries[0]?.entry_id||null;
    }catch(err){ console.error('CBBO panel',err); this._data={entries:[],error:true}; }
    finally{this._loading=false;this.renderMain();}
  }
  async refresh(){
    if(!this._hass||this._loading)return;
    this._loading=true;this.renderMain();
    try{
      await this._hass.callService('cbbo_waste_collection','refresh',{});
      await new Promise(r=>setTimeout(r,900));
      this._lastLoad=0;await this.loadData(true);
    }catch(e){console.error(e);this._loading=false;this.renderMain()}
  }
  entry(){const e=this._data?.entries||[];return e.find(x=>x.entry_id===this._selectedEntryId)||e[0]||null}
  entryName(e=this.entry()){if(!e)return 'CBBO';return e.zone_name?`${e.municipality_name} · ${e.zone_name}`:e.municipality_name}
  fmtDate(v,weekday=true){if(!v)return '—';const d=new Date(`${v}T12:00:00`);return new Intl.DateTimeFormat(this.locale(),{weekday:weekday?'long':undefined,day:'numeric',month:'long'}).format(d)}
  fmtStamp(v){if(!v)return '—';const d=new Date(v);return Number.isNaN(d.getTime())?v:new Intl.DateTimeFormat(this.locale(),{dateStyle:'short',timeStyle:'short'}).format(d)}
  text(c){return c?.waste_types?.length?c.waste_types.map((t,i)=>this.wasteLabel(t,c?.labels?.[i]||t)).join(' + '):this.t('noCollection')}
  wasteItems(c){return (c?.waste_types||[]).map((t,i)=>{const m=WASTE_META[t]||{icon:'mdi:recycle',cls:'other'};return `<span class="waste-token ${m.cls}"><ha-icon icon="${m.icon}"></ha-icon><b>${this.wasteLabel(t,c?.labels?.[i]||t)}</b></span>`}).join('')}
  dotItems(c){return (c?.waste_types||[]).map(t=>{const m=WASTE_META[t]||{icon:'mdi:recycle',cls:'other'};return `<span class="waste-dot ${m.cls}"><ha-icon icon="${m.icon}"></ha-icon></span>`}).join('')||'<span class="waste-dot empty"><ha-icon icon="mdi:minus"></ha-icon></span>'}
  tab(view,icon,label){return `<button class="nav-btn tab ${this._view===view?'active':''}" data-view="${view}" type="button"><ha-icon icon="${icon}"></ha-icon><span>${label}</span></button>`}
  sourceLabel(e){return e?.source_status==='fallback'?this.t('localCalendar'):e?.source_status==='cache'?this.t('cachedData'):this.t('onlineData')}

  renderShell(){
    const lang=this.lang();
    this.shadowRoot.innerHTML=`<style>${PANEL_STYLES}</style><div class="app"><header class="topbar"><div class="topbar-main"><button class="menu-btn" id="ha-menu-toggle" aria-label="Home Assistant menu" title="Home Assistant menu"><ha-icon icon="mdi:menu"></ha-icon></button><div class="app-identity"><div class="app-icon"><img src="/cbbo_waste_collection/icon.png" alt=""></div><div class="brand"><div class="brand-line"><div class="brand-title">CBBO Waste Collection</div><span class="version-badge">3.0.0</span></div><div class="brand-subtitle" id="brand-subtitle">Waste Center</div></div></div><div class="lang-switch" title="${this.t('language')}"><button class="lang-btn ${lang==='it'?'active':''}" data-lang="it">IT</button><button class="lang-btn ${lang==='en'?'active':''}" data-lang="en">EN</button></div></div><div class="nav-scroller"><nav class="nav tabs">${this.tab('home','mdi:view-dashboard',this.t('overview'))}${this.tab('calendar','mdi:calendar-month',this.t('calendar'))}${this.tab('place','mdi:map-marker-outline',this.t('municipality'))}${this.tab('center','mdi:recycle-variant',this.t('center'))}${this.tab('diag','mdi:tools',this.t('diagnostics'))}<button class="nav-btn support-nav" id="support-nav" type="button"><ha-icon icon="mdi:coffee-outline"></ha-icon><span>${this.t('support')}</span></button></nav></div></header><main id="view-content"></main><div class="footer">CBBO Waste Collection · v3.0.0 · Riccardo Cosi · Fabio Vittori</div></div>`;
    this._shellMounted=true;this.bindShell();this.renderMain();
  }
  bindShell(){
    this.shadowRoot.querySelectorAll('.lang-btn[data-lang]').forEach(btn=>btn.addEventListener('click',()=>this.setLanguage(btn.dataset.lang)));
    this.shadowRoot.getElementById('ha-menu-toggle')?.addEventListener('click',()=>{this.dispatchEvent(new Event('hass-toggle-menu',{bubbles:true,composed:true}));window.dispatchEvent(new Event('hass-toggle-menu',{bubbles:true,composed:true}))});
    this.shadowRoot.querySelectorAll('.tabs .tab[data-view]').forEach(el=>{
      let sx=0,sy=0,moved=false,touchHandled=false;
      el.addEventListener('touchstart',ev=>{if(ev.touches?.length!==1)return;sx=ev.touches[0].clientX;sy=ev.touches[0].clientY;moved=false;touchHandled=false},{passive:true});
      el.addEventListener('touchmove',ev=>{if(ev.touches?.length!==1)return;if(Math.abs(ev.touches[0].clientX-sx)>10||Math.abs(ev.touches[0].clientY-sy)>10)moved=true},{passive:true});
      el.addEventListener('touchend',ev=>{if(moved)return;touchHandled=true;ev.preventDefault();this.navigate(el.dataset.view);setTimeout(()=>touchHandled=false,350)},{passive:false});
      el.addEventListener('click',ev=>{if(touchHandled){ev.preventDefault();ev.stopPropagation();return}this.navigate(el.dataset.view)});
    });
    this.shadowRoot.getElementById('support-nav')?.addEventListener('click',()=>this.navigate('support'));
  }
  navigate(v){if(!v||v===this._view)return;this._view=v;localStorage.setItem('cbbo-panel-view',v);this.updateTabs();this.renderMain()}
  updateTabs(){this.shadowRoot.querySelectorAll('.tabs .tab[data-view]').forEach(el=>el.classList.toggle('active',el.dataset.view===this._view))}
  renderMain(){
    if(!this._shellMounted)return;
    const main=this.shadowRoot.getElementById('view-content');if(!main)return;
    const e=this.entry();
    const subtitle=this.shadowRoot.getElementById('brand-subtitle');if(subtitle)subtitle.textContent=e?`${this.entryName(e)} · Waste Center`:'Waste Center';
    if(!this._data){main.innerHTML=`<div class="empty-state"><ha-icon icon="mdi:recycle"></ha-icon><h2>CBBO Waste Collection</h2><p>${this._loading?this.t('updating'):this.t('loading')}</p></div>`;return}
    if(this._data.error){main.innerHTML=`<div class="empty-state"><ha-icon icon="mdi:alert-circle-outline"></ha-icon><h2>${this.t('loadError')}</h2><p>${this.t('tryAgain')}</p><button class="action-btn primary" id="retry">${this.t('retry')}</button></div>`;main.querySelector('#retry')?.addEventListener('click',()=>this.loadData(true));return}
    if(!e){main.innerHTML=`<div class="empty-state"><ha-icon icon="mdi:recycle"></ha-icon><h2>${this.t('noMunicipality')}</h2><p>${this.t('addIntegration')}</p></div>`;return}
    main.innerHTML=this.body(e);this.updateTabs();this.bindMain();
  }
  body(e){if(this._view==='calendar')return this.calendarView(e);if(this._view==='place')return this.placeView(e);if(this._view==='center')return this.centerView(e);if(this._view==='diag')return this.diagView(e);if(this._view==='support')return this.supportView(e);return this.homeView(e)}
  homeView(e){
    const expose=e.put_out_tonight;const focus=expose?e.tomorrow:e.today;
    const title=expose?this.t('expose'):this.t('nothingTonight');
    const desc=expose?this.t('prepareTomorrow',{waste:this.text(e.tomorrow)}):this.t('noTomorrow');
    return `<div class="view-head"><div class="eyebrow">${this.entryName(e)}</div><h1>${this.t('headline')}</h1><p>${this.t('headlineSub')}</p></div><section class="hero"><div class="hero-copy"><span class="hero-kicker"><ha-icon icon="${expose?'mdi:weather-night':'mdi:check-circle-outline'}"></ha-icon>${expose?this.t('exposeReminder'):this.t('allQuiet')}</span><h1>${title}</h1><p>${desc}</p><div class="waste-tokens">${this.wasteItems(focus)}</div><div class="hero-actions"><button class="action-btn primary" id="refresh-main"><ha-icon icon="mdi:refresh"></ha-icon>${this._loading?this.t('updating'):this.t('refreshData')}</button><button class="action-btn" data-view="calendar"><ha-icon icon="mdi:calendar-month"></ha-icon>${this.t('openCalendar')}</button></div></div><div class="hero-side"><div class="next-orbit"><span>${this.t('nextCollection')}</span><strong>${this.text(e.next)}</strong><small>${this.fmtDate(e.next?.date)}</small><div class="day-count"><b>${e.days_to_next??'—'}</b><em>${e.days_to_next===1?this.t('day'):this.t('days')} ${this.t('untilCollection')}</em></div></div></div></section><div class="status-strip"><div class="status-item"><span>${this.t('wasteToday')}</span><strong>${this.text(e.today)}</strong><small>${this.dotItems(e.today)}</small></div><div class="status-item"><span>${this.t('wasteTomorrow')}</span><strong>${this.text(e.tomorrow)}</strong><small>${this.dotItems(e.tomorrow)}</small></div><div class="status-item ${expose?'good':''}"><span>${this.t('putOutTonight')}</span><strong>${expose?this.t('yes'):this.t('no')}</strong><small>${expose?this.t('prepareBins'):this.t('noExposure')}</small></div><div class="status-item"><span>${this.t('source')}</span><strong>${this.sourceLabel(e)}</strong><small>${this.fmtStamp(e.last_update)}</small></div></div>${this.timelineBlock(e,this.t('upcoming'),6)}`
  }
  timelineBlock(e,title,limit=10){const rows=(e.upcoming||[]).slice(0,limit).map((c,i)=>`<div class="timeline-row"><div class="timeline-date">${this.fmtDate(c.date)}<small>${i===0?this.t('nextPassage'):''}</small></div><div class="timeline-main"><strong>${this.text(c)}</strong></div><div class="timeline-dots">${this.dotItems(c)}</div></div>`).join('');return `<section class="schedule-stage"><div class="stage-head"><div><div class="eyebrow">${this.t('agenda')}</div><h2>${title}</h2><p>${this.lang()==='en'?`Upcoming collections for ${this.entryName(e)}.`:`I prossimi passaggi previsti dal calendario ${this.entryName(e)}.`}</p></div></div><div class="timeline">${rows||`<div class="timeline-row"><div class="timeline-main"><strong>${this.t('noEvents')}</strong></div></div>`}</div></section>`}
  calendarView(e){
    const upcoming=(e.upcoming||[]).slice(0,7);const cards=upcoming.map((c,i)=>{const d=new Date(`${c.date}T12:00:00`);return `<div class="rail-day ${i===0?'today':''}"><span>${new Intl.DateTimeFormat(this.locale(),{weekday:'short'}).format(d)}</span><b>${d.getDate()}</b><div class="rail-dots">${this.dotItems(c)}</div></div>`}).join('');
    return `<div class="view-head"><div class="eyebrow">${this.t('calendar')}</div><h1>${this.t('calendarTitle')}</h1><p>${this.t('calendarSub')}</p></div><section class="calendar-hero"><div class="stage-head" style="padding:0"><div><h2>${this.t('sevenCollections')}</h2><p>${this.entryName(e)}</p></div></div><div class="month-rail">${cards}</div></section>${this.timelineBlock(e,this.t('fullAgenda'),14)}`
  }
  placeView(e){
    const entries=this._data?.entries||[];
    const options=entries.map(x=>{
      const active=x.entry_id===e.entry_id;
      return `<button class="location-option ${active?'active':''}" data-entry-id="${x.entry_id}" type="button"><span class="location-option-icon"><ha-icon icon="mdi:map-marker-outline"></ha-icon></span><span class="location-option-copy"><strong>${this.entryName(x)}</strong><small>${x.municipality_name||x.municipality||''}${x.zone_name?` · ${x.zone_name}`:''}</small></span>${active?'<span class="location-option-check"><ha-icon icon="mdi:check-circle"></ha-icon></span>':''}</button>`;
    }).join('');
    return `<div class="view-head"><div class="eyebrow">${this.t('municipality')}</div><h1>${this.t('areaTitle')}</h1><p>${this.t('areaSub')}</p></div><div class="control-deck"><section class="control-panel"><label>${this.t('activeProfile')}</label><div class="location-picker ${this._locationPickerOpen?'open':''}" id="location-picker"><button class="location-picker-trigger" id="location-picker-trigger" type="button" aria-expanded="${this._locationPickerOpen?'true':'false'}"><span class="location-picker-icon"><ha-icon icon="mdi:map-marker-radius-outline"></ha-icon></span><span class="location-picker-copy"><small>${this.t('municipalityZone')}</small><strong>${this.entryName(e)}</strong></span><span class="location-picker-chevron"><ha-icon icon="mdi:chevron-down"></ha-icon></span></button><div class="location-picker-menu" id="location-picker-menu">${options}</div></div><div class="location-picker-hint">${entries.length>1?this.t('configuredProfiles',{count:entries.length}):this.t('oneProfile')}</div><div class="link-stack">${e.source_url?`<a class="wide-link" href="${e.source_url}" target="_blank" rel="noopener"><span>${this.t('officialCbbo',{name:e.municipality_name})}</span><ha-icon icon="mdi:open-in-new"></ha-icon></a>`:''}${e.pdf_url?`<a class="wide-link" href="${e.pdf_url}" target="_blank" rel="noopener"><span>${this.t('officialCalendar')}</span><ha-icon icon="mdi:file-pdf-box"></ha-icon></a>`:''}<button class="wide-link" id="refresh-place"><span>${this.t('refreshNow')}</span><ha-icon icon="mdi:refresh"></ha-icon></button></div></section><section class="info-panel"><div class="eyebrow">${this.t('activeProfile')}</div><h2 style="margin:0;font-size:28px">${this.entryName(e)}</h2><p style="color:var(--secondary-text-color);line-height:1.6">${this.t('profileInfo')}</p><div class="waste-tokens" style="margin-top:22px">${this.wasteItems(e.next)}</div></section></div>`
  }
  periodMatches(period,date=new Date()){
    const md=`${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
    const start=period.start,end=period.end;
    return start<=end?(md>=start&&md<=end):(md>=start||md<=end);
  }
  centerPeriod(center,date=new Date()){return center?.periods?.find(p=>this.periodMatches(p,date))||center?.periods?.[0]||null}
  minutes(value){const [h,m]=value.split(':').map(Number);return h*60+m}
  centerStatus(center){
    const now=new Date(),period=this.centerPeriod(center,now),day=(now.getDay()+6)%7,slots=period?.schedule?.[String(day)]||[];
    const cur=now.getHours()*60+now.getMinutes();
    for(const slot of slots){const [a,b]=slot.split('-');if(cur>=this.minutes(a)&&cur<this.minutes(b))return {open:true,label:this.t('closesAt',{time:b}),period,slots};if(cur<this.minutes(a))return {open:false,label:this.t('opensAt',{time:a}),period,slots}}
    for(let offset=1;offset<=7;offset++){const d=new Date(now);d.setDate(now.getDate()+offset);const p=this.centerPeriod(center,d),idx=(d.getDay()+6)%7,next=p?.schedule?.[String(idx)]||[];if(next.length){const dayName=offset===1?this.t('tomorrow'):this.dayLabels()[idx];return {open:false,label:`${dayName} · ${next[0].split('-')[0]}`,period,slots}}}
    return {open:false,label:'—',period,slots};
  }
  centerView(e){
    const c=e.recycling_center;if(!c)return `<div class="empty-state"><ha-icon icon="mdi:recycle-variant"></ha-icon><h2>${this.t('center')}</h2><p>—</p></div>`;
    const status=this.centerStatus(c),period=status.period,now=new Date(),today=(now.getDay()+6)%7;
    const todaySlots=period?.schedule?.[String(today)]||[];
    const weekly=this.dayLabels().map((dayName,i)=>{const slots=period?.schedule?.[String(i)]||[];return `<div class="hours-row ${i===today?'today':''}"><div class="hours-day">${dayName}</div><div class="hours-slots">${slots.length?slots.map(s=>`<span class="hour-pill">${s.replace('-', ' – ')}</span>`).join(''):`<span class="hour-pill closed">${this.t('closed')}</span>`}</div></div>`}).join('');
    const name=this.lang()==='en'?c.name_en:c.name_it,notice=this.lang()==='en'?c.notice_en:c.notice_it,access=this.lang()==='en'?c.access_en:c.access_it;
    return `<div class="view-head"><div class="eyebrow">${this.t('centerEyebrow')}</div><h1>${this.t('centerTitle')}</h1><p>${this.t('centerSub')}</p></div><div class="center-hero"><section class="center-status"><span class="center-status-badge ${status.open?'open':'closed'}"><ha-icon icon="${status.open?'mdi:door-open':'mdi:door-closed'}"></ha-icon>${status.open?this.t('openNow'):this.t('closedNow')}</span><h2>${name}</h2><div class="status-line">${status.label}</div><div class="center-kpis"><div class="center-kpi"><span>${this.t('todayHours')}</span><strong>${todaySlots.length?todaySlots.map(x=>x.replace('-',' – ')).join(' · '):this.t('closed')}</strong></div><div class="center-kpi"><span>${this.t('nextOpen')}</span><strong>${status.open?status.label:this.centerStatus(c).label}</strong></div></div></section><section class="center-info"><div class="eyebrow">${this.t('address')}</div><div class="center-address"><ha-icon icon="mdi:map-marker-outline"></ha-icon><strong>${c.address}</strong></div>${access?`<div class="center-access"><strong>${this.t('access')}</strong><br>${access}</div>`:''}${notice?`<div class="center-notice">${notice}</div>`:''}<div class="link-stack"><a class="wide-link" href="${c.official_url}" target="_blank" rel="noopener"><span>${this.t('officialSource')}</span><ha-icon icon="mdi:open-in-new"></ha-icon></a></div></section></div><section class="hours-stage"><div class="hours-head"><div><div class="eyebrow">${this.t('weeklyHours')}</div><h2>${this.lang()==='en'?period?.label_en:period?.label_it}</h2><p>${this.t('verified',{date:this._data?.recycling_centers_verified||'2026-08-19'})}</p></div></div>${weekly}</section><div class="center-footnote">⚠️ ${this.t('holidayWarning')}</div>`
  }
  diagView(e){return `<div class="view-head"><div class="eyebrow">${this.t('diagnostics')}</div><h1>${this.t('diagTitle')}</h1><p>${this.t('diagSub')}</p></div><section class="info-grid"><div class="info-cell"><span>${this.t('dataSource')}</span><strong>${e.data_source||'—'}</strong><small>${this.sourceLabel(e)}</small></div><div class="info-cell"><span>${this.t('lastUpdate')}</span><strong>${this.fmtStamp(e.last_update)}</strong><small>${this.t('autoUpdate')}</small></div><div class="info-cell"><span>${this.t('municipality')}</span><strong>${this.entryName(e)}</strong><small>${e.municipality||''}</small></div><div class="info-cell"><span>${this.t('integrationVersion')}</span><strong>${this._data?.version||CBBO_PANEL_VERSION}</strong><small>CBBO Waste Collection</small></div></section>${e.last_error?`<section class="info-panel" style="margin-top:14px"><div class="eyebrow">${this.t('lastError')}</div><strong>${e.last_error}</strong></section>`:''}`}
  supportView(e){return `<div class="view-head"><div class="eyebrow">Open source</div><h1>${this.t('supportTitle')}</h1><p>${this.t('supportSub')}</p></div><section class="support-stage"><div><h1>${this.t('useful')}<br>${this.t('coffee')}</h1><p>${this.t('supportText')}</p><div class="hero-actions"><a class="action-btn primary" href="${this._data?.ko_fi||'https://ko-fi.com/fabvittori'}" target="_blank" rel="noopener"><ha-icon icon="mdi:coffee-outline"></ha-icon>${this.t('supportKofi')}</a><a class="action-btn" href="https://github.com/fabiovit/cbbo-waste-collection" target="_blank" rel="noopener"><ha-icon icon="mdi:github"></ha-icon>GitHub</a></div><div class="credits">${this.t('credits')}<br><br>${this.t('disclaimer')}</div></div><div class="coffee-orb">☕</div></section>`}
  bindMain(){
    const main=this.shadowRoot.getElementById('view-content');
    main?.querySelectorAll('[data-view]').forEach(el=>el.addEventListener('click',()=>this.navigate(el.dataset.view)));
    main?.querySelector('#refresh-main')?.addEventListener('click',()=>this.refresh());
    main?.querySelector('#refresh-place')?.addEventListener('click',()=>this.refresh());

    const picker=main?.querySelector('#location-picker');
    const trigger=main?.querySelector('#location-picker-trigger');
    const menu=main?.querySelector('#location-picker-menu');

    trigger?.addEventListener('click',ev=>{
      ev.preventDefault();
      ev.stopPropagation();
      if(!picker)return;
      const willOpen=!this._locationPickerOpen;
      this._locationPickerOpen=willOpen;
      picker.classList.toggle('open',willOpen);
      trigger.setAttribute('aria-expanded',willOpen?'true':'false');
    });

    menu?.addEventListener('click',ev=>ev.stopPropagation());

    main?.querySelectorAll('.location-option[data-entry-id]').forEach(option=>{
      option.addEventListener('click',ev=>{
        ev.preventDefault();
        ev.stopPropagation();
        const entryId=option.dataset.entryId;
        if(!entryId||entryId===this._selectedEntryId){
          this._locationPickerOpen=false;
          picker?.classList.remove('open');
          trigger?.setAttribute('aria-expanded','false');
          return;
        }
        this._locationPickerOpen=false;
        picker?.classList.remove('open');
        trigger?.setAttribute('aria-expanded','false');
        this._selectedEntryId=entryId;
        localStorage.setItem('cbbo-panel-entry',entryId);
        this.renderMain();
      });
    });

  }
}
if(!customElements.get('cbbo-waste-collection-panel-v300')) customElements.define('cbbo-waste-collection-panel-v300',CBBOWasteCollectionPanel);
