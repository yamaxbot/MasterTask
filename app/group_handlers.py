from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, F, Router
from aiogram.filters import Command

import app.database.group_sqlite_db as gsql
import app.database.sqlite_db as sql
import app.other_func as otf
import app.keyboards as kb


router_group = Router()

totalt = 0


@router_group.message(F.text.startswith('/add_group'))
async def add_group_handler(message: Message):
    all_groups = await gsql.get_all_groups_id_gsql()

    if str(message.chat.id)[0] == '-' and str(message.text).count('+') == 1 and str(message.chat.id) not in all_groups:
        name = list(str(message.text).split('+'))[1]
        await gsql.add_group_gsql(message.chat.id, name)
        await message.answer('Группа добавлена')
    else:
        if str(message.chat.id)[0] != '-':
            await message.answer('Эта команда работает только в группе')
        elif str(message.chat.id) in all_groups:
            await message.answer('Ваша группа уже зарегистрирована, вы можете только изменить её имя введя команду /rename+Новое название группы')
        elif str(message.text).count('+') != 1:
            await message.answer('Вы ввели команду некорректно. Корректный вид:\n/add_group+Название для команды(группы)\n\nНе забывайте про "+" его тоже надо писать')



@router_group.message(F.text.startswith('/upgrade'))
async def command_upgrade_handler(message: Message, bot: Bot):
    data = await sql.get_all_id_users_sql()
    client = await sql.get_client_sql(message.from_user.id)
    if str(message.from_user.id) not in data:
        await sql.add_client_sql(message.from_user.id, message.from_user.username, message.from_user.first_name)
        await sql.create_new_table_sql(message.from_user.id)
    else:
        if message.from_user.username != client[1] or message.from_user.first_name != client[4]:
            await sql.update_username_user_sql(message.from_user.id, message.from_user.username)
            await sql.update_firstname_user_sql(message.from_user.id, message.from_user.first_name)

    all_groups = await gsql.get_all_groups_id_gsql()
    if str(message.chat.id)[0] == '-':
        if str(message.chat.id) in all_groups:    
            total_points = await otf.random_num()
            client = await sql.get_client_sql(message.from_user.id)
            columns = await gsql.get_group_columns_gsql(message.chat.id)
            if f'id_{message.from_user.id}' not in columns:
                await gsql.add_new_user_group_gsql(message.chat.id, message.from_user.id, total_points)
                await gsql.add_points_main_groups_gsql(message.chat.id, total_points)
                await sql.add_points_clients_sql(message.from_user.id, total_points)
                all_group_points = await gsql.get_points_group_gsql(message.chat.id, message.from_user.id)

                await bot.send_message(chat_id=message.chat.id, text=f'{client[4]} зачислено {total_points} б.\n\nКоличество баллов у данного пользователя в этой группе: {all_group_points}', reply_to_message_id=message.message_id)
            else:
                activ = await gsql.get_activity_user_today_gsql(message.chat.id, message.from_user.id)

                if activ[0] == '0':
                    await gsql.add_points_gsql(message.chat.id, message.from_user.id, total_points)
                    await sql.add_points_clients_sql(message.from_user.id, total_points)
                    all_group_points = await gsql.get_points_group_gsql(message.chat.id, message.from_user.id)
                    await bot.send_message(chat_id=message.chat.id, text=f'{client[4]} зачислено {total_points} б.\n\nКоличество баллов у данного пользователя в этой группе: {all_group_points}', reply_to_message_id=message.message_id)

                else:
                    await bot.send_message(chat_id=message.chat.id, text=f'Вы уже пользовались данной функцией сегодня, эта функция работает раз в сутки. В следующий раз вы можете воспользоваться с ней в 00:00 по МСК. Если вы хотите набрать баллы, можете сразиться с другими участниками группы, введя команду /battle', reply_to_message_id=message.message_id)
        else:
            await message.answer('Ваша группа не зарегистрирована, пожалуйста зарегистрируйтесь')
    else:
        await message.answer('Эта команда работает только в группе')



@router_group.message(F.text.startswith('/top_groups'))
async def top_global_chats_handler(message: Message):
    if str(message.chat.id)[0] == '-':
        all_chats = await gsql.all_groups_gsql()
        all_chats = sorted(all_chats, key=lambda x: int(x[2]), reverse=True)
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
            for i in range(0, len(all_chats)):
                if all_chats[i][0] == str(message.chat.id):
                    mes += f'{i+1} {all_chats[i][1]}(Ваша группа) - {all_chats[i][2]} б.'
                    break
        await message.answer(mes)
    else:
        await message.answer('Эта команда работает только в группе')



@router_group.message(F.text.startswith('/top_users'))
async def top_users_handler(message: Message):
    all_groups = await gsql.get_all_groups_id_gsql()

    if str(message.chat.id)[0] == '-':
        if str(message.chat.id) in all_groups:
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

            mes = 'Топ 10 участников этой группы\n\n'
            i = 1
            for key_val in users_points:
                client = await sql.get_client_sql(key_val[0])
                mes += f'{i} {client[4]} - {key_val[1]} б.\n'
                i += 1

            await message.answer(mes)
        else:
            await message.answer('Ваша группа не зарегистрирована, пожалуйста зарегистрируйтесь')
    else:
        await message.answer('Эта команда работает только в группе')



@router_group.message(F.text.startswith('/global_top_users'))
async def global_top_users_command_handler(message: Message):
    if str(message.chat.id)[0] != '-':
        clients = await sql.get_all_clients_sql()
        clients = sorted(clients, key=lambda x: int(x[5]), reverse=True)
        mes = 'Топ 10 пользователей по количеству баллов\n\n'
        flag = False

        for i in range(0, 10):
            if clients[i][0] == str(message.from_user.id):
                mes += f'{i+1}. {clients[i][4]}(Вы) - {clients[i][5]} б.\n'
                flag = True
            else:
                mes += f'{i+1}. {clients[i][4]} - {clients[i][5]} б.\n'
        if flag == False:
            for i in range(0, len(clients)):
                if message.from_user.id == clients[i][0]:
                    mes += f'{i+1}. {clients[i][4]}(Вы) - {clients[i][5]} б.\n'
        await message.answer(mes)
    else:
        await message.answer('Эта команда работает только в личных сообщениях с ботом')



@router_group.message(F.text.startswith('/battle'))
async def group_battle_handler(message: Message):
    if str(message.chat.id)[0] == '-':
        data = await sql.get_all_id_users_sql()
        client = await sql.get_client_sql(message.from_user.id)
        if str(message.from_user.id) not in data:
            await sql.add_client_sql(message.from_user.id, message.from_user.username, message.from_user.first_name)
            await sql.create_new_table_sql(message.from_user.id)
        else:
            if message.from_user.username != client[1] or message.from_user.first_name != client[4]:
                await sql.update_username_user_sql(message.from_user.id, message.from_user.username)
                await sql.update_firstname_user_sql(message.from_user.id, message.from_user.first_name)

        total_points = await gsql.get_points_group_gsql(message.chat.id, message.from_user.id)
        if int(total_points) >= 5:
            await message.answer(f'⚔{client[4]} вызывает на сражение\n\n🏆Вы можете сразится если у вас больше 5 баллов. Если вы выигрываете, получаете 10 баллов, если проигрываете, теряете 5 баллов.\n\n🎲Решает абсолютный рандом!!!', reply_markup=await kb.battle_inline_kb(message.from_user.id))
        elif int(total_points) < 5:
            await message.answer('У вас не хватает баллов, минимально должно быть 5')
    else:
        await message.answer('Эта команда работает только в группе')



@router_group.callback_query(F.data.startswith('battle_kb_'))
async def battle_kb_start_handler(callback: CallbackQuery):
    await callback.answer()
    user_id = list(str(callback.data).split('_'))[2]
    total1 = await gsql.get_points_group_gsql(callback.message.chat.id, callback.from_user.id)
    total2 = await gsql.get_points_group_gsql(callback.message.chat.id, user_id)
    ls = [user_id, str(callback.from_user.id)]
    if str(callback.from_user.id) != user_id and int(total1) >= 5 and int(total2) >= 5:
        win = await otf.random_battle_num()
        if win == 0:
            await gsql.plus_minus_points_group_gsql(ls[0], callback.message.chat.id, 5)
            await sql.add_points_clients_sql(ls[0], 5)
            await gsql.plus_minus_points_group_gsql(ls[1], callback.message.chat.id, -5)
            await sql.add_points_clients_sql(ls[1], -5)
            win_client = await sql.get_client_sql(ls[0])
            loss_client = await sql.get_client_sql(ls[1])
        else:
            await gsql.plus_minus_points_group_gsql(ls[1], callback.message.chat.id, 5)
            await sql.add_points_clients_sql(ls[1], 5)
            await gsql.plus_minus_points_group_gsql(ls[0], callback.message.chat.id, -5)
            await sql.add_points_clients_sql(ls[0], -5)
            win_client = await sql.get_client_sql(ls[1])
            loss_client = await sql.get_client_sql(ls[0])

        await callback.message.edit_text(f'🏆Победитель: {win_client[4]}\n😭Проигравший: {loss_client[4]}\n\n{win_client[4]} +5 б.\n{loss_client[4]} -5 б.')
    else:
        await callback.message.answer('Сражаться можно только с другими и если обоих пользователей больше 5 баллов')


@router_group.message(F.text.startswith('/rename'))
async def rename_handler(message: Message):
    if str(message.chat.id)[0] == '-' and str(message.text).count('+') == 1:
        name = list(str(message.text).split('+'))[1]
        await gsql.rename_group_gsql(message.chat.id, name)
        await message.answer(f'Имя группы переименовано на {name}')
    else:
        if str(message.chat.id)[0] != '-':
            await message.answer('Команда доступна только в группе')
        elif str(message.text).count('+') != 1:
            await message.answer('Команда введена некорректно. Корректный вид:\n/rename+Новое название для группы')



@router_group.message(F.text.startswith('/group_help'))
async def my_points_command_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('👨‍💻Данный бот нужен для планировки дневных задания, но также в этом боте есть мини игра, с которой вы можете играть с друзьями.\n\n📋До начала игры, вам нужно зарегистрировать группу как клан, чтобы это сделать, нужно ввести команду /add_group, поставить знак "+" и написать название своего клана. Команда должна выглядеть так:\n/add_group+Название для вашего клана(группы)\n\n🏆Теперь вы можете соревноваться как и с друзьями в группе, так и с другими пользователями. Побеждает тот, у кого больше баллов. 1 раз в сутки вы можете заходить и нажимать кнопку /upgrade по которой вам на рандом будут даваться баллы. Также вы можете сражаться с участниками за баллы нажав на кнопку /battle. Вы можете купить дополнительную попытку за 10 звёзд нажав на кнопку /buy\n\n🎁В боте идёт конкурс до 20 июля. Группа в которой будет больше всего баллов, получит 150 звёзд, которые мы разделим среди 10 самых активных пользователей группы(каждому по 15 звёзд). Также 3 самых активных пользователя по баллам в глобальном топе получат дополнительно по 25 звёзд. Баллы в глобальном топе  - это сумма баллов пользователей со всех групп вместевзятых. Поэтому чем в большем количестве групп вы играете, тем больше у вас будет баллов в глобальном топе.\n\n🤖Итоги конкурса будут 20 июля, если вы выйграете, бот вам сам лично скажет куда написать. На фейков не ведитесь!\n\n❓По вопросам пишите сюда: @TaskMasterSupportBot')



@router_group.message(F.text.startswith('/buy'))
async def donate_group_handler(message: Message, bot: Bot):
    await message.answer('Данная функция пока недоступна')



@router_group.callback_query(F.data.startswith('battle_cancel_'))
async def battle_cancel_inline_handler(callback: CallbackQuery):
    await callback.answer()
    user_id = list(str(callback.data).split('_'))[2]
    if user_id == str(callback.from_user.id):
        await callback.message.edit_text(text='Сражение отменено!')
    else:
        await callback.message.answer('Сражение может отменить только пользователь, который начал сражение')