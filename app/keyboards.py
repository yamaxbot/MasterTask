from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


client_reply_keyboards = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📖Создать задания'), KeyboardButton(text='📊Статистика')],
    [KeyboardButton(text='✏️Выполнить задания'), KeyboardButton(text='📈Ежедневная статистика')],
    [KeyboardButton(text='📝Редактировать задания'), KeyboardButton(text='🙋‍♂️Статистика друга')],

], resize_keyboard=True)


stop_added_task_inlinekeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Хватит', callback_data='stop_add_task')]
])


async def inline_number_task_kb(quant):
    keyboard = InlineKeyboardBuilder()
    for i in range(1, quant+1):
        keyboard.add(InlineKeyboardButton(text=str(i), callback_data=f'number_{str(i)}'))
    return keyboard.adjust(3).as_markup()


inline_arroy_daily_tasks_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅', callback_data='arrow_left'), InlineKeyboardButton(text='➡', callback_data='arrow_right')]
])


edit_tasks_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить задание', callback_data='add_task'), InlineKeyboardButton(text='Удалить задание', callback_data='delete_task')]
])


async def delete_one_task_inline(quant):
    keyboard = InlineKeyboardBuilder()
    for i in range(1, quant+1):
        keyboard.add(InlineKeyboardButton(text=str(i), callback_data=f'deletetask_{str(i)}'))
    return keyboard.adjust(3).as_markup()


inline_cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
])


inline_friend_statistics_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мой код', callback_data='my_code'), InlineKeyboardButton(text='Статистика друга', callback_data='friend_code')]
])


inline_create_delete_code_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать код', callback_data='create_code'), InlineKeyboardButton(text='Удалить код', callback_data='delete_code')]
])


inline_friend_statistics_all_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Статистика', callback_data='general_statistics')]
])