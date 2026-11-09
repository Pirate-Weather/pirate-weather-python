"""Tests for parsing an API response into a Forecast."""

import asyncio
import copy
import os
import sys
from datetime import datetime
from unittest import mock
from unittest.mock import AsyncMock

import aiohttp
import pytest

from pirate_weather.api import PirateWeather, PirateWeatherAsync
from pirate_weather.forecast import Forecast
from pirate_weather.utils import get_datetime_from_unix

from . import mokcs, utils
from .data import DATA

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def forecast_sync():
    """Return a forecast fetched with the synchronous client."""
    with mock.patch("requests.Session", mokcs.MockSession):
        pirate_weather = PirateWeather("api_key")
        return pirate_weather.get_forecast(DATA["latitude"], DATA["longitude"])


@pytest.fixture
def forecast_async():
    """Return a forecast fetched with the asynchronous client."""

    async def get_async_data():
        pirate_weather = PirateWeatherAsync("api_key")

        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=copy.deepcopy(DATA))
        mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
        mock_resp.__aexit__ = AsyncMock(return_value=None)

        async with aiohttp.ClientSession() as session:
            with mock.patch.object(session, "get", return_value=mock_resp):
                result = await pirate_weather.get_forecast(
                    DATA["latitude"],
                    DATA["longitude"],
                    client_session=session,
                )

        return result

    return asyncio.run(get_async_data())


@pytest.fixture(params=["sync", "async"])
def forecast(request, forecast_sync, forecast_async):
    """Return the forecast from the sync and async clients."""
    if request.param == "sync":
        return forecast_sync
    return forecast_async


def test_forecast_base_fields(forecast):
    """The top level fields are parsed."""
    assert isinstance(forecast, Forecast)
    assert forecast.latitude == DATA["latitude"]
    assert forecast.longitude == DATA["longitude"]
    assert forecast.timezone == DATA["timezone"]


def test_forecast_currently(forecast):
    """Every field of the currently block is parsed."""
    f_item, d_item = forecast.currently, copy.deepcopy(DATA["currently"])
    for key in d_item:
        forecast_key = utils.snake_case_key(key)
        if isinstance(getattr(f_item, forecast_key), datetime):
            d_item[key] = get_datetime_from_unix(d_item[key])
        assert hasattr(f_item, forecast_key)
        assert getattr(f_item, forecast_key) == d_item[key]


def test_forecast_minutely(forecast):
    """Every field of the minutely block is parsed."""
    assert forecast.minutely.summary == DATA["minutely"]["summary"]
    assert forecast.minutely.icon == DATA["minutely"]["icon"]

    for f_item, d_item in zip(
        forecast.minutely.data, copy.deepcopy(DATA["minutely"]["data"]), strict=False
    ):
        for key in d_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(f_item, forecast_key), datetime):
                d_item[key] = get_datetime_from_unix(d_item[key])
            assert hasattr(f_item, forecast_key)
            assert getattr(f_item, forecast_key) == d_item[key]


def test_forecast_hourly(forecast):
    """Every field of the hourly block is parsed."""
    assert forecast.hourly.summary == DATA["hourly"]["summary"]
    assert forecast.hourly.icon == DATA["hourly"]["icon"]

    for f_item, d_item in zip(
        forecast.hourly.data, copy.deepcopy(DATA["hourly"]["data"]), strict=False
    ):
        for key in d_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(f_item, forecast_key), datetime):
                d_item[key] = get_datetime_from_unix(d_item[key])
            assert hasattr(f_item, forecast_key)
            assert getattr(f_item, forecast_key) == d_item[key]


def test_forecast_daily(forecast):
    """Every field of the daily block is parsed."""
    assert forecast.daily.summary == DATA["daily"]["summary"]
    assert forecast.daily.icon == DATA["daily"]["icon"]

    for f_item, d_item in zip(
        forecast.daily.data, copy.deepcopy(DATA["daily"]["data"]), strict=False
    ):
        for key in d_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(f_item, forecast_key), datetime):
                d_item[key] = get_datetime_from_unix(d_item[key])
            assert hasattr(f_item, forecast_key)
            assert getattr(f_item, forecast_key) == d_item[key]


def test_forecast_day_night(forecast):
    """Every field of the day_night block is parsed."""
    for f_item, d_item in zip(
        forecast.day_night.data, copy.deepcopy(DATA["day_night"]["data"]), strict=False
    ):
        for key in d_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(f_item, forecast_key), datetime):
                d_item[key] = get_datetime_from_unix(d_item[key])
            assert hasattr(f_item, forecast_key)
            assert getattr(f_item, forecast_key) == d_item[key]


def test_forecast_alerts(forecast):
    """Every field of the alerts are parsed."""
    for f_item, d_item in zip(
        forecast.alerts, copy.deepcopy(DATA["alerts"]), strict=False
    ):
        for key in d_item:
            forecast_key = utils.snake_case_key(key)
            if isinstance(getattr(f_item, forecast_key), datetime):
                d_item[key] = get_datetime_from_unix(d_item[key])
            assert hasattr(f_item, forecast_key)
            assert getattr(f_item, forecast_key) == d_item[key]


def test_forecast_flags(forecast):
    """Every field of the flags block is parsed."""
    d_item = copy.deepcopy(DATA["flags"])
    f_item = forecast.flags
    for key in d_item:
        forecast_key = utils.snake_case_key(key)
        if isinstance(getattr(f_item, forecast_key), datetime):
            d_item[key] = get_datetime_from_unix(d_item[key])
        assert hasattr(f_item, forecast_key)
        assert getattr(f_item, forecast_key) == d_item[key]


def test_forecast_v3_fields(forecast):
    """The new API v3 fields are exposed as snake_case attributes."""
    currently = forecast.currently
    assert currently.air_quality_index == 6
    assert currently.pm25 == 19.4
    assert currently.no2_concentration == 24.6
    assert currently.lifted_index == 11
    assert currently.k_index == 17
    assert currently.convective_inhibition == -2

    day = forecast.daily.data[0]
    assert day.air_quality_index_max == 6
    assert day.lifted_index_min == 3
    assert day.k_index_max_time == 1794279600
    assert day.vertical_velocity_min == -1.2

    assert forecast.flags.version == "V3.0.0a5"
    assert forecast.flags.source_i_d_x["dwd_mosmix"]["stations"][0]["id"] == "71892"
