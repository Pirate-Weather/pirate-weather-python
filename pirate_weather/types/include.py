"""Optional data blocks that can be added to a response."""

from enum import StrEnum


class Include(StrEnum):
    """Optional data blocks that can be added with the ``include`` parameter."""

    DAY_NIGHT_FORECAST = "day_night_forecast"
    AI_MODELS = "aimodels"
    AIR_QUALITY_DETAILS = "airqualitydetails"

    @classmethod
    def list(cls):
        """Return the values of every member."""
        return [c.value for c in cls]
