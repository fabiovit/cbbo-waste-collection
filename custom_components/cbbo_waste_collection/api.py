"""HTTP client and calendar parser for the public CBBO website."""
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from datetime import date, datetime
from typing import Any

from aiohttp import ClientError, ClientSession

from .const import BASE_URL, ZONE_NORTH, ZONE_SOUTH
from .schedule import Collection, normalize_title

_DATE_RE = r"20\d{2}-\d{2}-\d{2}"


class CBBOApiError(Exception):
    """Raised when CBBO data cannot be downloaded or parsed."""


class CBBOApiClient:
    """Read collection dates from a municipality page."""

    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def async_get_collections(self, municipality: str, zone: str) -> list[Collection]:
        url = f"{BASE_URL}/{municipality}"
        try:
            async with self._session.get(url, timeout=30) as response:
                response.raise_for_status()
                body = await response.text()
        except (ClientError, TimeoutError) as err:
            raise CBBOApiError(f"Impossibile scaricare {url}: {err}") from err

        events = self._parse_events(body)
        if not events:
            raise CBBOApiError("La pagina CBBO non contiene eventi calendario riconoscibili")

        grouped: dict[date, list[tuple[str, str]]] = defaultdict(list)
        for event_day, raw_title, raw_zone in events:
            if municipality == "mazzano" and raw_zone:
                zone_text = raw_zone.casefold()
                if zone == ZONE_NORTH and "sud" in zone_text:
                    continue
                if zone == ZONE_SOUTH and "nord" in zone_text:
                    continue
            waste_type, label = normalize_title(raw_title)
            pair = (waste_type, label)
            if pair not in grouped[event_day]:
                grouped[event_day].append(pair)

        return [
            Collection(
                day=day,
                waste_types=tuple(item[0] for item in items),
                labels=tuple(item[1] for item in items),
            )
            for day, items in sorted(grouped.items())
        ]

    @staticmethod
    def _parse_events(body: str) -> list[tuple[date, str, str | None]]:
        """Parse several common FullCalendar/Drupal serialisations.

        CBBO may change the exact markup, so this deliberately supports JSON
        objects, data attributes and ISO-date table cells.
        """
        decoded = html.unescape(body).replace("\\/", "/")
        found: set[tuple[date, str, str | None]] = set()

        # JSON event objects. Property order is not assumed.
        for match in re.finditer(r"\{[^{}]{0,1500}\}", decoded, re.S):
            blob = match.group(0)
            if not re.search(_DATE_RE, blob):
                continue
            try:
                obj: Any = json.loads(blob)
            except json.JSONDecodeError:
                obj = None
            if isinstance(obj, dict):
                start = obj.get("start") or obj.get("date") or obj.get("data")
                title = obj.get("title") or obj.get("name") or obj.get("summary")
                zone = obj.get("zone") or obj.get("zona") or obj.get("description")
                parsed = CBBOApiClient._event_tuple(start, title, zone)
                if parsed:
                    found.add(parsed)

        # data-date/data-title attributes in either order.
        attr_patterns = (
            rf'data-(?:date|start)=["\']({_DATE_RE})[^"\']*["\'][^>]*data-(?:title|event)=["\']([^"\']+)["\']',
            rf'data-(?:title|event)=["\']([^"\']+)["\'][^>]*data-(?:date|start)=["\']({_DATE_RE})[^"\']*["\']',
        )
        for index, pattern in enumerate(attr_patterns):
            for match in re.finditer(pattern, decoded, re.I | re.S):
                start, title = match.groups() if index == 0 else (match.group(2), match.group(1))
                parsed = CBBOApiClient._event_tuple(start, title, None)
                if parsed:
                    found.add(parsed)

        # FullCalendar-like JS objects that are not strict JSON.
        js_pattern = re.compile(
            rf'(?:title|name)\s*:\s*["\']([^"\']+)["\'][^{{}}]{{0,500}}?'
            rf'(?:start|date)\s*:\s*["\']({_DATE_RE})[^"\']*["\']|'
            rf'(?:start|date)\s*:\s*["\']({_DATE_RE})[^"\']*["\'][^{{}}]{{0,500}}?'
            rf'(?:title|name)\s*:\s*["\']([^"\']+)["\']',
            re.I | re.S,
        )
        for match in js_pattern.finditer(decoded):
            title = match.group(1) or match.group(4)
            start = match.group(2) or match.group(3)
            parsed = CBBOApiClient._event_tuple(start, title, None)
            if parsed:
                found.add(parsed)

        return sorted(found, key=lambda item: (item[0], item[1]))

    @staticmethod
    def _event_tuple(start: Any, title: Any, zone: Any) -> tuple[date, str, str | None] | None:
        if not isinstance(start, str) or not isinstance(title, str):
            return None
        match = re.search(_DATE_RE, start)
        if not match:
            return None
        try:
            event_day = datetime.strptime(match.group(0), "%Y-%m-%d").date()
        except ValueError:
            return None
        clean_title = re.sub(r"<[^>]+>", " ", title)
        clean_title = " ".join(html.unescape(clean_title).split())
        if not clean_title or clean_title.casefold() in {"oggi", "mese", "settimana", "giorno"}:
            return None
        clean_zone = " ".join(str(zone).split()) if zone else None
        return event_day, clean_title, clean_zone
