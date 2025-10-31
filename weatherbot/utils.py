import logging
from datetime import datetime

import aiohttp

from bot import MY_WEATHER_API_KEY


logger = logging.getLogger(__name__)


async def get_current_weather(city: str) -> None:
    try:
        url = f'http://api.weatherapi.com/v1/current.json?key={MY_WEATHER_API_KEY}&q={city}&lang=ru'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"API ошибка: статус {response.status}")
                    return None
    except Exception as e:
        logger.error(f"Ошибка API: {e}")
        return None


async def get_forecast_weather(city: str, days: int = 7) -> None:
    try:
        url = f'http://api.weatherapi.com/v1/forecast.json?key={MY_WEATHER_API_KEY}&q={city}&days={days}&lang=ru'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"API ошибка: статус {response.status}")
                    return None
    except Exception as e:
        logger.error(f"Ошибка API: {e}")
        return None


def format_current_weather(weather_data: dict) -> str:
    """Форматируем данные о текущей погоде"""
    if not weather_data:
        return "Не удалось получить данные о погоде"

    location = weather_data['location']
    current = weather_data['current']

    return (
        f"🌤 *Погода*\n\n"
        f"🌡 *Температура:* `{current['temp_c']}°C`\n"
        f"💭 *Ощущается как:* `{current['feelslike_c']}°C`\n"
        f"📝 *Состояние:* {current['condition']['text']}\n"
        f"💧 *Влажность:* `{current['humidity']}%`\n"
        f"🌬 *Ветер:* `{current['wind_kph']} км/ч`\n"
        f"📊 *Давление:* `{current['pressure_mb']} мбар`\n"
        f"👁 *Видимость:* `{current['vis_km']} км`"
    )


def format_forecast_weather(forecast_data: dict) -> str:
    """Форматируем прогноз погоды на неделю"""
    if not forecast_data:
        return "Не удалось получить прогноз погоды"

    location = forecast_data['location']
    forecast_days = forecast_data['forecast']['forecastday']

    result = [f"*Прогноз погоды на 3 дня:*"]

    for day in forecast_days:
        date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%d.%m')
        day_info = day['day']

        result.append(
            f"\n📅 *{date}:*\n"
            f"   🌡 *Температура:* `{day_info['mintemp_c']}°C...{day_info['maxtemp_c']}°C`\n"
            f"   📝 *Погода:* {day_info['condition']['text']}\n"
            f"   💧 *Влажность:* `{day_info['avghumidity']}%`\n"
            f"   🌬 *Ветер:* `{day_info['maxwind_kph']} км/ч`\n"
        )

    return "\n".join(result)
