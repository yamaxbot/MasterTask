from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, F, Router
from aiogram.filters import Command

import app.database.group_sqlite_db as gsql
import app.database.sqlite_db as sql

router_group = Router()


@router_group.message(F.text.startswith('/add_group'))
async def add_group_handler(message: Message, state: FSMContext):
    all_groups = await gsql.get_all_groups_id_gsql()

    if str(message.chat.id)[0] == '-' and str(message.text).count('+') == 1 and str(message.chat.id) not in all_groups:
        name = list(str(message.text).split('+'))[1]
        await gsql.add_group_gsql(message.chat.id, name)
        await message.answer('Группа добавлена')
    else:
        if str(message.chat.id)[0] != '-':
            await message.answer('Эта команда работает только в группе')
        elif str(message.chat.id) in all_groups:
            await message.answer('Ваша группа уже зарегестрирована, вы можете только изменить её имя')
        elif str(message.text).count('+') != 1:
            await message.answer('Вы ввели команду некорректно')



@router_group.message(Command('upgrade'))
async def command_upgrade_handler(message: Message):
    if str(message.chat.id)[0] == '-':
        columns = await gsql.get_group_columns_gsql(message.chat.id)
        if f'id_{message.from_user.id}' not in columns:
            await gsql.add_new_user_group_gsql(message.chat.id, message.from_user.id)
            await gsql.add_points_main_groups_gsql(message.chat.id)
            await sql.add_points_clients_sql(message.from_user.id)
            await message.answer('Вам зачислен бал за дисциплину')
        else:
            activ = await gsql.get_activity_user_today_gsql(message.chat.id, message.from_user.id)

            if activ[0] == '0':
                await gsql.add_points_gsql(message.chat.id, message.from_user.id)
                await message.answer('Вам зачислен бал')
            else:
                await message.answer('Вы уже пользовались данной функцией')
    else:
        await message.answer('Эта команда работает только в группе')



@router_group.message(Command('top_chats'))
async def top_global_chats_handler(message: Message):
    if str(message.chat.id)[0] == '-':
        all_chats = await gsql.all_groups_gsql()
        all_chats = sorted(all_chats, key=lambda x: x[2], reverse=True)
        flag = False
        mes = 'Топ 10 групп по количеству баллов:\n\n'
        for i in range(0, 10):
            if len(all_chats) < i+1:
                break

            if all_chats[i][0] == str(message.chat.id):
                mes += f'{i+1} {all_chats[i][1]}(Ваша группа) - {all_chats[i][2]} б.\n'
                flag = True
            else:
                mes += f'{i+1} {all_chats[i][1]} - {all_chats[i][2]} б.\n'

            if flag == False:
                for i in range(0, all_chats):
                    if all_chats[i][0] == str(message.chat.id):
                        mes += f'{i+1} {all_chats[i][1]}(Ваша группа) - {all_chats[i][2]} б.'
                        break
        await message.answer(mes)
    else:
        await message.answer('Эта команда работает только в группе')



@router_group.message(Command('top_users'))
async def top_users_handler(message: Message):
    if str(message.chat.id)[0] == '-':
        all_columns = await gsql.get_group_columns_gsql(message.chat.id)
        all_users_points = await gsql.get_all_group_gsql(message.chat.id)
        users_points = {}

        for i in range(len(all_users_points[0])):
            ls = []
            if i == 0:
                continue
            for j in range(len(all_users_points)):
                ls.append(int(all_users_points[j][i]))
            users_points[str(all_columns[i])[3:]] = sum(ls)
        users_points = sorted(users_points.items(), key=lambda x: x[1], reverse=True)

        mes = 'Топ участников этой группы\n\n'
        i = 1
        for key_val in users_points:
            client = await sql.get_client_sql(key_val[0])
            mes += f'{i} {client[4]} - {key_val[1]}б.\n'
            i += 1

        await message.answer(mes)
    else:
        await message.answer('Эта команда работает только в группе')



@router_group.message(Command('global_top_users'))
async def global_top_users_command_handler(message: Message):
    if str(message.chat.id)[0] != '-':
        clients = await sql.get_all_clients_sql()
        clients = sorted(clients, key=lambda x: x[5], reverse=True)
        mes = 'Топ 10 пользователей по количеству баллов\n\n'
        flag = False

        for i in range(0, 10):
            if clients[i][0] == str(message.from_user.id):
                mes += f'{i+1}. {clients[i][4]}(Вы) - {clients[i][5]}б.\n'
                flag = True
            else:
                mes += f'{i+1}. {clients[i][4]} - {clients[i][5]}б.\n'
        if flag == False:
            for i in range(0, len(clients)):
                if message.from_user.id == clients[i][0]:
                    mes += f'{i+1}. {clients[i][4]}(Вы) - {clients[i][5]}б.\n'
        await message.answer(mes)
    else:
        await message.answer('Эта команда работает только в личных сообщениях с ботом')
        
