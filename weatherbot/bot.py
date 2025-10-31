import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import asyncio

from keyboards import start_kb
from utils import *


load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
)
logger = logging.getLogger(__name__)

TOKEN_KEY = os.getenv('WEATHER_API_KEY')
MY_WEATHER_API_KEY = os.getenv('SITE_WEATHER_API_KEY')

bot = Bot(TOKEN_KEY)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_bot(message: Message):
    await message.answer(
        f"Привет, @{message.from_user.username}! Перейди в раздел help и узнай погоду!\n",
        reply_markup=start_kb
    )


@dp.message(Command("help"))
async def help_weather(message: Message):
    info = (
        "📖 Доступные команды:\n\n"
        "🌤 /weather [город] - погода на сегодня\n"
        "Пример: /weather Москва\n\n"
        "📅 /forecast [город] - прогноз на неделю\n"
        "Пример: /forecast Санкт-Петербург\n\n"
        "📍 Можно использовать на английском:\n"
        "`/weather London` | `/forecast New York`"
    )
    await message.answer_sticker(
        sticker='CAACAgIAAxkBAAEPq8FpBEn8j_Bhmj6zrkVgReLP87M1wAAC4BwAAnbQcUvyswPrqKIEgzYE'
    )
    await message.answer(
        info,
        parse_mode="Markdown"
    )


@dp.message(Command("weather"))
async def weather_command(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("❌ Укажите город: `/weather Москва`",
                             parse_mode="Markdown")
        return

    city = args[1].strip()
    await message.answer(f"🔍 Ищу погоду в *{city}*...",
                         parse_mode="Markdown")
    await asyncio.sleep(1)

    weather_data = await get_current_weather(city)
    if weather_data:
        formatted_weather = format_current_weather(weather_data)
        await message.answer(formatted_weather, parse_mode="Markdown")
    else:
        await message.answer(f"❌ Не удалось найти погоду для '{city}'")


@dp.message(Command("forecast"))
async def forecast_command(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("❌ Укажите город: `/forecast Москва`",
                             parse_mode="Markdown")
        return

    city = args[1].strip()
    await message.answer(f"🔍 Ищу прогноз для *{city}*...",
                         parse_mode="Markdown")
    await asyncio.sleep(1)

    forecast_data = await get_forecast_weather(city)
    if forecast_data:
        formatted_forecast = format_forecast_weather(forecast_data)
        await message.answer(formatted_forecast, parse_mode="Markdown")
    else:
        await message.answer(f"❌ Не удалось найти прогноз для '{city}'")


@dp.message(F.text)
async def handle_text(message: Message):
    text = message.text.strip()

    # Игнорируем кнопки и команды без слеша
    if text.lower() not in ['help', 'помощь']:
        await message.answer(
            "🤔 *Используй команды:*\n\n"
            "🌤 `/weather [город]` - погода на сегодня\n"
            "📅 `/forecast [город]` - прогноз на неделю\n"
            "❓ `/help` - помощь\n\n"
            "*Примеры:*\n"
            "`/weather Феодосия`\n"
            "`/forecast Феодосия`\n"
            "`/weather London`",
            parse_mode="Markdown"
        )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logger.info('---Бот запущен---')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('---Бот остановлен по команде пользователя---')
    except ValueError:
        logger.critical('Exit')
