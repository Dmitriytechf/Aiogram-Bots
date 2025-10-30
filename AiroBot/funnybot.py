import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from asyncio import sleep
import asyncio

from stick import *


load_dotenv()

TOKEN_KEY = os.getenv('FUNGAME_BOT_TOKEN')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(TOKEN_KEY)
dp = Dispatcher()


start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Меню", callback_data="menu")],
    ]
)

keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎲 Бросить кубик"), KeyboardButton(text="🏀 Бросить в кольцо")],
              [KeyboardButton(text="⚽ Пнуть мяч"),  KeyboardButton(text="🎯 Кинуть дротик")]],
    resize_keyboard=True,
    one_time_keyboard=True # Скрываем после нажатия
)

dice_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎲 Бросить кубик")]],
    resize_keyboard=True
)

basket_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🏀 Бросить в кольцо")]],
    resize_keyboard=True
)

football_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⚽ Пнуть мяч")]],
    resize_keyboard=True
)

darts_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎯 Кинуть дротик")]],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer(
        f"Привет, @{message.from_user.username}! Давай вместе сыграем.\n"
        "Перейди в меню и выбери игру!",
        reply_markup=start_keyboard
    )


@dp.callback_query(F.data == "menu")
async def menu_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "Выбери кнопку ниже, чтобы начать игру.",
        reply_markup=keyboard
    )


@dp.message(Command("menu"))
async def menu_command(message: types.Message):
    await message.answer(
        f"Выберите игру в меню!\n"
        "Нажми кнопку ниже, чтобы начать игру.",
        reply_markup=keyboard
    )


@dp.message(F.text == "🎲 Бросить кубик")
async def play_game_cube(message: types.Message):
    await message.answer('Значит, бросаем кости. Ну что ж, поехали')
    await sleep(1)
    
    await message.answer('🎲 Ииии, мой бросок')
    bot_dice = await message.answer_dice()
    bot_value = bot_dice.dice.value
    await sleep(4)
    
    await message.answer('🎲 Теперь бросаете Вы')
    await sleep(1)
    user_dice = await message.answer_dice()
    user_value = user_dice.dice.value
    await sleep(4)
    
    if user_value > bot_value:
        result = f'🏆 Поздравляю, Вы победили! {user_value} > {bot_value}'
        await message.answer_sticker(sticker=happy_stick)
    elif user_value < bot_value:
        result = f'😓 Ой-ой, выиграл бот! {user_value} < {bot_value}'
        await message.answer_sticker(sticker=cry_stick)
    else:
        result =  f'🎲 {user_value} = {bot_value}. Ничья 🥶'
        
    result += '\n\n Хотите поиграть в другую игру? /menu'
        
    await message.answer(result, reply_markup=dice_keyboard)


@dp.message(F.text == "🏀 Бросить в кольцо")
async def play_game_basketball(message: types.Message):
    await message.answer('Давайте сыграем в баскетбол. Ну что ж, поехали')
    await sleep(1)
    
    await message.answer("🏀 Бот бросает...")
    bot_throw = await message.answer_dice(emoji="🏀")
    bot_score = bot_throw.dice.value
    await sleep(4)
    
    await message.answer("🏀 Ваш бросок...")
    await sleep(1)
    player_throw = await message.answer_dice(emoji="🏀")
    player_score = player_throw.dice.value
    await sleep(4)
    
    if player_score > bot_score:
        result = f"🏆 Вы победили! Бросок как у Майкла Джордана! {player_score} > {bot_score}"
        await message.answer_sticker(sticker=happy_stick)
    elif player_score < bot_score:
        result = f"😓 Ну, ничего. Всегда есть куда расти. {player_score} < {bot_score}"
        await message.answer_sticker(sticker=cry_stick)
    else:
        result = f"🤝 {player_score} = {bot_score} Ничья!"
        
    if player_score == 5:
        result += "\n🔥 Идеальный бросок!"
    elif player_score >= 3:
        result += "\n✅ Ох, неплохо!"
    else:
        result += "\n❌ Ничего, время потренироваться"
    
    result += '\n\n Хотите поиграть в другую игру? /menu'    

    await message.answer(result, reply_markup=basket_keyboard)


@dp.message(F.text == "⚽ Пнуть мяч")
async def play_game_football(message: types.Message):
    await message.answer('Давайте сыграем в футбол. Ну что ж, поехали')
    await sleep(1)
    
    await message.answer("⚽ Бот бьет...")
    bot_throw = await message.answer_dice(emoji="⚽")
    bot_score = bot_throw.dice.value
    await sleep(4)
    
    await message.answer("⚽ Вы бьете")
    await sleep(1)
    player_throw = await message.answer_dice(emoji="⚽")
    player_score = player_throw.dice.value
    await sleep(4)
    
    if player_score > bot_score:
        result = f"🏆 Вы победили! Кажется, это была девятка? {player_score} > {bot_score}"
        await message.answer_sticker(sticker=happy_stick)
    elif player_score < bot_score:
        result = f"😓 Ну, ничего. Всегда есть куда расти. {player_score} < {bot_score}"
        await message.answer_sticker(sticker=cry_stick)
    else:
        result = f"🤝 {player_score} = {bot_score} Ничья!"
        
    result += '\n\n Хотите поиграть в другую игру? /menu'
        
    await message.answer(result, reply_markup=football_keyboard)


@dp.message(F.text == "🎯 Кинуть дротик")
async def play_game_darts(message: types.Message):
    await message.answer('Давайте сыграем в дартс. Ну что ж, поехали')
    await sleep(1)
    
    await message.answer("🎯 Бот кидает...")
    bot_throw = await message.answer_dice(emoji="🎯")
    bot_score = bot_throw.dice.value
    await sleep(4)
    
    await message.answer("🎯 Ваш бросок")
    await sleep(1)
    player_throw = await message.answer_dice(emoji="🎯")
    player_score = player_throw.dice.value
    await sleep(4)
    
    if player_score > bot_score:
        result = f"🏆 Вы победили! Точно в цель. {player_score} > {bot_score}"
        await message.answer_sticker(sticker=happy_stick)
    elif player_score < bot_score:
        result = f"😓 Ну, ничего. Покидаем еще. {player_score} < {bot_score}"
        await message.answer_sticker(sticker=cry_stick)
    else:
        result = f"🤝 {player_score} = {bot_score} Ох, ничья!"
        
    result += '\n\n Хотите поиграть в другую игру? /menu'
        
    await message.answer(result, reply_markup=darts_keyboard)


async def main():
    # Очищаем вебхук и все ожидающие обновления
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем бота в режиме long-polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logger.info('---Бот запущен---')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.critical('Exit')
