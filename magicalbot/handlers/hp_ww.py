import random
import aiohttp
import logging

from aiogram import F, Router
from aiogram.types import Message

from keyboards.keyboards import *
from utils.utils import *
from utils.decorators import *
from utils.api_requests import get_api_wizarding_world


logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "ww_spells")
@with_menu_callback
async def get_wizarding_world_spells(message: Message):
    data = await get_api_wizarding_world("spells")

    if data:
        spell = random.choice(data)
        info=f"""
✨ <b>Wizarding World Spell:</b>

🪄 <b>Spell: {get_value(spell.get('name'))}</b>
📖 Incantation: {get_value(spell.get('incantation'))}
💫 Effect: {get_value(spell.get('effect'))}
🎯 Type: {get_value(spell.get('type'))}
🔮 Light: {get_value(spell.get('light'))}
        """
        await message.answer(info, parse_mode="HTML")
    else:
        await message.answer("❌ The owl did not receive data from Hogwarts")


@router.callback_query(F.data == "ww_elixirs")
@with_menu_callback
async def get_wizarding_world_elixir(message: Message):
    data = await get_api_wizarding_world("elixirs")

    if data:
        elixir = random.choice(data)
        info=f"""
🧪 <b>Magical Elixir:</b>

⚗️ <b>Name: {get_value(elixir.get('name'))}</b>
💫 Effect: {get_value(elixir.get('effect'))}
🎯 Difficulty: {get_value(elixir.get('difficulty'))}
⏱️ Brewing Time: {get_value(elixir.get('time'))}
🧬 Characteristics: {get_value(elixir.get('characteristics'))}
💊 Side Effects: {get_value(elixir.get('sideEffects'))}

        """
        await message.answer(info, parse_mode="HTML")
    else:
        await message.answer("❌ The owl did not receive data from Hogwarts")


@router.callback_query(F.data == "ww_ingredients")
@with_menu_callback
async def get_wizarding_world_ingredients(message: Message):
    data = await get_api_wizarding_world("ingredients")

    if data:
        ingredient = random.choice(data)
        info=f"""
🌿 <b>Magical Ingredient:</b>

🔮 <b>Name: {get_value(ingredient.get('name'))}</b>
        """
        await message.answer(info, parse_mode="HTML")
    else:
        await message.answer("❌ The owl did not receive data from Hogwarts")
