"""Data blocks returned by the API."""

from enum import StrEnum


class Weather(StrEnum):
    """Data blocks that can be passed to the ``exclude`` parameter."""

    CURRENTLY = "currently"
    MINUTELY = "minutely"
    HOURLY = "hourly"
    DAILY = "daily"
    ALERTS = "alerts"
    FLAGS = "flags"
    SUMMARY = "summary"

    @classmethod
    def list(cls):
        """Return the values of every member."""
        return [c.value for c in cls]
