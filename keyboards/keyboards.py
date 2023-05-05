from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon_ru import LEXICON_BUTTON

button_yes = KeyboardButton(text=LEXICON_BUTTON['yes'])
button_no = KeyboardButton(text=LEXICON_BUTTON['no'])
keyboard_yes_no = ReplyKeyboardMarkup(keyboard=[[button_no, button_yes]],
                                      resize_keyboard=True,
                                      one_time_keyboard=True)
