"""HTTP client and robust calendar parser for the public CBBO website."""
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from datetime import date, datetime
from html.parser import HTMLParser
from typing import Any, Iterable

from aiohttp import ClientError, ClientSession

from .const import BASE_URL, ZONE_NORTH, ZONE_SOUTH
from .schedule import Collection, normalize_title

_DATE_RE = re.compile(r"20\d{2}-\d{2}-\d{2}")
_WASTE_WORDS = re.compile(
    r"organ|plastic|carta|cartone|vetro|lattin|indifferenzi|non riciclab|secco|"
    r"tessili sanitari|pannolin|pannolon|verde|sfalci|ramaglie",
    re.I,
)


class CBBOApiError(Exception):
    """Raised when CBBO data cannot be downloaded or parsed."""


class _CalendarHTMLParser(HTMLParser):
    """Collect date-bearing elements and their visible text."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._stack: list[dict[str, Any]] = []
        self.candidates: list[tuple[str, str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.casefold(): value or "" for key, value in attrs}
        date_value = ""
        for key in ("data-date", "data-start", "datetime", "date", "start"):
            if _DATE_RE.search(values.get(key, "")):
                date_value = values[key]
                break
        title = next(
            (values.get(key, "") for key in ("data-title", "data-event", "title", "aria-label") if values.get(key)),
            "",
        )
        zone = values.get("data-zone") or values.get("data-zona") or None
        self._stack.append({"date": date_value, "title": title, "zone": zone, "text": []})

    def handle_data(self, data: str) -> None:
        if self._stack:
            self._stack[-1]["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if not self._stack:
            return
        node = self._stack.pop()
        text = " ".join(" ".join(node["text"]).split())
        if node["date"]:
            title = node["title"] or text
            if title:
                self.candidates.append((node["date"], title, node["zone"]))
        if self._stack and text:
            self._stack[-1]["text"].append(text)


class CBBOApiClient:
    """Read collection dates from a municipality page."""

    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def async_get_collections(self, municipality: str, zone: str) -> list[Collection]:
        url = f"{BASE_URL}/{municipality}"
        try:
            async with self._session.get(url, timeout=30, allow_redirects=True) as response:
                response.raise_for_status()
                body = await response.text()
        except (ClientError, TimeoutError) as err:
            raise CBBOApiError(f"Impossibile scaricare {url}: {err}") from err

        events = self._parse_events(body)
        if not events:
            raise CBBOApiError(
                "La pagina CBBO è stata scaricata, ma il calendario non è stato riconosciuto"
            )

        grouped: dict[date, list[tuple[str, str]]] = defaultdict(list)
        for event_day, raw_title, raw_zone in events:
            searchable_zone = f"{raw_title} {raw_zone or ''}".casefold()
            if municipality == "mazzano":
                if zone == ZONE_NORTH and re.search(r"\b(sud|zona sud)\b", searchable_zone):
                    continue
                if zone == ZONE_SOUTH and re.search(r"\b(nord|zona nord)\b", searchable_zone):
                    continue

            waste_type, label = normalize_title(raw_title)
            # Ignore page chrome and generic calendar controls.
            if waste_type == "other" and not _WASTE_WORDS.search(raw_title):
                continue
            pair = (waste_type, label)
            if pair not in grouped[event_day]:
                grouped[event_day].append(pair)

        collections = [
            Collection(
                day=day,
                waste_types=tuple(item[0] for item in items),
                labels=tuple(item[1] for item in items),
            )
            for day, items in sorted(grouped.items())
            if items
        ]
        if not collections:
            raise CBBOApiError("Il calendario CBBO non contiene raccolte utilizzabili")
        return collections

    @classmethod
    def _parse_events(cls, body: str) -> list[tuple[date, str, str | None]]:
        """Parse Drupal, FullCalendar and date-bearing HTML serialisations."""
        decoded = html.unescape(body).replace("\\/", "/")
        found: set[tuple[date, str, str | None]] = set()

        # Strict JSON objects embedded in scripts or Drupal settings.
        for match in re.finditer(r"\{[^{}]{0,4000}\}", decoded, re.S):
            blob = match.group(0)
            if not _DATE_RE.search(blob):
                continue
            try:
                obj: Any = json.loads(blob)
            except json.JSONDecodeError:
                continue
            found.update(cls._walk_json(obj))

        # Date-keyed JSON maps: "2026-07-31": ["Organico", "Carta"].
        for match in re.finditer(
            r'["\'](?P<date>20\d{2}-\d{2}-\d{2})["\']\s*:\s*(?P<value>\[[^\]]{1,1500}\]|["\'][^"\']+["\'])',
            decoded,
            re.S,
        ):
            day = match.group("date")
            value = match.group("value")
            titles = re.findall(r'["\']([^"\']+)["\']', value)
            for title in titles:
                parsed = cls._event_tuple(day, title, None)
                if parsed:
                    found.add(parsed)

        # HTML elements carrying data-date, datetime or equivalent attributes.
        parser = _CalendarHTMLParser()
        try:
            parser.feed(decoded)
        except Exception:
            pass
        for start, title, zone in parser.candidates:
            parsed = cls._event_tuple(start, title, zone)
            if parsed:
                found.add(parsed)

        # FullCalendar-like JavaScript objects that are not strict JSON.
        js_pattern = re.compile(
            r'(?:title|name|summary)\s*:\s*["\']([^"\']+)["\'][^{}]{0,900}?'
            r'(?:start|date|data)\s*:\s*["\'](20\d{2}-\d{2}-\d{2})[^"\']*["\']|'
            r'(?:start|date|data)\s*:\s*["\'](20\d{2}-\d{2}-\d{2})[^"\']*["\'][^{}]{0,900}?'
            r'(?:title|name|summary)\s*:\s*["\']([^"\']+)["\']',
            re.I | re.S,
        )
        for match in js_pattern.finditer(decoded):
            parsed = cls._event_tuple(
                match.group(2) or match.group(3),
                match.group(1) or match.group(4),
                None,
            )
            if parsed:
                found.add(parsed)

        # Last-resort: a bounded HTML block containing an ISO date and waste text.
        for match in re.finditer(r"<(?P<tag>div|td|li|article)\b[^>]*>.*?</(?P=tag)>", decoded, re.I | re.S):
            block = match.group(0)
            date_match = _DATE_RE.search(block)
            if not date_match or not _WASTE_WORDS.search(block):
                continue
            text = re.sub(r"<[^>]+>", " ", block)
            text = " ".join(html.unescape(text).split())
            for title in cls._extract_waste_titles(text):
                parsed = cls._event_tuple(date_match.group(0), title, None)
                if parsed:
                    found.add(parsed)

        return sorted(found, key=lambda item: (item[0], item[1]))

    @classmethod
    def _walk_json(cls, value: Any) -> set[tuple[date, str, str | None]]:
        found: set[tuple[date, str, str | None]] = set()
        if isinstance(value, dict):
            start = value.get("start") or value.get("date") or value.get("data") or value.get("datetime")
            title = value.get("title") or value.get("name") or value.get("summary") or value.get("label")
            zone = value.get("zone") or value.get("zona") or value.get("description")
            parsed = cls._event_tuple(start, title, zone)
            if parsed:
                found.add(parsed)
            for key, child in value.items():
                if isinstance(key, str) and _DATE_RE.fullmatch(key):
                    if isinstance(child, str):
                        parsed = cls._event_tuple(key, child, None)
                        if parsed:
                            found.add(parsed)
                    elif isinstance(child, list):
                        for item in child:
                            if isinstance(item, str):
                                parsed = cls._event_tuple(key, item, None)
                                if parsed:
                                    found.add(parsed)
                found.update(cls._walk_json(child))
        elif isinstance(value, list):
            for child in value:
                found.update(cls._walk_json(child))
        return found

    @staticmethod
    def _extract_waste_titles(text: str) -> Iterable[str]:
        known = (
            "Frazione organica", "Organico", "Imballaggi in plastica", "Plastica",
            "Carta e cartone", "Vetro e lattine", "Vetro", "Rifiuti non differenziabili",
            "Rifiuto non riciclabile", "Indifferenziato", "Tessili sanitari", "Verde",
            "Sfalci e ramaglie",
        )
        lower = text.casefold()
        for title in known:
            if title.casefold() in lower:
                yield title

    @staticmethod
    def _event_tuple(start: Any, title: Any, zone: Any) -> tuple[date, str, str | None] | None:
        if not isinstance(start, str) or not isinstance(title, str):
            return None
        match = _DATE_RE.search(start)
        if not match:
            return None
        try:
            event_day = datetime.strptime(match.group(0), "%Y-%m-%d").date()
        except ValueError:
            return None
        clean_title = re.sub(r"<[^>]+>", " ", title)
        clean_title = " ".join(html.unescape(clean_title).split()).strip(" -–—")
        if not clean_title or clean_title.casefold() in {"oggi", "mese", "settimana", "giorno"}:
            return None
        clean_zone = " ".join(str(zone).split()) if zone else None
        return event_day, clean_title, clean_zone
