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
    # New fields from API v2+
    rain_intensity: float = None
    snow_intensity: float = None
    ice_intensity: float = None
    smoke: float = None
    solar: float = None
    feels_like: float = None
    cape: float = None
    fire_index: float = None
    liquid_accumulation: float = None
    snow_accumulation: float = None
    ice_accumulation: float = None
    station_pressure: float = None
    current_day_ice: float = None
    current_day_liquid: float = None
    current_day_snow: float = None


class MinutelyForecastItem(base.AutoInit):
    time: int
    precip_intensity: float
    precip_intensity_error: float
    precip_probability: float
    precip_type: str
    # New fields from API v2+
    rain_intensity: float = None
    snow_intensity: float = None
    sleet_intensity: float = None


class MinutelyForecast(base.BaseWeather):
    data: list[MinutelyForecastItem]
    data_class = MinutelyForecastItem


class HourlyForecastItem(base.AutoInit):
    time: int
    summary: str = None
    icon: str
    precip_intensity: float
    precip_intensity_error: float = None
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
    # New fields from API v2+
    nearest_storm_distance: int = None
    nearest_storm_bearing: int = None
    smoke: float = None
    solar: float = None
    feels_like: float = None
    cape: float = None
    fire_index: float = None
    liquid_accumulation: float = None
    snow_accumulation: float = None
    ice_accumulation: float = None
    rain_intensity: float = None
    snow_intensity: float = None
    ice_intensity: float = None
    station_pressure: float = None


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
    # New fields from API v2+
    rain_intensity: float = None
    rain_intensity_max: float = None
    rain_intensity_max_time: int = None
    snow_intensity: float = None
    snow_intensity_max: float = None
    snow_intensity_max_time: int = None
    ice_intensity: float = None
    ice_intensity_max: float = None
    ice_intensity_max_time: int = None
    smoke_max: float = None
    smoke_max_time: int = None
    solar_max: float = None
    solar_max_time: int = None
    cape_max: float = None
    cape_max_time: int = None
    fire_index_max: float = None
    fire_index_max_time: int = None
    liquid_accumulation: float = None
    snow_accumulation: float = None
    ice_accumulation: float = None
    current_day_ice: float = None
    current_day_liquid: float = None
    current_day_snow: float = None
    dawn_time: int = None
    dusk_time: int = None


class DailyForecast(base.BaseWeather):
    data: list[DailyForecastItem]
    data_class = DailyForecastItem


# DayNight block is similar to hourly but has some additional fields
class DayNightForecastItem(base.AutoInit):
    time: int
    summary: str = None
    icon: str
    precip_intensity: float
    precip_intensity_max: float = None
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
    # Fields that may be in day_night
    smoke: float = None
    solar: float = None
    feels_like: float = None
    cape: float = None
    fire_index: float = None
    liquid_accumulation: float = None
    snow_accumulation: float = None
    ice_accumulation: float = None
    rain_intensity: float = None
    snow_intensity: float = None
    ice_intensity: float = None
    rain_intensity_max: float = None
    snow_intensity_max: float = None
    ice_intensity_max: float = None
    station_pressure: float = None


class DayNightForecast(base.BaseWeather):
    data: list[DayNightForecastItem]
    data_class = DayNightForecastItem


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
    # New fields from API v2+
    source_times: dict = None
    source_i_d_x: dict = None
    version: str = None
    process_time: float = None
    ingest_version: str = None
    nearest_city: str = None
    nearest_country: str = None
    nearest_sub_national: str = None


class Forecast:
    latitude: float
    longitude: float
    timezone: str
    currently: CurrentlyForecast
    minutely: MinutelyForecast
    hourly: HourlyForecast
    daily: DailyForecast
    day_night: DayNightForecast
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
        day_night: dict = None,
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
        self.day_night = DayNightForecast(timezone=timezone, **(day_night or {}))

        self.alerts = [Alert(timezone=timezone, **alert) for alert in (alerts or [])]
        self.flags = Flags(timezone=timezone, **(flags or {}))

        self.offset = offset

        self.elevation = elevation
