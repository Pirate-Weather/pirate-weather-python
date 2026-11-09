"""Icon sets returned by the API."""

from enum import StrEnum


class Icons(StrEnum):
    """Icon sets that can be selected with the ``icon`` parameter."""

    PIRATE = "pirate"

    @classmethod
    def list(cls):
        """Return the values of every member."""
        return [c.value for c in cls]
