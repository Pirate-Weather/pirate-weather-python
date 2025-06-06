from . import base


class CurrentlyForecast(base.AutoInit):
    time: int
    summary: str = None
    icon: str
    nearest_storm_distance: int
    nearest_storm_bearing: int
    precip_intensity: float
    precip_intensity_error: float
    precip_probability: float
    precip_type: str
    precipAccumulation: float
    temperature: float
    apparent_temperature: float
    dew_point: float
    humidity: float
    pressure: float
    wind_speed: float
    wind_gust: float
    wind_bearing: int
    cloud_cover: float
    uv_index: int
    visibility: float
    ozone: float


class MinutelyForecastItem(base.AutoInit):
    time: int
    precip_intensity: float
    precip_intensity_error: float
    precip_probability: float
    precip_type: str


class MinutelyForecast(base.BaseWeather):
    data: list[MinutelyForecastItem]
    data_class = MinutelyForecastItem


class HourlyForecastItem(base.AutoInit):
    time: int
    summary: str = None
    icon: str
    precip_intensity: float
    precip_probability: float
    precip_type: str
    precipAccumulation: float
    temperature: float
    apparent_temperature: float
    dew_point: float
    humidity: float
    pressure: float
    wind_speed: float
    wind_gust: float
    wind_bearing: int
    cloud_cover: float
    uv_index: int
    visibility: float
    ozone: float


class HourlyForecast(base.BaseWeather):
    data: list[HourlyForecastItem]
    data_class = HourlyForecastItem


class DailyForecastItem(base.AutoInit):
    time: int
    summary: str = None
    icon: str
    sunrise_time: int
    sunset_time: int
    moon_phase: float
    precip_intensity: float
    precip_intensity_max: float
    precip_intensity_max_time: int
    precip_probability: float
    precip_type: str
    precipAccumulation: float
    temperature_high: float
    temperature_high_time: int
    temperature_low: float
    temperature_low_time: int
    apparent_temperature_high: float
    apparent_temperature_high_time: int
    apparent_temperature_low: float
    apparent_temperature_low_time: int
    dew_point: float
    humidity: float
    pressure: float
    wind_speed: float
    wind_gust: float
    wind_gust_time: int
    wind_bearing: int
    cloud_cover: float
    uv_index: int
    uv_index_time: int
    visibility: int
    ozone: float
    temperature_min: float
    temperature_min_time: int
    temperature_max: float
    temperature_max_time: int
    apparent_temperature_min: float
    apparent_temperature_min_time: int
    apparent_temperature_max: float
    apparent_temperature_max_time: int


class DailyForecast(base.BaseWeather):
    data: list[DailyForecastItem]
    data_class = DailyForecastItem


class Alert(base.AutoInit):
    title: str
    regions: list
    severity: str
    time: int
    expires: int
    description: str
    uri: str


class Flags(base.AutoInit):
    sources: list[str]
    sources_class = str
    nearest__station: float
    pirate_weather__unavailable: bool
    units: str


class Forecast:
    latitude: float
    longitude: float
    timezone: str
    currently: CurrentlyForecast
    minutely: MinutelyForecast
    hourly: HourlyForecast
    daily: DailyForecast
    alerts: list[Alert]
    flags: Flags
    offset: int

    def __init__(
        self,
        latitude: float,
        longitude: float,
        timezone: str,
        currently: dict = None,
        minutely: dict = None,
        hourly: dict = None,
        daily: dict = None,
        alerts: [dict] = None,
        flags: dict = None,
        offset: int = None,
        elevation: int = None,
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone

        self.currently = CurrentlyForecast(timezone=timezone, **(currently or {}))
        self.minutely = MinutelyForecast(timezone=timezone, **(minutely or {}))
        self.hourly = HourlyForecast(timezone=timezone, **(hourly or {}))
        self.daily = DailyForecast(timezone=timezone, **(daily or {}))

        self.alerts = [Alert(timezone=timezone, **alert) for alert in (alerts or [])]
        self.flags = Flags(timezone=timezone, **(flags or {}))

        self.offset = offset

        self.elevation = elevation
