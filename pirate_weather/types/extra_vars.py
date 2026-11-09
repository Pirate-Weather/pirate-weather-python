"""Hidden variables that can be added to a response."""

from enum import StrEnum


class ExtraVars(StrEnum):
    """Hidden variables that can be requested with the ``extraVars`` parameter."""

    STATION_PRESSURE = "stationPressure"

    @classmethod
    def list(cls):
        """Return the values of every member."""
        return [c.value for c in cls]
