Pirate Weather Python
==========

This library for the [Pirate Weather API](https://pirateweather.net) which is an alternative to the deprecated DarkSky
API, and provides access to detailed
weather information from around the globe.

**Now supporting Pirate Weather API v2.8+** with new data fields including smoke levels, solar radiation, fire indices, and detailed precipitation breakdowns.

* [Installation](#installation)
* [Get started](#get-started)
* [New Features](#new-features)
* [Contact us](#contact-us)
* [License](#license)

## This library was made by updating the [darksky library by Detrous](https://github.com/Detrous/darksky) so all credits go to them.

### Installation

```
pip3 install pirateweather
```

### Get started

Before you start using this library, you need to get your API key
[here](https://pirate-weather.apiable.io/).

#### Notes on functionality

The Pirate Weather timemachine data is limited in availability, it is only possible to fetch data about 1-2 months ago.
For recent historical weather data use the get_recent_time_machine_forecast which will have data from about 1-5 days prior.
Unfortunately, at the time of writing this it is not possible to get data from 2 weeks ago for example.

All classes are fully annotated, source code is your best doc : )

Use of synchronous client:

```python
from pirate_weather.api import PirateWeather
from pirate_weather.types.languages import Languages
from pirate_weather.types.units import Units
from pirate_weather.types.weather import Weather

API_KEY = "0123456789"
pirate_weather = PirateWeather(API_KEY)

latitude = 42.3601
longitude = -71.0589
forecast = pirate_weather.get_forecast(
    latitude, longitude,
    extend=False,  # default `False`
    lang=Languages.ENGLISH,  # default `ENGLISH`
    values_units=Units.AUTO,  # default `auto`
    exclude=[Weather.MINUTELY, Weather.ALERTS],  # default `[]`,
    timezone='UTC'  # default None - will be set by Pirate Weather API automatically
)
```

Use of synchronous timemachine client:

```python
from pirate_weather.api import PirateWeather
from pirate_weather.types.languages import Languages
from pirate_weather.types.units import Units
from pirate_weather.types.weather import Weather
from datetime import datetime as dt

API_KEY = "0123456789"
pirate_weather = PirateWeather(API_KEY)
t = dt(2022, 5, 6, 12)

latitude = 42.3601
longitude = -71.0589
forecast = pirate_weather.get_time_machine_forecast(
    latitude, longitude,
    extend=False,  # default `False`
    lang=Languages.ENGLISH,  # default `ENGLISH`
    values_units=Units.AUTO,  # default `auto`
    exclude=[Weather.MINUTELY, Weather.ALERTS],  # default `[]`,
    timezone='UTC',  # default None - will be set by Pirate Weather API automatically
    time=t
)
```

Use of synchronous client getting recent timemachine data:

```python
from pirate_weather.api import PirateWeather
from pirate_weather.types.languages import Languages
from pirate_weather.types.units import Units
from pirate_weather.types.weather import Weather
from datetime import datetime as dt

API_KEY = "0123456789"
pirate_weather = PirateWeather(API_KEY)
t = dt(2023, 4, 4)

latitude = 42.3601
longitude = -71.0589
forecast = pirate_weather.get_recent_time_machine_forecast(
    latitude, longitude,
    extend=False,  # default `False`
    lang=Languages.ENGLISH,  # default `ENGLISH`
    values_units=Units.AUTO,  # default `auto`
    exclude=[Weather.MINUTELY, Weather.ALERTS],  # default `[]`,
    timezone='UTC',  # default None - will be set by Pirate Weather API automatically
    time=t
)
```

Use of asynchronous client:

```python
from pirate_weather.api import PirateWeatherAsync
from pirate_weather.types.languages import Languages
from pirate_weather.types.units import Units
from pirate_weather.types.weather import Weather

import asyncio
import aiohttp


async def main(api_key):
    async with aiohttp.ClientSession() as session:
        pirate_weather = PirateWeatherAsync(api_key)

        latitude = 42.3601
        longitude = -71.0589
        forecast = await pirate_weather.get_forecast(
            latitude, longitude,
        extend=False,  # default `False`
        lang=Languages.ENGLISH,  # default `ENGLISH`
        values_units=Units.AUTO,  # default `auto`
        exclude=[Weather.MINUTELY, Weather.ALERTS],  # default `[]`,
        timezone='UTC',  # default None - will be set by Pirate Weather API automatically
         client_session=session  # default aiohttp.ClientSession()
        )

api_key = "0123456789"
asyncio.run(main(api_key))
```

### New Features

#### API v2.8+ Support

This library now supports all Pirate Weather API v2.8+ fields:

**New Weather Data Fields:**
- `smoke` - Air quality smoke levels (µg/m³)
- `solar` - Solar radiation (W/m²)
- `feelsLike` - Apparent temperature based on wind and humidity
- `cape` - Convective Available Potential Energy
- `fireIndex` - Fire weather index
- `liquidAccumulation`, `snowAccumulation`, `iceAccumulation` - Precipitation by type
- `rainIntensity`, `snowIntensity`, `iceIntensity` - Intensity by precipitation type
- `currentDayIce`, `currentDayLiquid`, `currentDaySnow` - Accumulations for the current day
- `dawnTime`, `duskTime` - Civil twilight times

**New Metadata Fields:**
- `sourceTimes` - Model update timestamps
- `sourceIDX` - Grid coordinates for each model
- `version` - API version
- `processTime` - Request processing time
- `ingestVersion` - Data ingest version
- `nearestCity`, `nearestCountry`, `nearestSubNational` - Location information

**Day/Night Forecast Block:**

The library now supports the optional `day_night` forecast block which provides 12-hour forecast periods:

```python
forecast = pirate_weather.get_forecast(latitude, longitude)

# Access day/night forecast data
for period in forecast.day_night.data:
    print(f"Time: {period.time}, Temp: {period.temperature}, Smoke: {period.smoke}")
```

**Example accessing new fields:**

```python
forecast = pirate_weather.get_forecast(latitude, longitude)

# Current conditions with new fields
print(f"Current smoke level: {forecast.currently.smoke} µg/m³")
print(f"Solar radiation: {forecast.currently.solar} W/m²")
print(f"Feels like: {forecast.currently.feels_like}°")
print(f"Fire index: {forecast.currently.fire_index}")

# Hourly forecasts with precipitation breakdowns
for hour in forecast.hourly.data:
    if hour.rain_intensity > 0:
        print(f"Rain intensity: {hour.rain_intensity} mm/h")
    if hour.snow_intensity > 0:
        print(f"Snow intensity: {hour.snow_intensity} cm/h")

# Daily forecasts with new max fields
for day in forecast.daily.data:
    print(f"Max smoke: {day.smoke_max} at {day.smoke_max_time}")
    print(f"Max solar: {day.solar_max} at {day.solar_max_time}")
    print(f"Dawn: {day.dawn_time}, Dusk: {day.dusk_time}")

# Metadata
print(f"API Version: {forecast.flags.version}")
print(f"Nearest City: {forecast.flags.nearest_city}")
print(f"Process Time: {forecast.flags.process_time}ms")
```

### License.

Library is released under the [MIT License](./LICENSE).
