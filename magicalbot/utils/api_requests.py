import aiohttp
import logging


logger = logging.getLogger(__name__)

async def get_api_harry_potter(endpoint="characters"):
    try:
        url = f"https://hp-api.onrender.com/api/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except Exception as e:
        logger.error(f"Ошибка API: {e}")
        return None


async def get_api_wizarding_world(endpoint="characters"):
    try:
        url = f"https://wizard-world-api.herokuapp.com/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except Exception as e:
        logger.error(f"Ошибка API: {e}")
        return None
