from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.database.sqlite_db as sql          # Импорт всех функций и переменных с файла sqlite_db
import app.keyboards as kb

router = Router()

@router.message(Command('start'))
async def command_start(message: Message):
    await sql.sql_add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)  # Добавление пользователя
    await message.answer('Привет!')


@router.message(Command('get_my_data'))
async def get_my_data(message: Message):
    data = await sql.sql_get_user(message.from_user.id)
    await message.answer(f'Id: {data[0]}\nName: {data[1]}\nUsername: {data[2]}')


@router.message(Command('zero'))
async def update_user_handler(message: Message):
    await sql.sql_update_user(message.from_user.id)
    await message.answer('Готово')


@router.message(Command('delete_me'))
async def delete_user_handler(message: Message):
    await sql.sql_delete_user(message.from_user.id)
    await message.answer('Готово! Чтобы обратно зарегестрироваться, введите команду /start')