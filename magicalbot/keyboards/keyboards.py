from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


all_buttons = [
    {"text": "🧙 Name Wizard", "callback_data": "name_wizard"},
    {"text": "🔮 Character Wizard", "callback_data": "character_wizard"},
    {"text": "📜 Wizard Characters Menu", "callback_data": "wizard_menu"},
    {"text": "🪄 Wizarding World Spells", "callback_data": "ww_spells"},
    {"text": "🧪 Wizarding World Elixirs", "callback_data": "ww_elixirs"},
    {"text": "🌿 Wizarding World Ingredients", "callback_data": "ww_ingredients"},
    {"text": "📸 Magic Photo", "callback_data": "magic_photo"},
    {"text": "🎵 Magic Sound", "callback_data": "magic_sound"},
    {"text": "📚 All Books", "callback_data": "magic_link"},
    {"text": "🎬 Movies Info", "callback_data": "movies_info"}
]


def create_main_kb(page: int = 0, buttons_per_page: int = 4):
    builder = InlineKeyboardBuilder()

    start_idx = page * buttons_per_page
    end_idx = start_idx + buttons_per_page
    page_buttons = all_buttons[start_idx:end_idx]

     # Добавляем кнопки текущей страницы
    for button in page_buttons:
        builder.add(InlineKeyboardButton(
            text=button["text"],
            callback_data=button["callback_data"]
        ))

    # Навигация
    if len(all_buttons) > buttons_per_page:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton(
                text="⬅️ Back",
                callback_data=f"nav_{page-1}"
            ))
        if end_idx < len(all_buttons):
            nav_buttons.append(InlineKeyboardButton(
                text="Next ➡️",
                callback_data=f"nav_{page+1}"
            ))
        
        if nav_buttons:
            builder.row(*nav_buttons)

    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)


inline_kb_sound = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Link", url="https://www.youtube.com/watch?v=rPt79QYxXEc&list=RDrPt79QYxXEc&start_radio=1")
        ]
    ]
)

inline_kb_photo = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Photo", url="https://www.pinterest.com/ideas/hogwarts-photos/942338441439/")
        ]
    ]
)

inline_kb_link= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Book link", url="https://disk.yandex.ru/d/FrY5OUO6av68ow")
        ]
    ]
)

inline_kb_movie= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Movies", url="https://vk.com/video-136020824_456247545")
        ]
    ]
)

inline_kb_characters = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🏰 Гриффиндор",
                                 callback_data="house_gryffindor"),
            InlineKeyboardButton(text="🐍 Слизерин",
                                 callback_data="house_slytherin")
        ],
        [
            InlineKeyboardButton(text="🦡 Пуффендуй",
                                 callback_data="house_hufflepuff"),
            InlineKeyboardButton(text="🦅 Когтевран",
                                 callback_data="house_ravenclaw")
        ]
    ]
)
