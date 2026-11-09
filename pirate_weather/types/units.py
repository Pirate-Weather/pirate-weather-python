"""Unit systems supported by the API."""

from enum import StrEnum


class Units(StrEnum):
    """Unit systems supported by the ``units`` parameter."""

    AUTO = "auto"
    CA = "ca"
    UK = "uk"
    US = "us"
    SI = "si"

    @classmethod
    def list(cls):
        """Return the values of every member."""
        return [c.value for c in cls]
