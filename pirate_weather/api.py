"""Synchronous and asynchronous clients for the Pirate Weather API."""

from datetime import datetime
from enum import Enum, StrEnum

import aiohttp
import pytz

from .forecast import Forecast
from .request_manager import BaseRequestManger, RequestManger, RequestMangerAsync
from .types.aqi_units import AQIUnits
from .types.extra_vars import ExtraVars
from .types.icons import Icons
from .types.include import Include
from .types.languages import Languages
from .types.units import Units
from .types.weather import Weather


class PirateWeatherApiVersion(StrEnum):
    """Base URLs of the Pirate Weather API endpoints."""

    BASE = "https://api.pirateweather.net/forecast"
    TIME_MACHINE = "https://timemachine.pirateweather.net/forecast"


class BasePirateWeather:
    """Shared logic for the synchronous and asynchronous clients."""

    def __init__(self, api_key: str):
        """Store the API key used to authenticate requests."""
        self.api_key: str = api_key
        self.request_manager: BaseRequestManger = None

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        extend: bool | None = None,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: list[Weather] | None = None,
        timezone: str | None = None,
        *,
        version: int | None = None,
        include: list[Include] | None = None,
        extra_vars: list[ExtraVars] | None = None,
        icon: Icons | None = None,
        aqi_units: AQIUnits | None = None,
    ):
        """Get the current forecast for a location."""
        raise NotImplementedError

    def get_time_machine_forecast(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        extend: bool = False,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: list[Weather] | None = None,
        timezone: str | None = None,
        *,
        version: int | None = None,
        include: list[Include] | None = None,
        extra_vars: list[ExtraVars] | None = None,
        icon: Icons | None = None,
        aqi_units: AQIUnits | None = None,
    ):
        """Get historic weather data for a location from the time machine."""
        raise NotImplementedError

    @staticmethod
    def _enum_value(value):
        return value.value if isinstance(value, Enum) else value

    @classmethod
    def convert_list_param_to_string(cls, values: list | None) -> str | None:
        """Join a list of enums or strings into a comma separated string."""
        if values:
            values = ",".join(str(cls._enum_value(v)) for v in values)
        return values or None

    @classmethod
    def convert_exclude_param_to_string(
        cls, exclude: list[Weather] | None
    ) -> str | None:
        """Join the ``exclude`` list into a comma separated string."""
        return cls.convert_list_param_to_string(exclude)

    @classmethod
    def build_params(
        cls,
        *,
        extend: bool | None = None,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: list[Weather] | None = None,
        timezone: str | None = None,
        version: int | None = None,
        include: list[Include] | None = None,
        extra_vars: list[ExtraVars] | None = None,
        icon: Icons | None = None,
        aqi_units: AQIUnits | None = None,
    ) -> dict:
        """Build the query parameters for a request.

        Args:
            extend: Extend the hourly block from 48 to 168 hours.
            lang: Language of the text summaries.
            values_units: Unit system of the returned values.
            exclude: Data blocks (``Weather``) or model sources (``Sources``) to exclude.
            timezone: Time zone used to convert timestamps, defaults to the location's.
            version: API version, ``2`` or higher adds fields not in the Dark Sky spec.
            include: Optional data blocks to add to the response.
            extra_vars: Hidden variables to add to the response.
            icon: Icon set to use, ``Icons.PIRATE`` for the expanded set.
            aqi_units: Scale used for the air quality index.

        Returns:
            The query parameters with unset values removed.

        """
        params = {
            "extend": Weather.HOURLY.value if extend else None,
            "lang": cls._enum_value(lang),
            "units": cls._enum_value(values_units),
            "exclude": cls.convert_list_param_to_string(exclude),
            "timezone": timezone,
            "version": version,
            "include": cls.convert_list_param_to_string(include),
            "extraVars": cls.convert_list_param_to_string(extra_vars),
            "icon": cls._enum_value(icon),
            "aqiunits": cls._enum_value(aqi_units),
        }
        return {key: value for key, value in params.items() if value is not None}

    def get_url(
        self,
        latitude: float,
        longitude: float,
        time=None,
        api_version=PirateWeatherApiVersion.BASE,
        **params,
    ) -> str:
        """Build the request URL for a location and optional time."""
        host = api_version.value
        valid_lat_long = self.validate_lat_long(latitude=latitude, longitude=longitude)
        if not valid_lat_long:
            raise ValueError("Invalid Latitude or Longitude values.")
        if time is None:
            return f"{host}/{self.api_key}/{latitude},{longitude}"
        return f"{host}/{self.api_key}/{latitude},{longitude},{time}"

    def get_time_machine_url(
        self, latitude: float, longitude: float, time: datetime
    ) -> str:
        """Build the time machine URL for a location at a given time."""
        return self.get_url(
            latitude,
            longitude,
            int(time.timestamp()),
            api_version=PirateWeatherApiVersion.TIME_MACHINE,
        )

    def get_recent_time_machine_url(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        timezone: str | None = None,
    ) -> str:
        """Build the forecast URL for a time relative to now."""
        current_time = int(datetime.now().timestamp())
        if timezone:
            current_time = int(datetime.now(pytz.timezone(timezone)).timestamp())
        return self.get_url(latitude, longitude, int(time.timestamp()) - current_time)

    @staticmethod
    def validate_lat_long(latitude: float, longitude: float) -> bool:
        """Validate latitude and longitude values.

        Args:
            latitude: Latitude value in degrees.
            longitude: Longitude value in degrees.

        Returns:
            True if the latitude and longitude values are valid, False otherwise.

        """
        if -90.0 <= latitude <= 90.0:
            if -180.0 <= longitude <= 180.0:
                return True
        return False


class PirateWeather(BasePirateWeather):
    """Synchronous Pirate Weather client.

    The optional arguments of every method are documented in
    ``BasePirateWeather.build_params``.
    """

    def __init__(self, api_key: str, gzip: bool = True):
        """Create a client, requesting gzip compressed responses by default."""
        super().__init__(api_key)
        self.request_manager = RequestManger(gzip)

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        extend: bool | None = None,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: list[Weather] | None = None,
        timezone: str | None = None,
        *,
        version: int | None = None,
        include: list[Include] | None = None,
        extra_vars: list[ExtraVars] | None = None,
        icon: Icons | None = None,
        aqi_units: AQIUnits | None = None,
    ) -> Forecast:
        """Get the current forecast for a location."""
        data = self.request_manager.make_request(
            url=self.get_url(latitude, longitude),
            **self.build_params(
                extend=extend,
                lang=lang,
                values_units=values_units,
                exclude=exclude,
                timezone=timezone,
                version=version,
                include=include,
                extra_vars=extra_vars,
                icon=icon,
                aqi_units=aqi_units,
            ),
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
        exclude: list[Weather] | None = None,
        timezone: str | None = None,
        *,
        version: int | None = None,
        include: list[Include] | None = None,
        extra_vars: list[ExtraVars] | None = None,
        icon: Icons | None = None,
        aqi_units: AQIUnits | None = None,
    ) -> Forecast:
        """Get historic weather data for a location from the time machine."""
        data = self.request_manager.make_request(
            url=self.get_time_machine_url(latitude, longitude, time),
            **self.build_params(
                extend=extend,
                lang=lang,
                values_units=values_units,
                exclude=exclude,
                timezone=timezone,
                version=version,
                include=include,
                extra_vars=extra_vars,
                icon=icon,
                aqi_units=aqi_units,
            ),
        )
        return Forecast(**data)

    def get_recent_time_machine_forecast(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        extend: bool | None = None,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: list[Weather] | None = None,
        timezone: str | None = None,
        *,
        version: int | None = None,
        include: list[Include] | None = None,
        extra_vars: list[ExtraVars] | None = None,
        icon: Icons | None = None,
        aqi_units: AQIUnits | None = None,
    ) -> Forecast:
        """Get recent historic weather data (the last few days) for a location."""
        data = self.request_manager.make_request(
            url=self.get_recent_time_machine_url(latitude, longitude, time, timezone),
            **self.build_params(
                extend=extend,
                lang=lang,
                values_units=values_units,
                exclude=exclude,
                timezone=timezone,
                version=version,
                include=include,
                extra_vars=extra_vars,
                icon=icon,
                aqi_units=aqi_units,
            ),
        )
        return Forecast(**data)


class PirateWeatherAsync(BasePirateWeather):
    """Asynchronous Pirate Weather client.

    The optional arguments of every method are documented in
    ``BasePirateWeather.build_params``.
    """

    def __init__(self, api_key: str, gzip: bool = True):
        """Create a client, requesting gzip compressed responses by default."""
        super().__init__(api_key)
        self.request_manager = RequestMangerAsync(gzip=gzip)

    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        client_session: aiohttp.ClientSession,
        extend: bool | None = None,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: list[Weather] | None = None,
        timezone: str | None = None,
        *,
        version: int | None = None,
        include: list[Include] | None = None,
        extra_vars: list[ExtraVars] | None = None,
        icon: Icons | None = None,
        aqi_units: AQIUnits | None = None,
    ) -> Forecast:
        """Get the current forecast for a location."""
        data = await self.request_manager.make_request(
            url=self.get_url(latitude, longitude),
            **self.build_params(
                extend=extend,
                lang=lang,
                values_units=values_units,
                exclude=exclude,
                timezone=timezone,
                version=version,
                include=include,
                extra_vars=extra_vars,
                icon=icon,
                aqi_units=aqi_units,
            ),
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
        exclude: list[Weather] | None = None,
        timezone: str | None = None,
        *,
        version: int | None = None,
        include: list[Include] | None = None,
        extra_vars: list[ExtraVars] | None = None,
        icon: Icons | None = None,
        aqi_units: AQIUnits | None = None,
    ) -> Forecast:
        """Get historic weather data for a location from the time machine."""
        data = await self.request_manager.make_request(
            url=self.get_time_machine_url(latitude, longitude, time),
            **self.build_params(
                extend=extend,
                lang=lang,
                values_units=values_units,
                exclude=exclude,
                timezone=timezone,
                version=version,
                include=include,
                extra_vars=extra_vars,
                icon=icon,
                aqi_units=aqi_units,
            ),
            session=client_session,
        )
        return Forecast(**data)

    async def get_recent_time_machine_forecast(
        self,
        latitude: float,
        longitude: float,
        time: datetime,
        client_session: aiohttp.ClientSession,
        extend: bool | None = None,
        lang=Languages.ENGLISH,
        values_units=Units.AUTO,
        exclude: list[Weather] | None = None,
        timezone: str | None = None,
        *,
        version: int | None = None,
        include: list[Include] | None = None,
        extra_vars: list[ExtraVars] | None = None,
        icon: Icons | None = None,
        aqi_units: AQIUnits | None = None,
    ) -> Forecast:
        """Get recent historic weather data (the last few days) for a location."""
        data = await self.request_manager.make_request(
            url=self.get_recent_time_machine_url(latitude, longitude, time, timezone),
            **self.build_params(
                extend=extend,
                lang=lang,
                values_units=values_units,
                exclude=exclude,
                timezone=timezone,
                version=version,
                include=include,
                extra_vars=extra_vars,
                icon=icon,
                aqi_units=aqi_units,
            ),
            session=client_session,
        )
        return Forecast(**data)
