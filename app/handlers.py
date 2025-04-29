from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.database.sqlite_db as sql
import app.keyboards as kb

router = Router()


class AddTasks(StatesGroup):
    title = State()


@router.message(Command('start'))
async def command_start_handler(message: Message):
    await message.answer('Это бот по дисциплине, прочитайте инструкцию', reply_markup=kb.client_reply_keyboards)


@router.message(F.text == 'Создать задания')
async def create_tasks_handler(message: Message, state: FSMContext):
    global tasks_ls 
    tasks_ls = []

    await message.answer('Пишите свои задачи по одному')
    await state.set_state(AddTasks.title)


@router.message(AddTasks.title)
async def create_tasks_state_handler(message: Message, state: FSMContext):
    global tasks_ls
    tasks_ls.append(message.text)

    await message.answer("Напишите ещё одно задание если хотите или нажмите кнопку хватит", reply_markup=kb.stop_added_task_inlinekeyboard)

@router.callback_query(F.data == 'stop_add_task')
async def stop_add_task_handler(callback: CallbackQuery, state: FSMContext):
    global tasks_ls
    await sql.create_new_table_sql(tasks_ls, callback.from_user.id)
    await callback.message.answer(str(tasks_ls))
    await state.clear()


@router.message(F.text == 'Выполнить задания')
async def execute_tasks_handler(message: Message):
    data = await sql.get_today_tasks_sql(message.from_user.id)
    mes = ''
    columns = await sql.get_all_table_sql(message.from_user.id)
    await message.answer(str(columns))
    # for d in range(len(data)):
    #     if d == 0:
    #         mes = mes+f'Сегодняшняя дата:\n{data[0]}\n\n'
    #     else:
    #         if data[d] == 0:
    #             mes = mes + f''