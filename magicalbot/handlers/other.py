import logging

from aiogram import types, F, Router
from aiogram.types import Message

from keyboards.keyboards import *
from utils.utils import *
from utils.decorators import *


logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "magic_sound")
@with_menu_callback
async def magic_sound(message: Message):
    await message.answer("Fast forward to Hogwarts!",
                         reply_markup=inline_kb_sound)


@router.callback_query(F.data == "magic_photo")
@with_menu_callback
async def magic_photo(message: Message):
    await message.answer("Fast forward to Hogwarts!",
                         reply_markup=inline_kb_photo)


@router.callback_query(F.data == "magic_link")
@with_menu_callback
async def magic_link(message: Message):
    await message.answer("All Harry Potter books",
                         reply_markup=inline_kb_link)


@router.callback_query(F.data == "movies_info")
@with_menu_callback
async def magic_movies(message: Message):
    await message.answer("The Harry Potter Movies",
                         reply_markup=inline_kb_movie)
