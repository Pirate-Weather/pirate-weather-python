import json

import requests
from aiohttp import ClientSession

from .exceptions import PirateWeatherException


class BaseRequestManger:
    def __init__(self, gzip: bool):
        self.headers = {} if not gzip else {"Accept-Encoding": "gzip"}

    def make_request(self, url: str, **params):
        raise NotImplementedError


class RequestManger(BaseRequestManger):
    def __init__(self, gzip: bool):
        super().__init__(gzip)
        self.session = requests.Session()
        self.session.headers = self.headers

    def make_request(self, url: str, **params):
        response = self.session.get(url, params=params)
        response_json = response.json()
        if response.status_code != 200:
            raise PirateWeatherException(response.status_code, response.text)
        response_json["timezone"] = params.get("timezone") or response_json["timezone"]
        return response_json


class RequestMangerAsync(BaseRequestManger):
    async def make_request(self, url: str, session: ClientSession, **params):
        assert isinstance(session, ClientSession)

        for key in list(params.keys()):
            if params[key] is None:
                del params[key]
            elif isinstance(params[key], list):
                params[key] = ",".join(params[key])

        async with session.get(url, params=params, headers=self.headers) as resp:
            response = await resp.json()
            if resp.status != 200:
                raise PirateWeatherException(resp.status, json.loads(resp._body))
        response["timezone"] = params.get("timezone") or response["timezone"]
        return response
