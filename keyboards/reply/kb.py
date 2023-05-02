from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cancel_add_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Отмена')]
    ], resize_keyboard=True)
    return kb
