from enum import Enum


class Weather(str, Enum):
    CURRENTLY = "currently"
    MINUTELY = "minutely"
    HOURLY = "hourly"
    DAILY = "daily"
    ALERTS = "alerts"
    FLAGS = "flags"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
