from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import math

import app.database.sqlite_db as sql
import app.keyboards as kb

router = Router()


class AddTasks(StatesGroup):
    title = State()

class AddOneTask(StatesGroup):
    title = State()

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
        await message.answer('‼️Пишите задачи, который вам нужно делать по одному. Если вы написали все задания, нажмите кнопку Хватит')
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
    await callback.answer()
    await sql.create_new_table_sql(tasks_ls, callback.from_user.id)
    await callback.message.answer(f'✅Вы добавили задания, теперь вам доступен просмотр статистики и выполнение заданий')
    await state.clear()


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
        
        mes += '\n‼️Чтобы задание выделилось галочкой, нажмите на кнопку снизу с номером'
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
        main_mes = 'Ежедневная статистика\n\n'
        for data in daily_tasks[-1: -8: -1][::-1]:
            mes = f'Дата:\n{data[0]}\n'
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
        mes = 'Ваша статистика за всё время\n\n'

        all_done_tasks = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                if j != 0:
                    all_done_tasks += int(data[i][j])
        mes += f'Количество сделанных заданий за всё время: {all_done_tasks}\n\n'

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
            mes += f'Задание "{str(columns[j]).replace('_', ' ')}":\nСделано всего - {total_task}\nУдарный режим - {shock_mode}\n\n'
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
    await callback.message.answer('‼️Напишите новое задание, которое хотите добавить')
    await state.set_state(AddOneTask.title)


@router.message(AddOneTask.title)
async def edit_task_add_state_handler(message: Message, state: FSMContext):
    await sql.add_one_column_sql(message.from_user.id, message.text.replace(' ', '_'))
    await message.answer(f'✅Вы добавили новое задание "{message.text}"')
    await state.clear()


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
    await callback.message.answer(f'✅Задание "{str(columns[number]).replace('_', ' ')}" удалено')
    

@router.message(F.text == '🙋‍♂️Статистика друга')
async def statistics_friend_handler(message: Message, state:FSMContext):
    await state.clear()
    await message.answer('Данная функция пока не работает, но скоро будет доступна')