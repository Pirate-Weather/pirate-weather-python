from enum import Enum


class Units(str, Enum):
    AUTO = "auto"
    CA = "ca"
    UK = "uk"
    US = "us"
    SI = "si"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
