"""Exceptions raised by the Pirate Weather library."""


class PirateWeatherException(Exception):
    """Raised when the API returns a non 200 status code."""

    def __init__(self, code, msg):  # pylint: disable=W0231
        """Store the HTTP status code and the error message."""
        self.code = code
        self.msg = msg

    def __str__(self):
        """Return the status code and message."""
        return f"Error[{self.code}]: {self.msg}"
