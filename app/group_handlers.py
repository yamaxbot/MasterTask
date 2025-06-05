from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, F, Router
from aiogram.filters import Command

import app.database.group_sqlite_db as gsql


router_group = Router()


class AddGroup(StatesGroup):
    title = State()


@router_group.message(Command('add_group'))
async def add_group_handler(message: Message, state: FSMContext):
    if str(message.chat.id)[0] == '-':
        await message.answer('Придумайте и отправьте название для своей команды(в группе)')
        await state.set_state(AddGroup.title)
    else:
        await message.answer('Эта команда работает только в группе')



@router_group.message(AddGroup.title)
async def add_group_state_handler(message: Message, state: FSMContext):
    await message.answer('Команда добавлена')
    name = str(message.text).replace(' ', '_')
    await gsql.add_group_gsql(message.chat.id, name)
    await state.clear()
    await message.answer('Ваша группа создана, теперь можете начать играть')



