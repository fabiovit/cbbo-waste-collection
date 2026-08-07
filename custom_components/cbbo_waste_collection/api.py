"""HTTP client and parser for public CBBO municipality pages."""
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from datetime import date, datetime
from html.parser import HTMLParser
from typing import Any

from aiohttp import ClientError, ClientSession, ClientTimeout

from .const import BASE_URL, ZONE_NORTH, ZONE_SOUTH
from .schedule import Collection, OTHER, normalize_title

_DATE_RE = re.compile(r"20\d{2}-\d{2}-\d{2}")
_WASTE_RE = re.compile(
    r"organ|umido|plastic|carta|cartone|vetro|lattin|indifferenzi|"
    r"non riciclab|non differenziab|secco residuo|tessili sanitari|"
    r"pannolin|pannolon|verde|sfalci|ramaglie",
    re.I,
)


class CBBOApiError(Exception):
    """Raised when data cannot be downloaded or parsed."""


class _Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[dict[str, Any]] = []
        self.items: list[tuple[str, str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.casefold(): value or "" for key, value in attrs}
        inherited_date = self.stack[-1]["date"] if self.stack else ""
        date_value = next(
            (
                values.get(key, "")
                for key in ("data-date", "data-start", "datetime", "date", "start")
                if _DATE_RE.search(values.get(key, ""))
            ),
            inherited_date,
        )
        title = next(
            (
                values.get(key, "")
                for key in ("data-title", "data-event", "title", "aria-label")
                if values.get(key)
            ),
            "",
        )
        zone = values.get("data-zone") or values.get("data-zona") or None
        self.stack.append({"date": date_value, "title": title, "zone": zone, "text": []})

    def handle_data(self, data: str) -> None:
        if self.stack:
            self.stack[-1]["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            return
        node = self.stack.pop()
        text = " ".join(" ".join(node["text"]).split())
        if node["date"] and (node["title"] or text):
            self.items.append((node["date"], node["title"] or text, node["zone"]))
        if self.stack and text:
            self.stack[-1]["text"].append(text)


class CBBOApiClient:
    def __init__(self, session: ClientSession) -> None:
        self._session = session
        self.last_pdf_url: str | None = None

    async def async_get_collections(self, municipality: str, zone: str) -> list[Collection]:
        url = f"{BASE_URL}/{municipality}"
        try:
            async with self._session.get(
                url,
                timeout=ClientTimeout(total=30),
                allow_redirects=True,
                headers={
                    "Accept-Language": "it-IT,it;q=0.9",
                    "User-Agent": "HomeAssistant-CBBO-Waste-Collection/1.0",
                },
            ) as response:
                response.raise_for_status()
                body = await response.text()
        except (ClientError, TimeoutError) as err:
            raise CBBOApiError(f"Download non riuscito: {err}") from err

        self.last_pdf_url = self.discover_ecocalendar_url(body)
        events = self.parse_events(body)
        grouped: dict[date, list[tuple[str, str]]] = defaultdict(list)

        for day, title, event_zone in events:
            searchable = f"{title} {event_zone or ''}".casefold()
            if municipality == "mazzano":
                if zone == ZONE_NORTH and re.search(r"\b(zona )?sud\b", searchable):
                    continue
                if zone == ZONE_SOUTH and re.search(r"\b(zona )?nord\b", searchable):
                    continue

            waste_type, label = normalize_title(title)
            if waste_type == OTHER and not _WASTE_RE.search(title):
                continue
            pair = (waste_type, label)
            if pair not in grouped[day]:
                grouped[day].append(pair)

        result = [
            Collection(
                day,
                tuple(item[0] for item in values),
                tuple(item[1] for item in values),
            )
            for day, values in sorted(grouped.items())
            if values
        ]
        if not result:
            raise CBBOApiError("Calendario non riconosciuto nella pagina CBBO")
        return result

    @staticmethod
    def discover_ecocalendar_url(body: str) -> str | None:
        """Return the Ecocalendario PDF URL advertised on a municipality page."""
        text = html.unescape(body).replace("\\/", "/")
        matches = re.findall(r"href=[\"']([^\"']+\.pdf(?:\?[^\"']*)?)[\"']", text, re.I)
        preferred = [item for item in matches if "ecocalend" in item.casefold()]
        if not preferred:
            return None
        value = preferred[0]
        if value.startswith("//"):
            return "https:" + value
        if value.startswith("/"):
            return BASE_URL + value
        if value.startswith("http://") or value.startswith("https://"):
            return value
        return BASE_URL + "/" + value.lstrip("/")

    @classmethod
    def parse_events(cls, body: str) -> list[tuple[date, str, str | None]]:
        text = html.unescape(body).replace("\\/", "/")
        found: set[tuple[date, str, str | None]] = set()

        script_pattern = re.compile(
            r'''<script[^>]*type=["']application/(?:ld\+)?json["'][^>]*>(.*?)</script>''',
            re.I | re.S,
        )
        for match in script_pattern.finditer(text):
            try:
                found.update(cls._walk_json(json.loads(match.group(1))))
            except (json.JSONDecodeError, TypeError):
                pass

        for match in re.finditer(
            r"\{[^{}]{0,5000}20\d{2}-\d{2}-\d{2}[^{}]{0,5000}\}", text, re.S
        ):
            try:
                found.update(cls._walk_json(json.loads(match.group(0))))
            except json.JSONDecodeError:
                pass

        date_map_pattern = re.compile(
            r'''["'](?P<date>20\d{2}-\d{2}-\d{2})["']\s*:\s*'''
            r'''(?P<value>\[[^]]{1,2000}\]|["'][^"']+["'])''',
            re.S,
        )
        for match in date_map_pattern.finditer(text):
            for title in re.findall(r'''["']([^"']+)["']''', match.group("value")):
                event = cls._event(match.group("date"), title, None)
                if event:
                    found.add(event)

        parser = _Parser()
        try:
            parser.feed(text)
        except Exception:
            pass
        for start, title, zone in parser.items:
            event = cls._event(start, title, zone)
            if event:
                found.add(event)

        fullcalendar_pattern = re.compile(
            r'''(?:title|name|summary|label)\s*:\s*["']([^"']+)["']'''
            r'''[^{}]{0,1200}?(?:start|date|data|datetime)\s*:\s*["']'''
            r'''(20\d{2}-\d{2}-\d{2})[^"']*["']|'''
            r'''(?:start|date|data|datetime)\s*:\s*["']'''
            r'''(20\d{2}-\d{2}-\d{2})[^"']*["'][^{}]{0,1200}?'''
            r'''(?:title|name|summary|label)\s*:\s*["']([^"']+)["']''',
            re.I | re.S,
        )
        for match in fullcalendar_pattern.finditer(text):
            event = cls._event(
                match.group(2) or match.group(3),
                match.group(1) or match.group(4),
                None,
            )
            if event:
                found.add(event)

        return sorted(found, key=lambda item: (item[0], item[1]))

    @classmethod
    def _walk_json(cls, value: Any) -> set[tuple[date, str, str | None]]:
        found: set[tuple[date, str, str | None]] = set()
        if isinstance(value, dict):
            start = next(
                (
                    value.get(key)
                    for key in ("start", "date", "data", "datetime", "startDate")
                    if value.get(key)
                ),
                None,
            )
            title = next(
                (
                    value.get(key)
                    for key in ("title", "name", "summary", "label", "description")
                    if value.get(key)
                ),
                None,
            )
            zone = value.get("zone") or value.get("zona")
            event = cls._event(start, title, zone)
            if event:
                found.add(event)

            for key, child in value.items():
                if isinstance(key, str) and _DATE_RE.fullmatch(key):
                    values = child if isinstance(child, list) else [child]
                    for item in values:
                        if isinstance(item, str):
                            event = cls._event(key, item, None)
                            if event:
                                found.add(event)
                        elif isinstance(item, dict):
                            found.update(cls._walk_json({**item, "date": key}))
                found.update(cls._walk_json(child))
        elif isinstance(value, list):
            for child in value:
                found.update(cls._walk_json(child))
        return found

    @staticmethod
    def _event(start: Any, title: Any, zone: Any) -> tuple[date, str, str | None] | None:
        if not isinstance(start, str) or not isinstance(title, str):
            return None
        match = _DATE_RE.search(start)
        if not match:
            return None
        try:
            day = datetime.strptime(match.group(), "%Y-%m-%d").date()
        except ValueError:
            return None
        clean = " ".join(re.sub(r"<[^>]+>", " ", title).split())
        if not clean:
            return None
        return day, clean, str(zone) if zone is not None else None
