from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

client_inline_keyboards = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить', callback_data='buy'), InlineKeyboardButton(text='Продать', callback_data='sell')],
    [InlineKeyboardButton(text='Помощь', callback_data='help'), InlineKeyboardButton(text='О проекте', callback_data='project')]

])
