Pirate Weather Python
==========

This library for the [Pirate Weather API](https://pirateweather.net) which is an alternative to the deprecated DarkSky
API, and provides access to detailed
weather information from around the globe.

* [Installation](#installation)
* [Get started](#get-started)
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

### License.

Library is released under the [MIT License](./LICENSE).
