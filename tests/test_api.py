"""Tests for the request parameters sent by the API clients."""

import asyncio
import copy
from datetime import UTC, datetime
from unittest import mock
from unittest.mock import AsyncMock

import aiohttp

from pirate_weather.api import BasePirateWeather, PirateWeather, PirateWeatherAsync
from pirate_weather.types.aqi_units import AQIUnits
from pirate_weather.types.extra_vars import ExtraVars
from pirate_weather.types.icons import Icons
from pirate_weather.types.include import Include
from pirate_weather.types.languages import Languages
from pirate_weather.types.sources import Sources
from pirate_weather.types.units import Units
from pirate_weather.types.weather import Weather

from . import mokcs
from .data import DATA


def test_build_params_defaults():
    """Only the language and units are sent by default."""
    params = BasePirateWeather.build_params()
    assert params == {"lang": "en", "units": "auto"}


def test_build_params_all_options():
    """Every option is converted to its API query parameter."""
    params = BasePirateWeather.build_params(
        extend=True,
        lang=Languages.FRENCH,
        values_units=Units.CA,
        exclude=[Weather.MINUTELY, Weather.SUMMARY, Sources.HRRR],
        timezone="UTC",
        version=2,
        include=[Include.DAY_NIGHT_FORECAST, Include.AIR_QUALITY_DETAILS],
        extra_vars=[ExtraVars.STATION_PRESSURE],
        icon=Icons.PIRATE,
        aqi_units=AQIUnits.CA,
    )
    assert params == {
        "extend": "hourly",
        "lang": "fr",
        "units": "ca",
        "exclude": "minutely,summary,hrrr",
        "timezone": "UTC",
        "version": 2,
        "include": "day_night_forecast,airqualitydetails",
        "extraVars": "stationPressure",
        "icon": "pirate",
        "aqiunits": "ca",
    }


def test_build_params_accepts_plain_strings():
    """Plain strings are accepted in place of enums."""
    params = BasePirateWeather.build_params(
        include=["aimodels"], icon="pirate", aqi_units="eu"
    )
    assert params["include"] == "aimodels"
    assert params["icon"] == "pirate"
    assert params["aqiunits"] == "eu"


def test_build_params_empty_lists_are_dropped():
    """Empty lists are not sent to the API."""
    params = BasePirateWeather.build_params(exclude=[], include=[], extra_vars=[])
    assert "exclude" not in params
    assert "include" not in params
    assert "extraVars" not in params


def test_get_forecast_sends_new_params():
    """The new v3 parameters are passed to the HTTP request."""
    with mock.patch("requests.Session", mokcs.MockSession):
        pirate_weather = PirateWeather("api_key")
        with mock.patch.object(
            pirate_weather.request_manager.session,
            "get",
            wraps=pirate_weather.request_manager.session.get,
        ) as get:
            pirate_weather.get_forecast(
                DATA["latitude"],
                DATA["longitude"],
                version=2,
                include=[Include.AIR_QUALITY_DETAILS],
                extra_vars=[ExtraVars.STATION_PRESSURE],
                icon=Icons.PIRATE,
                aqi_units=AQIUnits.US,
            )

    params = get.call_args.kwargs["params"]
    assert params["version"] == 2
    assert params["include"] == "airqualitydetails"
    assert params["extraVars"] == "stationPressure"
    assert params["icon"] == "pirate"
    assert params["aqiunits"] == "us"


TIME = datetime(2026, 11, 1, 12, tzinfo=UTC)
TIME_MACHINE_URL = (
    f"https://timemachine.pirateweather.net/forecast/api_key/"
    f"{DATA['latitude']},{DATA['longitude']},{int(TIME.timestamp())}"
)


def test_time_machine_forecast_uses_time_machine_url():
    """The sync time machine request goes to the time machine host."""
    with mock.patch("requests.Session", mokcs.MockSession):
        pirate_weather = PirateWeather("api_key")
        with mock.patch.object(
            pirate_weather.request_manager.session,
            "get",
            wraps=pirate_weather.request_manager.session.get,
        ) as get:
            pirate_weather.get_time_machine_forecast(
                DATA["latitude"], DATA["longitude"], TIME
            )

    assert get.call_args.args[0] == TIME_MACHINE_URL


def test_async_time_machine_forecast_uses_time_machine_url():
    """The async time machine request goes to the time machine host."""

    async def get_forecast():
        pirate_weather = PirateWeatherAsync("api_key")
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=copy.deepcopy(DATA))
        mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
        mock_resp.__aexit__ = AsyncMock(return_value=None)

        async with aiohttp.ClientSession() as session:
            with mock.patch.object(session, "get", return_value=mock_resp) as get:
                await pirate_weather.get_time_machine_forecast(
                    DATA["latitude"], DATA["longitude"], TIME, client_session=session
                )
        return get

    get = asyncio.run(get_forecast())
    assert get.call_args.args[0] == TIME_MACHINE_URL
