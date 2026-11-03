"""Incident classification rules shared by the incident list and the statistics."""

from collections.abc import Callable

from dgt_monitor.core.models import Incident

WEATHER_WORDS = ("weather", "fog", "snow", "flooding", "ice", "rain")


def is_accident(incident: Incident) -> bool:
    return "accident" in incident.cause.casefold()


def is_roadworks(incident: Incident) -> bool:
    cause = incident.cause.casefold()
    return "roadworks" in cause or "maintenance" in cause


def is_breakdown(incident: Incident) -> bool:
    cause = incident.cause.casefold()
    return "stuck" in cause or "breakdown" in cause


def is_obstruction(incident: Incident) -> bool:
    return "obstruction" in incident.cause.casefold()


def is_weather(incident: Incident) -> bool:
    cause = incident.cause.casefold()
    return any(word in cause for word in WEATHER_WORDS)


# Indicator key -> predicate. "total" is handled separately because it counts everything.
INDICATOR_RULES: dict[str, Callable[[Incident], bool]] = {
    "accidents": is_accident,
    "roadworks": is_roadworks,
    "breakdowns": is_breakdown,
    "obstructions": is_obstruction,
    "weather": is_weather,
}
