from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

client_reply_keyboards = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать задания'), KeyboardButton(text='Выполнить задания')],
    [KeyboardButton(text='Общая статистика'), KeyboardButton(text='Ежедневная статистика')],

], resize_keyboard=True)


stop_added_task_inlinekeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Хватит', callback_data='stop_add_task')]
])