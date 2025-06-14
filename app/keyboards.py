from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


client_reply_keyboards = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🔔Напоминание'), KeyboardButton(text='👤Профиль')],
    [KeyboardButton(text='✏️Дневной план'), KeyboardButton(text='📊Статистика')],
    [KeyboardButton(text='📝Изменить дневной план'), KeyboardButton(text='🙋‍♂️Статистика друга')],

], resize_keyboard=True)


stop_added_task_inlinekeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Хватит', callback_data='stop_add_task')]
])


user_statistics_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Статистика', callback_data='general_statistics'), InlineKeyboardButton(text='Ежедневник', callback_data='default_statistics')]
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
    [InlineKeyboardButton(text='Добавить задания', callback_data='add_task'), InlineKeyboardButton(text='Удалить задания', callback_data='delete_task')]
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
    [InlineKeyboardButton(text='Статистика', callback_data='general_statistics_friend')],
    [InlineKeyboardButton(text='Ежедневник', callback_data='default_statistics_friend')]
])


inline_arroy_daily_tasks_friend_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅', callback_data='arrow_left_friend'), InlineKeyboardButton(text='➡', callback_data='arrow_right_friend')]
])


inline_add_delete_reminder_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Редактировать время', callback_data='edit_time')]
])


inline_stop_add_time_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Хватит', callback_data='add_time_stop')]
])


inline_all_times_reminder_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='00:00', callback_data='remtime_0000'), InlineKeyboardButton(text='01:00', callback_data='remtime_0100'), InlineKeyboardButton(text='02:00', callback_data='remtime_0200'), InlineKeyboardButton(text='03:00', callback_data='remtime_0300')],
    [InlineKeyboardButton(text='04:00', callback_data='remtime_0400'), InlineKeyboardButton(text='05:00', callback_data='remtime_0500'), InlineKeyboardButton(text='06:00', callback_data='remtime_0600'), InlineKeyboardButton(text='07:00', callback_data='remtime_0700')],
    [InlineKeyboardButton(text='08:00', callback_data='remtime_0800'), InlineKeyboardButton(text='09:00', callback_data='remtime_0900'), InlineKeyboardButton(text='10:00', callback_data='remtime_1000'), InlineKeyboardButton(text='11:00', callback_data='remtime_1100')],
    [InlineKeyboardButton(text='12:00', callback_data='remtime_1200'), InlineKeyboardButton(text='13:00', callback_data='remtime_1300'), InlineKeyboardButton(text='14:00', callback_data='remtime_1400'), InlineKeyboardButton(text='15:00', callback_data='remtime_1500')],
    [InlineKeyboardButton(text='16:00', callback_data='remtime_1600'), InlineKeyboardButton(text='17:00', callback_data='remtime_1700'), InlineKeyboardButton(text='18:00', callback_data='remtime_1800'), InlineKeyboardButton(text='19:00', callback_data='remtime_1900')],
    [InlineKeyboardButton(text='20:00', callback_data='remtime_2000'), InlineKeyboardButton(text='21:00', callback_data='remtime_2100'), InlineKeyboardButton(text='22:00', callback_data='remtime_2200'), InlineKeyboardButton(text='23:00', callback_data='remtime_2300')],
    [InlineKeyboardButton(text='Сохранить', callback_data='save_time')]
])


async def donate_reminder_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить 100 ⭐️", pay=True)
    
    return builder.as_markup()


async def battle_inline_kb(id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Сразиться!', callback_data=f'battle_kb_{str(id)}'))
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data=f'battle_cancel_{str(id)}'))
    return keyboard.adjust(1).as_markup()

