import random
import aiohttp
import logging

from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import *
from utils.utils import *
from utils.decorators import *
from .hp_ww import *
from utils.api_requests import get_api_harry_potter


logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"🪄{message.from_user.first_name}, welcome to the world of Harry Potter!",
        parse_mode="HTML",
        reply_markup=create_main_kb(page=0)
    )


@router.callback_query(F.data.startswith("nav_"))
async def handle_navigation(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[1])
    new_kb = create_main_kb(page=page)

    # Обновляем клавиатуру без изменения текста
    await callback.message.edit_reply_markup(reply_markup=new_kb)
    await callback.answer()


@router.callback_query(F.data == "name_wizard")
@with_menu_callback
async def get_random_name(message: Message):
    data = await get_api_harry_potter()
    if data:
        character = random.choice(data)
        await message.answer(f"🪄 Random character: <b>{character.get('name')}</b>",
                             parse_mode="HTML")
    else:
        await message.answer("❌ The owl did not receive data from Hogwarts")


@router.callback_query(F.data == "character_wizard")
@with_menu_callback
async def get_random_character(message: Message):
    data = await get_api_harry_potter()
    if data:
        character = random.choice(data)
        info = f"""
🪄 <b>Random character:</b>

🧙 <b>Name: {character.get('name')}</b>
🏰 Faculty: {get_value(character.get('house')) }
🎂 Birthday: {get_value(character.get('dateOfBirth'))}
🧬 Ancestry: {get_value(character.get('ancestry'))}
🦌 Patronus: {get_value(character.get('patronus'))}
        """
        await message.answer(info, parse_mode="HTML")
    else:
        await message.answer("❌ The owl did not receive data from Hogwarts")


@router.callback_query(F.data.startswith("house_"))
async def handle_house_selection(callback: types.CallbackQuery):
    house = callback.data.split("_")[1]
    house_names = {
        "gryffindor": "Gryffindor",
        "slytherin": "Slytherin",
        "hufflepuff": "Hufflepuff",
        "ravenclaw": "Ravenclaw"
    }
    data = await get_api_harry_potter()
    if data:
        house_characters = [char for char in data if char.get('house') == house_names[house]]
        if house_characters:
            character = random.choice(house_characters)
            await callback.message.answer(
                f"🏰 Random student {house_names[house]}а:\n<b>{character['name']}</b>",
                parse_mode="HTML"
            )
    else:
        await callback.message.answer("❌ The owl did not receive data from Hogwarts")

    await callback.message.answer("Choose an option:", reply_markup=create_main_kb(page=0))
    await callback.answer()


@router.callback_query(F.data == "wizard_menu")
async def characters_menu(callback: types.CallbackQuery):
    await callback.message.answer("Select an option:", reply_markup=inline_kb_characters)
    await callback.answer()


@router.callback_query(F.data == "random_char")
@with_menu_callback
async def handle_random_character(callback: types.CallbackQuery):
    await get_random_character(callback.message)
