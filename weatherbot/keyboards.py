from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/help")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
