"""Mocks used in place of the HTTP clients."""

import copy

from .data import DATA


class MockSession:
    """Stand-in for ``requests.Session`` returning the sample response."""

    def __init__(self):
        """Set the attributes the request manager uses."""
        self.headers = {}
        self.auth = None
        self.mock_json = None
        self.status_code = 200

    def get(self, url, params=None):
        """Return the session itself so ``json`` can be called on the response."""
        return self

    def json(self):  # pylint: disable=R0201
        """Return a copy of the sample API response."""
        return copy.deepcopy(DATA)
