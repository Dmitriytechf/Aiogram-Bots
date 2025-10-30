import asyncio
from aiogram import types
from keyboards.keyboards import create_main_kb


def with_menu_callback(func):
    """Декоратор для callback_query хэндлеров"""
    async def wrapper(callback: types.CallbackQuery):
        await func(callback.message)
        await asyncio.sleep(2)
        await callback.message.answer(
            "Choose an option:",
            reply_markup=create_main_kb(page=0)
        )
        await callback.answer()
    return wrapper
