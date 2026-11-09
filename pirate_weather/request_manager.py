"""HTTP request managers for the synchronous and asynchronous clients."""

import requests
from aiohttp import ClientSession

from .exceptions import PirateWeatherException


class BaseRequestManger:
    """Base class holding the request headers."""

    def __init__(self, gzip: bool):
        """Set the request headers, asking for gzip compression if enabled."""
        self.headers = {} if not gzip else {"Accept-Encoding": "gzip"}

    def make_request(self, url: str, **params):
        """Request ``url`` with ``params`` and return the decoded JSON."""
        raise NotImplementedError


class RequestManger(BaseRequestManger):
    """Request manager using a ``requests`` session."""

    def __init__(self, gzip: bool):
        """Create the ``requests`` session."""
        super().__init__(gzip)
        self.session = requests.Session()
        self.session.headers = self.headers

    def make_request(self, url: str, **params):
        """Request ``url`` with ``params`` and return the decoded JSON."""
        response = self.session.get(url, params=params)
        response_json = response.json()
        if response.status_code != 200:
            raise PirateWeatherException(response.status_code, response.text)
        response_json["timezone"] = params.get("timezone") or response_json["timezone"]
        return response_json


class RequestMangerAsync(BaseRequestManger):
    """Request manager using an ``aiohttp`` client session."""

    async def make_request(self, url: str, session: ClientSession, **params):
        """Request ``url`` with ``params`` and return the decoded JSON."""
        assert isinstance(session, ClientSession)

        for key in list(params.keys()):
            if params[key] is None:
                del params[key]
            elif isinstance(params[key], list):
                params[key] = ",".join(params[key])

        async with session.get(url, params=params, headers=self.headers) as resp:
            response = await resp.json()
            if resp.status != 200:
                raise PirateWeatherException(resp.status, response)
        response["timezone"] = params.get("timezone") or response["timezone"]
        return response
