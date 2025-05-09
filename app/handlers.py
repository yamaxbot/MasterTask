from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import math

import app.database.sqlite_db as sql
import app.keyboards as kb
import app.other_func as otf

router = Router()


class AddTasks(StatesGroup):
    title = State()

class AddOneTask(StatesGroup):
    title = State()

class PasswordFriend(StatesGroup):
    password = State()

class ReminderTime(StatesGroup):
    time = State()


@router.message(Command('start'))
async def command_start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('👋Привет! Это бот, который поможет вам в улучшении вашей дисциплины, а также поможет удобно составлять и выполнять график дня.\n\n☄Здесь вы можете:\n-Создать график дня\n-Ежедневно отмечать выполненные задания\n-Формировать статистику, с помощью которой вы сможете оценить свою продуктивность\n\n📋Подробно познакомиться со всем функционалом вы сможете прочитав инструкцию, введя команду /help\n\n❓Если у вас возникли вопросы или же вы хотите предложить свою идею в развитии бота, пишите сюда: @TaskMasterSupportBot\n\n👨‍💻Наш канал, где выходят самые свежие новости про этого бота: @BestTaskMaster', reply_markup=kb.client_reply_keyboards)
    data = await sql.get_all_id_users_sql()
    if str(message.from_user.id) not in data:
        await sql.add_client_sql(message.from_user.id)


@router.message(Command('help'))
async def command_help_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('🗒Инструкция\n\n✏Выполнение заданий:\nПервым делом вам нужно создать ваши ежедневне задания с помощью кнопки Создать задания. После создания заданий вы можете ежедневно отмечать задания, которые вы сделали, с помощью кнопки Выполнить задания. Также если вы хотите удалить какое либо задание, или добавить новое, вы можете это сделать, нажав на кнопку Редактировать задания\n\n📊Статистика:\nЧтобы узнать статистику, где будет показываться сколько заданий вы сделали всего, нужно нажать на кнопку Статистика.\nЕсли вы хотите узнать в какие дни, какие задания вы делали, нужно нажать на кнопку ежедневная статистика.')


@router.message(F.text == '📖Создать задания')
async def create_tasks_handler(message: Message, state: FSMContext):
    await state.clear()
    global tasks_ls 
    tasks_ls = []
    aval_table = await sql.availability_of_table(message.from_user.id)
    if aval_table == 'no':
        await message.answer('‼️Пишите задания по одному сообщению.')
        await state.set_state(AddTasks.title)
    else:
        await message.answer('‼️У вас уже созданы задания, вы их можете отредактировать нажав на кнопку Редактировать задания')


@router.message(AddTasks.title)
async def create_tasks_state_handler(message: Message, state: FSMContext):
    global tasks_ls
    text = message.text.replace(' ', '_')
    if message.text not in tasks_ls:
        tasks_ls.append(text)
        await message.answer("😉Напишите ещё одно задания или нажмите кнопку Хватит", reply_markup=kb.stop_added_task_inlinekeyboard)
    else:
        await message.answer("‼️Точно такое задание уже есть. Напишите ещё одно задания или нажмите кнопку Хватит", reply_markup=kb.stop_added_task_inlinekeyboard)

@router.callback_query(F.data == 'stop_add_task')
async def stop_add_task_handler(callback: CallbackQuery, state: FSMContext):
    global tasks_ls

    if len(tasks_ls) != 0:
        await callback.answer()
        await sql.create_new_table_sql(tasks_ls, callback.from_user.id)
        await callback.message.answer(f'✅Вы добавили задания, теперь вам доступен просмотр статистики и выполнение заданий')
        await state.clear()
        tasks_ls = []



@router.message(F.text == '✏️Выполнить задания')
async def execute_tasks_handler(message: Message, state: FSMContext):
    await state.clear()
    aval_tasks = await sql.availability_of_table(message.from_user.id)
    if aval_tasks == 'yes':
        data = await sql.get_today_tasks_sql(message.from_user.id)
        data = data[0]
        mes = f'🗓Сегодняшняя дата:\n{data[0]}\n\n'
        columns = await sql.get_all_columns_sql(message.from_user.id)
        columns = [column.replace('_', ' ') for column in columns]
        for d in range(1, len(data)):
            if data[d] == '0':
                mes += f'{d} {columns[d]} - ❌\n'
            else: 
                mes += f'{d} {columns[d]} - ✅\n'
        
        mes += '\n‼️Чтобы задание выделилось галочкой или наоборот крестиком, нажмите на кнопку снизу с таким номером, под которым указано задание'
        await message.answer(mes, reply_markup=await kb.inline_number_task_kb(len(data)-1))
    else:
        await message.answer('‼️У вас пока не созданы задания, пожалуйста создайте их')


@router.callback_query(F.data.startswith('number_'))
async def change_state_task_handler(callback: CallbackQuery):
    await callback.answer()
    number = str(callback.data).replace('number_', '')
    await sql.change_state_task_sql(callback.from_user.id, number)

    data = await sql.get_today_tasks_sql(callback.from_user.id)
    data = data[0]
    mes = f'🗓Сегодняшняя дата:\n{data[0]}\n\n'
    columns = await sql.get_all_columns_sql(callback.from_user.id)
    columns = [column.replace('_', ' ') for column in columns]
    for d in range(1, len(data)):
        if data[d] == '0':
            mes += f'{d} {columns[d]} - ❌\n'
        else: 
            mes += f'{d} {columns[d]} - ✅\n'

    mes += '\n‼️Чтобы задание выделилось галочкой или наоборот крестиком, нажмите на кнопку снизу с таким номером, под которым указано задание'
    await callback.message.edit_text(mes, reply_markup=await kb.inline_number_task_kb(len(data)-1))


@router.message(F.text == '📈Ежедневная статистика')
async def daily_statics_handler(message: Message, state: FSMContext):
    await state.clear()
    aval_tasks = await sql.availability_of_table(message.from_user.id)
    if aval_tasks == 'yes':
        daily_tasks = await sql.get_all_daily_tasks_sql(message.from_user.id)
        main_mes = '📈Ежедневная статистика\n\n'
        for data in daily_tasks[-1: -8: -1][::-1]:
            mes = f'🗓Дата:\n{data[0]}\n'
            columns = await sql.get_all_columns_sql(message.from_user.id)
            columns = [column.replace('_', ' ') for column in columns]
            for d in range(1, len(data)):
                if data[d] == '0':
                    mes += f'{d} {columns[d]} - ❌\n'
                else: 
                    mes += f'{d} {columns[d]} - ✅\n'

            main_mes += mes + '\n\n'
        main_mes += f'{math.ceil(len(daily_tasks)/7)}/{math.ceil(len(daily_tasks)/7)}'
        
        await message.answer(main_mes, reply_markup=kb.inline_arroy_daily_tasks_kb)
    else:
        await message.answer('‼️У вас не созданы задания, пожалуйста создайте их')


@router.callback_query(F.data == 'arrow_left')
async def daily_statics_allow_left_handler(callback: CallbackQuery):
    await callback.answer()
    pages = str(callback.message.text).split()[-1].replace('/', ' ').split()
    current_n, total_n = int(pages[0]), int(pages[1])

    if current_n != 1:
        page_difference = total_n-current_n+1
        start_page = page_difference*7+1
        stop_page = start_page+7

        daily_tasks = await sql.get_all_daily_tasks_sql(callback.from_user.id)
        main_mes = 'Ежедневная статистика\n\n'
        for data in daily_tasks[-start_page: -stop_page: -1][::-1]:
            mes = f'Дата:\n{data[0]}\n'
            columns = await sql.get_all_columns_sql(callback.from_user.id)
            columns = [column.replace('_', ' ') for column in columns]
            for d in range(1, len(data)):
                if data[d] == '0':
                    mes += f'{d} {columns[d]} - ❌\n'
                else: 
                    mes += f'{d} {columns[d]} - ✅\n'

            main_mes += mes + '\n\n'
        main_mes += f'{current_n-1}/{math.ceil(len(daily_tasks)/7)}'
        
        await callback.message.edit_text(main_mes, reply_markup=kb.inline_arroy_daily_tasks_kb)


@router.callback_query(F.data == 'arrow_right')
async def daily_statics_allow_right_handler(callback: CallbackQuery):
    await callback.answer()
    pages = str(callback.message.text).split()[-1].replace('/', ' ').split()
    current_n, total_n = int(pages[0]), int(pages[1])

    if total_n != current_n:
        page_difference = total_n-current_n+1
        start_page = page_difference*7-13
        stop_page = start_page+7

        daily_tasks = await sql.get_all_daily_tasks_sql(callback.from_user.id)
        main_mes = 'Ежедневная статистика\n\n'
        for data in daily_tasks[-start_page: -stop_page: -1][::-1]:
            mes = f'Дата:\n{data[0]}\n'
            columns = await sql.get_all_columns_sql(callback.from_user.id)
            columns = [column.replace('_', ' ') for column in columns]
            for d in range(1, len(data)):
                if data[d] == '0':
                    mes += f'{d} {columns[d]} - ❌\n'
                else: 
                    mes += f'{d} {columns[d]} - ✅\n'

            main_mes += mes + '\n\n'
        main_mes += f'{current_n+1}/{math.ceil(len(daily_tasks)/7)}'
        
        await callback.message.edit_text(main_mes, reply_markup=kb.inline_arroy_daily_tasks_kb)


@router.message(F.text == '📊Статистика')
async def general_statistics_handler(message: Message, state: FSMContext):
    await state.clear()
    aval_tasks = await sql.availability_of_table(message.from_user.id)
    if aval_tasks == 'yes':
        data = await sql.get_all_daily_tasks_sql(message.from_user.id)
        columns = await sql.get_all_columns_sql(message.from_user.id)
        mes = '📊Ваша статистика за всё время\n\n'

        all_done_tasks = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                if j != 0:
                    all_done_tasks += int(data[i][j])
        mes += f'🌏Количество сделанных заданий за всё время: {all_done_tasks}\n\n'

        for j in range(len(data[0])):
            if j == 0:
                continue
            total_task = 0
            shock_mode = 0
            for i in range(len(data)):
                total_task += int(data[i][j])

                if data[i][j] == '0':
                    shock_mode = 0
                else:
                    shock_mode += 1
            mes += f'{j} Задание "{str(columns[j]).replace("_", " ")}":\nСделано всего - {total_task}\nУдарный режим - {shock_mode}\n\n'
        await message.answer(mes)
    else:
        await message.answer('‼️У вас нет заданий, пожалуйста создайте их')


@router.message(F.text == '📝Редактировать задания')
async def edit_tasks_handler(message: Message, state: FSMContext):
    await state.clear()
    aval_tasks = await sql.availability_of_table(message.from_user.id)
    if aval_tasks == 'yes':
        await message.answer('🌏Также вы можете добавить какое либо задание, вместе с этим, за все прошедшие дни, будет выделено, что вы не выполняли это задание\n\n🗑Вы можете удалить какое либо задание, при этом удалятся все данные и статистика об этом задании.\n\n', reply_markup=kb.edit_tasks_inline_kb)
    else:
        await message.answer('‼️У вас пока что нет заданий, пожалуйста создайте их')


@router.callback_query(F.data == 'add_task')
async def edit_task_add_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('‼️Напишите новое задание, которое хотите добавить', reply_markup=kb.inline_cancel_kb)
    await state.set_state(AddOneTask.title)


@router.message(AddOneTask.title)
async def edit_task_add_state_handler(message: Message, state: FSMContext):
    columns = await sql.get_all_columns_sql(message.from_user.id)
    text = message.text.replace(' ', '_')
    if text not in columns:
        await sql.add_one_column_sql(message.from_user.id, text)
        await message.answer(f'✅Вы добавили новое задание "{message.text}"')
        await state.clear()
    else:
        await message.answer('‼️Точно такоеже задание у вас уже есть. Напишите другое задание или отмените действие с помощью кнопки Отменить', reply_markup=kb.inline_cancel_kb)


@router.callback_query(F.data == 'delete_task')
async def edit_task_delete_handler(callback: CallbackQuery):
    await callback.answer()
    data = await sql.get_today_tasks_sql(callback.from_user.id)
    data = data[0]
    mes = f'📒Все ваши задания\n\n'
    columns = await sql.get_all_columns_sql(callback.from_user.id)
    columns = [column.replace('_', ' ') for column in columns]
    for d in range(1, len(data)):
        if data[d] == '0':
            mes += f'{d} {columns[d]}\n'
        else: 
            mes += f'{d} {columns[d]}\n'
    
    mes += '\n‼️Чтобы удалить задание, нажмите на кнопку снизу с номером'
    await callback.message.answer(mes, reply_markup=await kb.delete_one_task_inline(len(data)-1))


@router.callback_query(F.data.startswith('deletetask_'))
async def edit_task_delete_state_handler(callback: CallbackQuery):
    await callback.answer()
    number = str(callback.data).split('_')
    number = int(number[1])
    columns = await sql.get_all_columns_sql(callback.from_user.id)
    await sql.delete_one_column_sql(callback.from_user.id, columns[number])
    await callback.message.delete()
    await callback.message.answer(f"✅Задание {str(columns[number]).replace('_', ' ')} удалено")
    

@router.callback_query(F.data == 'cancel')
async def cancel_callback_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Действие отменено')


@router.message(F.text == '🙋‍♂️Статистика друга')
async def statistics_friend_handler(message: Message, state:FSMContext):
    await state.clear()
    await message.answer('🔑Здесь вы можете создать свой специальный код, чтобы ваш друг смог посмотреть вашу статистику.\n\n🔐Также вы можете посмотреть статистику своего друга, если у вас есть специальный код, который должен предоставить ваш друг', reply_markup=kb.inline_friend_statistics_kb)


@router.callback_query(F.data == 'my_code')
async def my_code_callback_handler(callback: CallbackQuery):
    await callback.answer()
    data = await sql.get_user_friend_statistics_sql(callback.from_user.id)
    if data == None:
        await callback.message.answer('🔑У вас пока нет кода. Вы можете его создать, нажав на кнопку создать код', reply_markup=kb.inline_create_delete_code_kb)
    else:
        await callback.message.answer(f'🔑Ваш код: `{data[1]}`\n🫵Кликните по нему чтобы скопировать\n\n🔓Любой кому вы отправите этот код, сможет посмотреть вашу статистику\n\n🗑Если вы хотите удалить код, чтобы ваши друзья потеряли доступ к вашей статистике, нажмите кнопку Удалить код', reply_markup=kb.inline_create_delete_code_kb,parse_mode="MARKDOWN")


@router.callback_query(F.data == 'create_code')
async def create_code_handler(callback: CallbackQuery):
    await callback.answer()
    data = await sql.get_user_friend_statistics_sql(callback.from_user.id)
    if data == None:
        code = await otf.generation_code()
        await sql.add_code_friend_statistics_sql(callback.from_user.id, code)
        await callback.message.edit_text(f'🔑Ваш код: `{code}`\n🫵Кликните по нему чтобы скопировать\n\n🔓Любой кому вы отправите этот код, сможет посмотреть вашу статистику\n\n🗑Если вы хотите удалить код, чтобы ваши друзья потеряли доступ к вашей статистике, нажмите кнопку Удалить код', reply_markup=kb.inline_create_delete_code_kb, parse_mode="MARKDOWN")
    else:
        await callback.message.answer('‼️У вас уже есть код')


@router.callback_query(F.data == 'delete_code')
async def delete_code_handler(callback: CallbackQuery):
    await callback.answer()
    data = await sql.get_user_friend_statistics_sql(callback.from_user.id)
    if data == None:
        await callback.message.answer('‼️У вас нет кода')
    else:
        await sql.delete_code_friend_statistics_sql(callback.from_user.id)
        await callback.message.edit_text('🔑У вас пока нет кода. Вы можете его создать, нажав на кнопку создать код', reply_markup=kb.inline_create_delete_code_kb)
        

@router.callback_query(F.data == 'friend_code')
async def friend_code_state_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('🔑Отправьте код, который вы получили от друга')
    await state.set_state(PasswordFriend.password)


@router.message(PasswordFriend.password)
async def friend_code_state_password_handler(message: Message, state: FSMContext):
    all_codes = await sql.get_all_friends_codes_sql()
    id_by_code = await sql.get_id_by_password_sql(message.text)

    if str(message.from_user.id) == id_by_code:
        await message.answer('‼️Это ваш собственный код')
    elif message.text in all_codes:
        await message.answer(f'🔐Код который вы ввели: `{message.text}`\n\n🙋‍♂️Вы можете посмотреть 2 статистики вашего друга', reply_markup=kb.inline_friend_statistics_all_kb, parse_mode="MARKDOWN")
        await state.clear()
    else:
        await message.answer('‼️Такого кода нет или он уже неактивен. Введите другой код или нажмите кнопку Отменить', reply_markup=kb.inline_cancel_kb)


@router.callback_query(F.data == 'general_statistics')
async def general_statistics_friend_handler(callback: CallbackQuery):
    await callback.answer()
    friend_password = list(str(callback.message.text).split())
    id_user = await sql.get_id_by_password_sql(friend_password[4])

    aval_tasks = await sql.availability_of_table(id_user)
    if aval_tasks == 'yes':
        data = await sql.get_all_daily_tasks_sql(id_user)
        columns = await sql.get_all_columns_sql(id_user)
        mes = '📊Cтатистика вашего друга за всё время\n\n'

        all_done_tasks = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                if j != 0:
                    all_done_tasks += int(data[i][j])
        mes += f'🌏Количество сделанных заданий за всё время: {all_done_tasks}\n\n'

        for j in range(len(data[0])):
            if j == 0:
                continue
            total_task = 0
            shock_mode = 0
            for i in range(len(data)):
                total_task += int(data[i][j])

                if data[i][j] == '0':
                    shock_mode = 0
                else:
                    shock_mode += 1
            mes += f'{j} Задание "{str(columns[j]).replace("_", " ")}":\nСделано всего - {total_task}\nУдарный режим - {shock_mode}\n\n'
        await callback.message.answer(mes)
    else:
        await callback.message.answer('‼️У данного пользователя нет заданий')



@router.callback_query(F.data == 'default_statistics')
async def daily_statics_friend_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    friend_password = list(str(callback.message.text).split())
    id_user = await sql.get_id_by_password_sql(friend_password[4])
    aval_tasks = await sql.availability_of_table(id_user)

    if aval_tasks == 'yes':
        daily_tasks = await sql.get_all_daily_tasks_sql(id_user)
        main_mes = f'🔐Код вашего друга: {friend_password[4]}\n\n📈Ежедневная статистика\n\n'
        for data in daily_tasks[-1: -8: -1][::-1]:
            mes = f'🗓Дата:\n{data[0]}\n'
            columns = await sql.get_all_columns_sql(id_user)
            columns = [column.replace('_', ' ') for column in columns]
            for d in range(1, len(data)):
                if data[d] == '0':
                    mes += f'{d} {columns[d]} - ❌\n'
                else: 
                    mes += f'{d} {columns[d]} - ✅\n'

            main_mes += mes + '\n\n'
        main_mes += f'{math.ceil(len(daily_tasks)/7)}/{math.ceil(len(daily_tasks)/7)}'
        
        await callback.message.answer(main_mes, reply_markup=kb.inline_arroy_daily_tasks_friend_kb)
    else:
        await callback.message.answer('‼️У вашего друга не созданы задания')


@router.callback_query(F.data == 'arrow_left_friend')
async def daily_statics_friend_allow_left_handler(callback: CallbackQuery):
    await callback.answer()
    pages = str(callback.message.text).split()[-1].replace('/', ' ').split()
    current_n, total_n = int(pages[0]), int(pages[1])
    code = list(str(callback.message.text).split())[3]
    id_user = await sql.get_id_by_password_sql(code)

    if current_n != 1:
        page_difference = total_n-current_n+1
        start_page = page_difference*7+1
        stop_page = start_page+7

        daily_tasks = await sql.get_all_daily_tasks_sql(id_user)
        main_mes = '📈Ежедневная статистика\n\n'
        for data in daily_tasks[-start_page: -stop_page: -1][::-1]:
            mes = f'Дата:\n{data[0]}\n'
            columns = await sql.get_all_columns_sql(id_user)
            columns = [column.replace('_', ' ') for column in columns]
            for d in range(1, len(data)):
                if data[d] == '0':
                    mes += f'{d} {columns[d]} - ❌\n'
                else: 
                    mes += f'{d} {columns[d]} - ✅\n'

            main_mes += mes + '\n\n'
        main_mes += f'{current_n-1}/{math.ceil(len(daily_tasks)/7)}'
        
        await callback.message.edit_text(main_mes, reply_markup=kb.inline_arroy_daily_tasks_friend_kb)


@router.callback_query(F.data == 'arrow_right_friend')
async def daily_statics_friend_allow_right_handler(callback: CallbackQuery):
    await callback.answer()
    pages = str(callback.message.text).split()[-1].replace('/', ' ').split()
    current_n, total_n = int(pages[0]), int(pages[1])
    code = list(str(callback.message.text).split())[3]
    id_user = await sql.get_id_by_password_sql(code)

    if total_n != current_n:
        page_difference = total_n-current_n+1
        start_page = page_difference*7-13
        stop_page = start_page+7

        daily_tasks = await sql.get_all_daily_tasks_sql(id_user)
        main_mes = 'Ежедневная статистика\n\n'
        for data in daily_tasks[-start_page: -stop_page: -1][::-1]:
            mes = f'Дата:\n{data[0]}\n'
            columns = await sql.get_all_columns_sql(id_user)
            columns = [column.replace('_', ' ') for column in columns]
            for d in range(1, len(data)):
                if data[d] == '0':
                    mes += f'{d} {columns[d]} - ❌\n'
                else: 
                    mes += f'{d} {columns[d]} - ✅\n'

            main_mes += mes + '\n\n'
        main_mes += f'{current_n+1}/{math.ceil(len(daily_tasks)/7)}'
        
        await callback.message.edit_text(main_mes, reply_markup=kb.inline_arroy_daily_tasks_friend_kb)


@router.message(F.text == '🔔Напоминание')
async def reminder_main_handler(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == 5227185772:
        await message.answer('Вы можете добавить время, в которое вам нужно отправить напоминание.\n\nТакже вы можете удалить все напоминания', reply_markup=kb.inline_add_delete_reminder_kb)
    else:
        await message.answer('Данная функция на данный момент не работает, но скоро будет работать')


@router.callback_query(F.data == 'add_time')
async def add_time_handler(callback: CallbackQuery, state: FSMContext):
    global ls_time
    ls_time = []
    await callback.message.answer('Пишите по одному время, в которое вам нужно отправлять напоминание. Формат должен быть строго следующим 00:00')
    await state.set_state(ReminderTime.time)


@router.message(ReminderTime.time)
async def add_time_state_handler(message: Message):
    global ls_time
    if message.text not in ls_time:
        ls_time.append(message.text)
        await message.answer('Напишите ещё время или нажмите кнопку хватит', reply_markup=kb.inline_stop_add_time_kb)
    else:
        await message.answer('Такое время уже есть, введите другое или нажмите кнопку хватит', reply_markup=kb.inline_stop_add_time_kb)


@router.callback_query(F.data == 'add_time_stop')
async def add_time_stop_state_handler(callback: CallbackQuery):
    global ls_time
    ls_time_str = '/'.join(ls_time)
    await sql.add_times_user_sql(callback.from_user.id, ls_time_str)
    await callback.message.answer('Мы будем отправлять вам напоминания в это время по мск, если у вас будут недоделаны задания')


@router.callback_query(F.data == 'delete_time')
async def delete_time_inline_kb_handler(callback: CallbackQuery):
    await sql.delete_times_user_sql(callback.from_user.id)
    await callback.answer('Ваши напоминания удалены, можете создать новые!')