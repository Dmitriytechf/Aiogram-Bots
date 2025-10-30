import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import asyncio

from handlers import hp_api, hp_ww, other


load_dotenv()
TOKEN_KEY = os.getenv('MAGIC_BOT')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(TOKEN_KEY)
    dp = Dispatcher()

    dp.include_routers(
        hp_api.router,
        hp_ww.router,
        other.router
    )

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
