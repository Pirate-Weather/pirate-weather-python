from enum import Enum


class Units(str, Enum):
    AUTO = "auto"
    CA = "ca"
    UK2 = "uk2"
    US = "us"
    SI = "si"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
