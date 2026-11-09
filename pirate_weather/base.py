"""Base classes used to build forecast objects from API responses."""

from datetime import datetime

import pytz

from .utils import get_datetime_from_unix, undo_snake_case_key


class BaseWeather:
    """A data block made up of a summary, an icon and a list of data points."""

    summary: str
    icon: str
    data_class: object

    def __init__(self, summary=None, icon=None, data=None, timezone=None):
        """Build the data points of the block using ``data_class``."""
        self.summary = summary
        self.icon = icon

        assert self.data_class is not None
        self.data = [
            self.data_class(timezone=timezone, **item) for item in (data or [])
        ]

    def __repr__(self):
        """Return the class name and the number of data points."""
        return f"{self.__class__.__name__}([{len(self.data)}])"

    def __iter__(self):
        """Iterate over the data points."""
        return iter(self.data)


class AutoInit:
    """Set every annotated attribute from the matching camelCase API field."""

    def __init__(self, **params):
        """Populate the annotated fields from the API response ``params``."""
        try:
            timezone = pytz.timezone(params.pop("timezone", None))
        except (pytz.UnknownTimeZoneError, AttributeError, TypeError):
            timezone = pytz.UTC

        for field in getattr(self.__class__, "__annotations__", {}):
            api_field = undo_snake_case_key(field)
            annotations = getattr(self.__class__, "__annotations__", {})
            if annotations.get(field) == datetime:
                params[api_field] = get_datetime_from_unix(
                    params.get(api_field), timezone
                )

            if api_field in params:
                setattr(self, field, params.get(api_field))
            else:
                setattr(self, field, None)

    def __iter__(self):
        """Iterate over ``(field, value)`` pairs."""
        return iter(self.__dict__.items())

    def __repr__(self):
        """Return the class name and the time of the data point."""
        return f"{self.__class__.__name__}({getattr(self, 'time', '')})"
