"""Air quality index scales."""

from enum import StrEnum


class AQIUnits(StrEnum):
    """Air quality index scales that can be selected with the ``aqiunits`` parameter."""

    UK = "uk"
    EU = "eu"
    CA = "ca"
    US = "us"
    HK = "hk"
    IE = "ie"
    IL = "il"
    ID = "id"
    CN = "cn"
    MY = "my"
    VN = "vn"

    @classmethod
    def list(cls):
        """Return the values of every member."""
        return [c.value for c in cls]
