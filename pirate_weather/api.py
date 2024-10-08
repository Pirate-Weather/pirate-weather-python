from datetime import datetime
from enum import Enum

import aiohttp
import pytz

from .forecast import Forecast
from .request_manager import BaseRequestManger, RequestManger, RequestMangerAsync
from .types.languages import Languages
from .types.units import Units
from .types.weather import Weather


class PirateWeatherApiVersion(str, Enum):
    BASE = "https://api.pirateweather.net/forecast"
    TIME_MACHINE = "https://timemachine.pirateweather.net/forecast"


class BasePirateWeather:
    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.request_manager: BaseRequestManger = None

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        extend: bool = None,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: [Weather] = None,
        timezone: str = None,
    ):
        raise NotImplementedError

    def get_time_machine_forecast(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        extend: bool = False,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: [Weather] = None,
        timezone: str = None,
    ):
        raise NotImplementedError

    @staticmethod
    def convert_exclude_param_to_string(exclude: list[Weather] | None):
        if exclude:
            exclude = [ex.value for ex in exclude]
            exclude = ",".join(exclude)
        return exclude

    def get_url(
        self,
        latitude: float,
        longitude: float,
        time=None,
        api_version=PirateWeatherApiVersion.BASE,
        **params,
    ):
        host = api_version.value
        valid_lat_long = self.validate_lat_long(latitude=latitude, longitude=longitude)
        if not valid_lat_long:
            raise ValueError("Invalid Latitude or Longitude values.")
        if time is None:
            return f"{host}/{self.api_key}/{latitude},{longitude}"
        return f"{host}/{self.api_key}/{latitude},{longitude},{time}"

    @staticmethod
    def validate_lat_long(latitude: float, longitude: float):
        """Validate latitude and longitude values.

        Parameters:
        latitude (float): Latitude value in degrees.
        longitude (float): Longitude value in degrees.

        Returns:
        bool: True if the latitude and longitude values are valid, False otherwise.

        """
        if -90.0 <= latitude <= 90.0:
            if -180.0 <= longitude <= 180.0:
                return True
        return False


class PirateWeather(BasePirateWeather):
    def __init__(self, api_key: str, gzip: bool = True):
        super().__init__(api_key)
        self.request_manager = RequestManger(gzip)

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        extend: bool = None,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: [Weather] = None,
        timezone: str = None,
    ) -> Forecast:
        url = self.get_url(latitude, longitude)
        exclude = self.convert_exclude_param_to_string(exclude)
        data = self.request_manager.make_request(
            url=url,
            extend=Weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
        )
        return Forecast(**data)

    def get_time_machine_forecast(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        extend: bool = False,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: [Weather] = None,
        timezone: str = None,
    ) -> Forecast:
        url = self.get_url(
            latitude,
            longitude,
            int(time.timestamp()),
            api_version=PirateWeatherApiVersion.TIME_MACHINE,
        )
        exclude = self.convert_exclude_param_to_string(exclude)
        data = self.request_manager.make_request(
            url=url,
            extend=Weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
        )
        return Forecast(**data)

    def get_recent_time_machine_forecast(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        extend: bool = None,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: [Weather] = None,
        timezone: str = None,
    ) -> Forecast:
        required_time = int(time.timestamp())
        current_time = int(datetime.now().timestamp())
        if timezone:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)

        diff = required_time - current_time

        exclude = self.convert_exclude_param_to_string(exclude)

        url = self.get_url(latitude, longitude, diff)
        data = self.request_manager.make_request(
            url=url,
            extend=Weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
        )
        return Forecast(**data)


class PirateWeatherAsync(BasePirateWeather):
    def __init__(self, api_key: str, gzip: bool = True):
        super().__init__(api_key)
        self.request_manager = RequestMangerAsync(gzip=gzip)

    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        client_session: aiohttp.ClientSession,
        extend: bool = None,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: [Weather] = None,
        timezone: str = None,
    ) -> Forecast:
        url = self.get_url(latitude, longitude)
        exclude = self.convert_exclude_param_to_string(exclude)
        data = await self.request_manager.make_request(
            url=url,
            extend=Weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
            session=client_session,
        )
        return Forecast(**data)

    async def get_time_machine_forecast(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        client_session: aiohttp.ClientSession,
        extend: bool = False,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: [Weather] = None,
        timezone: str = None,
    ) -> Forecast:
        url = self.get_url(latitude, longitude, int(time.timestamp()))
        exclude = self.convert_exclude_param_to_string(exclude)
        data = await self.request_manager.make_request(
            url=url,
            extend=Weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
            session=client_session,
        )
        return Forecast(**data)
