const CBBO_PANEL_VERSION = "2.1.2";

const STRINGS = {
  it: {
    title: "CBBO Waste Collection",
    subtitle: "Raccolta differenziata direttamente in Home Assistant",
    select: "Comune / zona",
    today: "Rifiuti oggi",
    tomorrow: "Rifiuti domani",
    next: "Prossimo ritiro",
    days: "Giorni al prossimo ritiro",
    tonight: "Esporre stasera",
    tomorrowCollection: "Ritiro domani",
    calendar: "Prossime raccolte",
    source: "Sorgente dati",
    updated: "Ultimo aggiornamento",
    yes: "Sì",
    no: "No",
    none: "Nessun ritiro",
    noConfig: "Nessun Comune CBBO configurato.",
    noConfigHint: "Aggiungi CBBO Waste Collection da Impostazioni → Dispositivi e servizi.",
    refresh: "Aggiorna",
    refreshing: "Aggiornamento…",
    support: "Supporta il progetto",
    openCbbo: "Apri CBBO",
    diagnostic: "Informazioni",
    status: "Stato",
    online: "Dati online",
    fallback: "Calendario locale 2026 attivo",
    cache: "Dati in cache",
    error: "Impossibile caricare i dati della dashboard.",
    daysUnit: "giorni",
  },
  en: {
    title: "CBBO Waste Collection",
    subtitle: "Waste collection directly in Home Assistant",
    select: "Municipality / zone",
    today: "Waste today",
    tomorrow: "Waste tomorrow",
    next: "Next collection",
    days: "Days to next collection",
    tonight: "Put out tonight",
    tomorrowCollection: "Collection tomorrow",
    calendar: "Upcoming collections",
    source: "Data source",
    updated: "Last update",
    yes: "Yes",
    no: "No",
    none: "No collection",
    noConfig: "No CBBO municipality configured.",
    noConfigHint: "Add CBBO Waste Collection from Settings → Devices & services.",
    refresh: "Refresh",
    refreshing: "Refreshing…",
    support: "Support the project",
    openCbbo: "Open CBBO",
    diagnostic: "Information",
    status: "Status",
    online: "Online data",
    fallback: "Local 2026 calendar active",
    cache: "Cached data",
    error: "Unable to load dashboard data.",
    daysUnit: "days",
  },
};

const WASTE_ICONS = {
  organic: "🌱",
  paper: "📦",
  plastic: "🟨",
  glass_cans: "🫙",
  residual: "🗑️",
  sanitary: "🧷",
  green: "🌿",
};

class CBBOWasteCollectionPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = null;
    this._data = null;
    this._selectedEntryId = localStorage.getItem("cbbo-panel-entry") || null;
    this._loading = false;
    this._lastLoad = 0;
    this._refreshTimer = null;
  }

  set hass(value) {
    this._hass = value;
    const now = Date.now();
    if (!this._data || now - this._lastLoad > 30000) {
      clearTimeout(this._refreshTimer);
      this._refreshTimer = setTimeout(() => this._loadData(), 50);
    }
  }

  get hass() { return this._hass; }
  set narrow(value) { this._narrow = value; }
  set route(value) { this._route = value; }
  set panel(value) { this._panel = value; }

  connectedCallback() {
    this._render();
    if (this._hass) this._loadData();
  }

  _lang() {
    const lang = (this._hass?.language || navigator.language || "it").toLowerCase();
    return lang.startsWith("it") ? "it" : "en";
  }

  _t(key) { return STRINGS[this._lang()][key] || key; }

  async _loadData(force = false) {
    if (!this._hass || this._loading) return;
    if (!force && this._data && Date.now() - this._lastLoad < 30000) return;
    this._loading = true;
    this._render();
    try {
      this._data = await this._hass.callWS({ type: "cbbo_waste_collection/panel_data" });
      this._lastLoad = Date.now();
      const entries = this._data?.entries || [];
      if (!entries.find((entry) => entry.entry_id === this._selectedEntryId)) {
        this._selectedEntryId = entries[0]?.entry_id || null;
      }
    } catch (err) {
      console.error("CBBO panel:", err);
      this._data = { entries: [], error: true };
    } finally {
      this._loading = false;
      this._render();
    }
  }

  async _requestRefresh() {
    if (!this._hass || this._loading) return;
    this._loading = true;
    this._render();
    try {
      await this._hass.callService("cbbo_waste_collection", "refresh", {});
      await new Promise((resolve) => setTimeout(resolve, 1200));
      this._lastLoad = 0;
      await this._loadData(true);
    } catch (err) {
      console.error("CBBO refresh:", err);
      this._loading = false;
      this._render();
    }
  }

  _entry() {
    const entries = this._data?.entries || [];
    return entries.find((entry) => entry.entry_id === this._selectedEntryId) || entries[0];
  }

  _entryLabel(entry) {
    return entry.zone_name ? `${entry.municipality_name} · ${entry.zone_name}` : entry.municipality_name;
  }

  _collectionText(collection) {
    return collection?.labels?.length ? collection.labels.join(" + ") : this._t("none");
  }

  _collectionIcons(collection) {
    if (!collection?.waste_types?.length) return "—";
    return collection.waste_types.map((type) => WASTE_ICONS[type] || "♻️").join(" ");
  }

  _formatDate(value, includeWeekday = true) {
    if (!value) return "—";
    const date = new Date(`${value}T12:00:00`);
    return new Intl.DateTimeFormat(this._lang() === "it" ? "it-IT" : "en-GB", {
      weekday: includeWeekday ? "long" : undefined,
      day: "numeric",
      month: "long",
    }).format(date);
  }

  _formatTimestamp(value) {
    if (!value) return "—";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return new Intl.DateTimeFormat(this._lang() === "it" ? "it-IT" : "en-GB", {
      dateStyle: "short",
      timeStyle: "short",
    }).format(date);
  }

  _card(icon, title, value, detail = "", tone = "") {
    return `<article class="card ${tone}">
      <div class="card-head"><span class="card-icon">${icon}</span><span>${title}</span></div>
      <div class="card-value">${value}</div>
      ${detail ? `<div class="card-detail">${detail}</div>` : ""}
    </article>`;
  }

  _render() {
    if (!this.shadowRoot) return;
    const entry = this._entry();
    const entries = this._data?.entries || [];

    const styles = `<style>
      :host{display:block;min-height:100%;color:var(--primary-text-color);background:radial-gradient(circle at 10% 0%,rgba(76,175,80,.12),transparent 32rem),var(--primary-background-color);font-family:var(--paper-font-body1_-_font-family,system-ui,sans-serif)}
      *{box-sizing:border-box}.page{max-width:1180px;margin:0 auto;padding:24px 20px 40px}.hero{display:flex;gap:18px;align-items:center;justify-content:space-between;margin-bottom:20px}.hero-main{display:flex;align-items:center;gap:16px;min-width:0}.logo{width:62px;height:62px;border-radius:18px;display:grid;place-items:center;font-size:34px;background:linear-gradient(145deg,#2e7d32,#66bb6a);box-shadow:0 10px 28px rgba(46,125,50,.25);color:white;flex:0 0 auto}h1{font-size:28px;line-height:1.1;margin:0 0 6px}.subtitle{color:var(--secondary-text-color);font-size:14px}.actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}
      button,select,.link-button{border:1px solid var(--divider-color);background:var(--card-background-color);color:var(--primary-text-color);border-radius:12px;min-height:42px;padding:0 14px;font:inherit;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:7px}button:hover,.link-button:hover{background:var(--secondary-background-color)}button.primary{border-color:#388e3c;background:#388e3c;color:white}button:disabled{opacity:.65;cursor:wait}.selector-wrap{display:flex;align-items:center;gap:10px;margin-bottom:18px;color:var(--secondary-text-color)}select{min-width:240px}
      .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-bottom:18px}.card,.section{background:var(--card-background-color);border:1px solid var(--divider-color);border-radius:18px;box-shadow:var(--ha-card-box-shadow,0 2px 8px rgba(0,0,0,.08))}.card{padding:18px;min-height:138px}.card-head{display:flex;align-items:center;gap:9px;color:var(--secondary-text-color);font-weight:600;margin-bottom:14px}.card-icon{font-size:22px}.card-value{font-size:22px;font-weight:700;line-height:1.25}.card-detail{margin-top:8px;color:var(--secondary-text-color);font-size:13px}.positive .card-value{color:var(--success-color,#43a047)}
      .section{padding:20px;margin-bottom:18px}.section h2{font-size:18px;margin:0 0 14px}.upcoming{display:grid;gap:8px}.row{display:grid;grid-template-columns:160px 1fr auto;gap:12px;align-items:center;padding:11px 12px;border-radius:11px;background:var(--secondary-background-color)}.row-date{font-weight:600;text-transform:capitalize}.row-icons{font-size:20px;letter-spacing:2px}.meta{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;color:var(--secondary-text-color);font-size:13px}.meta strong{display:block;color:var(--primary-text-color);margin-top:4px;word-break:break-word}.empty{padding:64px 24px;text-align:center;color:var(--secondary-text-color)}.empty-icon{font-size:58px;margin-bottom:14px}.empty h2{color:var(--primary-text-color);margin-bottom:8px}.footer{text-align:center;color:var(--secondary-text-color);font-size:12px;padding-top:8px}.error{color:var(--error-color,#db4437)}
      @media(max-width:720px){.page{padding:16px 12px 28px}.hero{align-items:flex-start;flex-direction:column}.actions{justify-content:flex-start;width:100%}.grid{grid-template-columns:1fr}.selector-wrap{align-items:stretch;flex-direction:column}select{width:100%}.row{grid-template-columns:1fr auto}.row-value{grid-column:1/-1}.meta{grid-template-columns:1fr}}
    </style>`;

    if (!this._data) {
      this.shadowRoot.innerHTML = `${styles}<div class="page"><div class="empty"><div class="empty-icon">♻️</div><h2>${this._t("title")}</h2><p>${this._loading ? this._t("refreshing") : "…"}</p></div></div>`;
      return;
    }
    if (this._data.error) {
      this.shadowRoot.innerHTML = `${styles}<div class="page"><div class="empty"><div class="empty-icon">⚠️</div><h2>${this._t("error")}</h2><button id="retry">${this._t("refresh")}</button></div></div>`;
      this.shadowRoot.querySelector("#retry")?.addEventListener("click", () => this._loadData(true));
      return;
    }
    if (!entry) {
      this.shadowRoot.innerHTML = `${styles}<div class="page"><div class="empty"><div class="empty-icon">♻️</div><h2>${this._t("noConfig")}</h2><p>${this._t("noConfigHint")}</p></div></div>`;
      return;
    }

    const selector = entries.length > 1 ? `<div class="selector-wrap"><label for="entry-select">${this._t("select")}</label><select id="entry-select">${entries.map((item) => `<option value="${item.entry_id}" ${item.entry_id === entry.entry_id ? "selected" : ""}>${this._entryLabel(item)}</option>`).join("")}</select></div>` : "";
    const upcoming = (entry.upcoming || []).slice(0, 8).map((item) => `<div class="row"><div class="row-date">${this._formatDate(item.date)}</div><div class="row-value">${this._collectionText(item)}</div><div class="row-icons">${this._collectionIcons(item)}</div></div>`).join("");

    this.shadowRoot.innerHTML = `${styles}<div class="page">
      <header class="hero"><div class="hero-main"><div class="logo">♻</div><div><h1>${this._t("title")}</h1><div class="subtitle">${this._entryLabel(entry)} · ${this._t("subtitle")}</div></div></div>
      <div class="actions">${entry.source_url ? `<a class="link-button" href="${entry.source_url}" target="_blank" rel="noopener">🌐 ${this._t("openCbbo")}</a>` : ""}<a class="link-button" href="${this._data.ko_fi}" target="_blank" rel="noopener">☕ ${this._t("support")}</a><button id="refresh" class="primary" ${this._loading ? "disabled" : ""}>↻ ${this._loading ? this._t("refreshing") : this._t("refresh")}</button></div></header>
      ${selector}
      <section class="grid">
        ${this._card(this._collectionIcons(entry.today),this._t("today"),this._collectionText(entry.today))}
        ${this._card(this._collectionIcons(entry.tomorrow),this._t("tomorrow"),this._collectionText(entry.tomorrow))}
        ${this._card("🚛",this._t("next"),this._collectionText(entry.next),entry.next?this._formatDate(entry.next.date):"")}
        ${this._card("⏱️",this._t("days"),entry.days_to_next??"—",entry.days_to_next!=null?this._t("daysUnit"):"")}
        ${this._card("🌙",this._t("tonight"),entry.put_out_tonight?this._t("yes"):this._t("no"),entry.put_out_tonight?this._collectionText(entry.tomorrow):"",entry.put_out_tonight?"positive":"")}
        ${this._card("🚚",this._t("tomorrowCollection"),entry.collection_tomorrow?this._t("yes"):this._t("no"),"",entry.collection_tomorrow?"positive":"")}
      </section>
      <section class="section"><h2>📆 ${this._t("calendar")}</h2><div class="upcoming">${upcoming||`<div>${this._t("none")}</div>`}</div></section>
      <section class="section"><h2>ℹ️ ${this._t("diagnostic")}</h2><div class="meta"><div>${this._t("source")}<strong>${entry.data_source||"—"}</strong></div><div>${this._t("updated")}<strong>${this._formatTimestamp(entry.last_update)}</strong></div><div>${this._t("status")}<strong>${this._t(entry.source_status||"online")}</strong></div><div>Version<strong>${this._data.version||CBBO_PANEL_VERSION}</strong></div>${entry.last_error && entry.source_status === "online" ? `<div class="error">Error<strong>${entry.last_error}</strong></div>` : ""}</div></section>
      <div class="footer">CBBO Waste Collection · Riccardo Cosi / Fabio Vittori · v${this._data.version||CBBO_PANEL_VERSION}</div>
    </div>`;

    this.shadowRoot.querySelector("#refresh")?.addEventListener("click", () => this._requestRefresh());
    this.shadowRoot.querySelector("#entry-select")?.addEventListener("change", (event) => {
      this._selectedEntryId = event.target.value;
      localStorage.setItem("cbbo-panel-entry", this._selectedEntryId);
      this._render();
    });
  }
}

if (!customElements.get("cbbo-waste-collection-panel")) {
  customElements.define("cbbo-waste-collection-panel", CBBOWasteCollectionPanel);
}
