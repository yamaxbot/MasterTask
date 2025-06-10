from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice
from aiogram.filters import Command, CommandObject
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot
from config import ADMINS

import math
import datetime

import app.database.sqlite_db as sql
import app.keyboards as kb
import app.other_func as otf


time_moscow = datetime.timezone(datetime.timedelta(hours=3))
router = Router()
tasks_sl = {}


class AddTask(StatesGroup):
    title = State()

class PasswordFriend(StatesGroup):
    password = State()

class AddPostAvtor(StatesGroup):
    avtor = State()

class AddPostName(StatesGroup):
    name = State()

class AddPostPhoto(StatesGroup):
    photo = State()

class AddPostContent(StatesGroup):
    content = State()



@router.message(Command('start'))
async def command_start_handler(message: Message, state: FSMContext):
    await state.clear()
    if str(message.chat.id)[0] == '-':
        await message.answer('👋Привет! Это бот, который поможет вам в улучшении вашей дисциплины, а также поможет удобно составлять и выполнять график дня. Также в этом боте есть миниигра для групп, вы можете узнать о ней введя команду /group_help\n\n☄Здесь вы можете:\n- Создать дневной\n- Ежедневно отмечать выполненные задания\n- Формировать статистику, с помощью которой вы сможете оценить свою продуктивность\n- Делиться статистикой с друзьями\n\n📋Подробно познакомиться со всем функционалом вы сможете прочитав инструкцию, введя команду /help\n\n❓Если у вас возникли вопросы или же вы хотите предложить свою идею в развитии бота(или вы нашли баги) пишите сюда: @TaskMasterSupportBot\n\n👨‍💻Наш канал, где выходят самые свежие новости про этого бота: @BestTaskMaster')
    else:
        await message.answer('👋Привет! Это бот, который поможет вам в улучшении вашей дисциплины, а также поможет удобно составлять и выполнять график дня. Также в этом боте есть миниигра для групп, вы можете узнать о ней введя команду /group_help\n\n☄Здесь вы можете:\n- Создать дневной план\n- Ежедневно отмечать выполненные задания\n- Формировать статистику, с помощью которой вы сможете оценить свою продуктивность\n- Делиться статистикой с друзьями\n\n📋Подробно познакомиться со всем функционалом вы сможете прочитав инструкцию, введя команду /help\n\n❓Если у вас возникли вопросы или же вы хотите предложить свою идею в развитии бота(или вы нашли баги) пишите сюда: @TaskMasterSupportBot\n\n👨‍💻Наш канал, где выходят самые свежие новости про этого бота: @BestTaskMaster', reply_markup=kb.client_reply_keyboards)
    
    data = await sql.get_all_id_users_sql()
    client = await sql.get_client_sql(message.from_user.id)
    if str(message.from_user.id) not in data:
        await sql.add_client_sql(message.from_user.id, message.from_user.username, message.from_user.first_name)
        await sql.create_new_table_sql(message.from_user.id)
    else:
        if message.from_user.username != client[1] or message.from_user.first_name != client[4]:
            await sql.update_username_user_sql(message.from_user.id, message.from_user.username)
            await sql.update_firstname_user_sql(message.from_user.id, message.from_user.first_name)

@router.message(Command('help'))
async def command_help_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('🗒Инструкция\n\n⏰️Время:\nВся работа со временем в этом боте работает по Московскому времени(МСК). Поэтому выбирая время в напоминаниях, имейте ввиду, что время там установлено по МСК. Также новый день в боте начинается в 00:00 по МСК.\n\n📝Изменить дневной план:\nЧтобы изменить дневной план, нажмите кнопку Изменить дневной план. После этого, нажмите на кнопку Добавить задания или на кнопку Удалить задания. Если вы нажали на кнопку добавить задания, то пишите новые задания по одному сообщению. Если вы нажали удалить сообщение, то нажмите цифры, под которым стоят ваши задания для их удаления.\n\n✏Дневной план:\nПосле создания дневного плана, вы можете ежедневно отмечать задания, которые вы создали, с помощью кнопки Дневной план. Чтобы отметить задание галочкой, нажмите на кнопку с цифрой, под номером которого расположено ваше задание. Если вы хотите обратно пометить задание крестиком, снова нажмите на эту цифру.\n\n📊Статистика:\nЧтобы узнать свою статистику, нажмите на кнопку Статистика. После чего вам будет предложено 2 вида статистики, это Общая статистика и Ежедневник. Если вы нажмёте на кнопку Статистика под сообщением, вы узнаете количество выполненных заданий, ударный режим и тд. А если вы нажмёте на кнопку Ежедневник, вы увидите в какие дни, какие задания вы сделали с момента регестрации в боте.\n\n🙋‍♂️Статистика друга:\nЧтобы узнать статистику друга или показать другу свою статистику, вам нужно нажать кнопку Статистика друга. Вы сможете создать свой код, чтобы поделиться своей статистикой с другом. А также вы можете посмотреть статистику друга, если он предоставит вам код для просмотра его статистики.Если вы хотите, чтобы ваши друзья не могли посмотреть вашу статистику, просто удалите код, так они потеряют доступ к вашей статистике.\n\n🔔Напоминание:\nЧтобы поставить напоминания в удобное вам время, вам нужно нажать кнопку Напоминания, а затем нажать кнопку Редактировать время. После нажатия выберите нужное время и нажмите кнопку сохранить. Время устанавливается по МСК, поэтому, при установке времени, переводите своё местное время в Московское!\n\n👤Профиль:\nНажав на кнопку Профиль, вы можете узнать характеристики своего аккаунта в этом боте')



@router.message(F.text == '✏️Дневной план')
async def execute_tasks_handler(message: Message, state: FSMContext, bot: Bot):
    await state.clear()

    ls_channel = []
    sub_channels = await sql.get_all_username_channels_sql()

    for c in sub_channels:
        try:
            chat = await bot.get_chat(c)
            member = await bot.get_chat_member(chat_id=chat.id, user_id=message.from_user.id)
            if str(member.status) == 'ChatMemberStatus.LEFT':
                ls_channel.append(c)
        except:
            await bot.send_message(text=f'С ботом в канале {c} произошла ошибка', chat_id=ADMINS[0])

    if len(ls_channel) == 0:
        aval_tasks = await sql.availability_of_table(message.from_user.id)
        if aval_tasks == 'yes':
            data = await sql.get_today_tasks_sql(message.from_user.id)
            data = data[0]
            if len(data) > 1:
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
                await message.answer('У вас нет заданий')
        else:
            await message.answer('‼️У вас пока не создан план дня, пожалуйста создайте его, нажав на кнопку Изменить дневной план')
    else:
        sub_mes = '💥Чтобы использовать данную функцию, вы должны быть подписаны на эти каналы:\n'
        for i in range(len(ls_channel)):
            sub_mes += f'{i+1} {ls_channel[i]}\n'
        sub_mes += '\n🔄Если вы подписались на все нужные каналы, запустите команду повторно'
        await message.answer(sub_mes)



@router.message(F.text == '📊Статистика')
async def main_keyboard_statistics_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer('📊Вы можете посмотреть статистику, где будут показаны количество сделанных заданий, а также количество ударных дней.\n\n🗓Также вы можете посмотреть ежедневник, где будет показано, какие задания вы делали ежедневно со дня регестрации.', reply_markup=kb.user_statistics_inline_keyboard)


@router.callback_query(F.data == 'default_statistics')
async def daily_statics_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await callback.answer()

    ls_channel = []
    sub_channels = await sql.get_all_username_channels_sql()

    for c in sub_channels:
        try:
            chat = await bot.get_chat(c)
            member = await bot.get_chat_member(chat_id=chat.id, user_id=callback.from_user.id)
            if str(member.status) == 'ChatMemberStatus.LEFT':
                ls_channel.append(c)
        except:
            await bot.send_message(text=f'С ботом в канале {c} произошла ошибка', chat_id=ADMINS[0])

    if len(ls_channel) == 0:
        aval_tasks = await sql.availability_of_table(callback.from_user.id)
        if aval_tasks == 'yes':
            daily_tasks = await sql.get_all_daily_tasks_sql(callback.from_user.id)
            main_mes = '📈Ваш ежедневник:\n\n'
            for data in daily_tasks[-1: -8: -1][::-1]:
                mes = f'🗓Дата:\n{data[0]}\n'
                columns = await sql.get_all_columns_sql(callback.from_user.id)
                columns = [column.replace('_', ' ') for column in columns]
                for d in range(1, len(data)):
                    if data[d] == '0':
                        mes += f'{d} {columns[d]} - ❌\n'
                    else: 
                        mes += f'{d} {columns[d]} - ✅\n'

                main_mes += mes + '\n\n'
            main_mes += f'{math.ceil(len(daily_tasks)/7)}/{math.ceil(len(daily_tasks)/7)}'
            
            await callback.message.answer(main_mes, reply_markup=kb.inline_arroy_daily_tasks_kb)
        else:
            await callback.message.answer('‼️У вас не создан дневной план, пожалуйста создайте его, нажав на кнопку Изменить дневной план')
    else:
        sub_mes = '💥Чтобы использовать данную функцию, вы должны быть подписаны на эти каналы:\n'
        for i in range(len(ls_channel)):
            sub_mes += f'{i+1} {ls_channel[i]}\n'
        sub_mes += '\n🔄Если вы подписались на все нужные каналы, запустите команду повторно'
        await callback.message.answer(sub_mes)



@router.callback_query(F.data == 'general_statistics')
async def general_statistics_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await callback.answer()
    
    ls_channel = []
    sub_channels = await sql.get_all_username_channels_sql()

    for c in sub_channels:
        try:
            chat = await bot.get_chat(c)
            member = await bot.get_chat_member(chat_id=chat.id, user_id=callback.from_user.id)
            if str(member.status) == 'ChatMemberStatus.LEFT':
                ls_channel.append(c)
        except:
            await bot.send_message(text=f'С ботом в канале {c} произошла ошибка', chat_id=ADMINS[0])

    if len(ls_channel) == 0:
        time_moscow = datetime.timezone(datetime.timedelta(hours=3))
        today = str(datetime.datetime.now(time_moscow).date())
        aval_tasks = await sql.availability_of_table(callback.from_user.id)
        if aval_tasks == 'yes':
            data = await sql.get_all_daily_tasks_sql(callback.from_user.id)
            columns = await sql.get_all_columns_sql(callback.from_user.id)
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

                    if data[i][0] == today:
                        shock_mode += 0
                        if data[i][j] == '1':
                            shock_mode += 1
                    elif data[i][j] == '0':
                        shock_mode = 0
                    else:
                        shock_mode += 1
                mes += f'{j} Задание "{str(columns[j]).replace("_", " ")}":\nСделано всего - {total_task}\nУдарный режим - {shock_mode}\n\n'
            await callback.message.answer(mes)
        else:
            await callback.message.answer('‼️У вас не создан дневной план, пожалуйста создайте его, нажав на кнопку Изменить дневной план')
    else:
        sub_mes = '💥Чтобы использовать данную функцию, вы должны быть подписаны на эти каналы:\n'
        for i in range(len(ls_channel)):
            sub_mes += f'{i+1} {ls_channel[i]}\n'
        sub_mes += '\n🔄Если вы подписались на все нужные каналы, запустите команду повторно'
        await callback.message.answer(sub_mes)



@router.message(F.text == '📝Изменить дневной план')
async def edit_tasks_handler(message: Message, state: FSMContext, bot: Bot):
    await state.clear()

    ls_channel = []
    sub_channels = await sql.get_all_username_channels_sql()

    for c in sub_channels:
        try:
            chat = await bot.get_chat(c)
            member = await bot.get_chat_member(chat_id=chat.id, user_id=message.from_user.id)
            if str(member.status) == 'ChatMemberStatus.LEFT':
                ls_channel.append(c)
        except:
            await bot.send_message(text=f'С ботом в канале {c} произошла ошибка', chat_id=ADMINS[0])

    if len(ls_channel) == 0:
        await message.answer('🌏Вы можете добавить какое либо ежедневное задание, нажав на кнопку Добавить задания.\n\n🗑Вы можете удалить какое либо задание, при этом удалятся все данные и статистика об этом задании.\n\n', reply_markup=kb.edit_tasks_inline_kb)
    else:
        sub_mes = '💥Чтобы использовать данную функцию, вы должны быть подписаны на эти каналы:\n'
        for i in range(len(ls_channel)):
            sub_mes += f'{i+1} {ls_channel[i]}\n'
        sub_mes += '\n🔄Если вы подписались на все нужные каналы, запустите команду повторно'
        await message.answer(sub_mes)



@router.message(F.text == '🙋‍♂️Статистика друга')
async def statistics_friend_handler(message: Message, state:FSMContext, bot: Bot):
    await state.clear()
    ls_channel = []
    sub_channels = await sql.get_all_username_channels_sql()

    for c in sub_channels:
        try:
            chat = await bot.get_chat(c)
            member = await bot.get_chat_member(chat_id=chat.id, user_id=message.from_user.id)
            if str(member.status) == 'ChatMemberStatus.LEFT':
                ls_channel.append(c)
        except:
            await bot.send_message(text=f'С ботом в канале {c} произошла ошибка', chat_id=ADMINS[0])

    if len(ls_channel) == 0:
        await message.answer('🔑Здесь вы можете создать свой специальный код, чтобы ваш друг смог посмотреть вашу статистику.\n\n🔐Также вы можете посмотреть статистику своего друга, если у вас есть специальный код, который должен предоставить ваш друг', reply_markup=kb.inline_friend_statistics_kb)
    else:
        sub_mes = '💥Чтобы использовать данную функцию, вы должны быть подписаны на эти каналы:\n'
        for i in range(len(ls_channel)):
            sub_mes += f'{i+1} {ls_channel[i]}\n'
        sub_mes += '\n🔄Если вы подписались на все нужные каналы, запустите команду повторно'
        await message.answer(sub_mes)



@router.message(F.text == '🔔Напоминание')
async def reminder_main_handler(message: Message, state: FSMContext, bot: Bot):
    await state.clear()

    ls_channel = []
    sub_channels = await sql.get_all_username_channels_sql()

    for c in sub_channels:
        try:
            chat = await bot.get_chat(c)
            member = await bot.get_chat_member(chat_id=chat.id, user_id=message.from_user.id)
            if str(member.status) == 'ChatMemberStatus.LEFT':
                ls_channel.append(c)
        except:
            await bot.send_message(text=f'С ботом в канале {c} произошла ошибка', chat_id=ADMINS[0])

    if len(ls_channel) == 0:
        data = await sql.get_times_user_sql(message.from_user.id)
        if data[2] == '0':
            await message.answer('⏰️Нажав на кнопку Редактировать время, вы сможете добавить время, в которое вам нужно отправить напоминание и удалить время напоминаний, которое уже вам не нужно.\n\n⏳Время устанавливается по МСК!\n\n📒У вас пока нет напоминаний', reply_markup=kb.inline_add_delete_reminder_kb)
        else:
            times = str(data[2]).replace('/', '\n')
            await message.answer(f'⏰️Нажав на кнопку Редактировать время, вы сможете добавить время, в которое вам нужно отправить напоминание и удалить время напоминаний, которое уже вам не нужно.\n\n⏳Время устанавливается по МСК!\n\n📒Ваши напоминания сработают в это время по МСК:\n{times}', reply_markup=kb.inline_add_delete_reminder_kb)
    else:
        sub_mes = '💥Чтобы использовать данную функцию, вы должны быть подписаны на эти каналы:\n'
        for i in range(len(ls_channel)):
            sub_mes += f'{i+1} {ls_channel[i]}\n'
        sub_mes += '\n🔄Если вы подписались на все нужные каналы, запустите команду повторно'
        await message.answer(sub_mes)



@router.message(F.text == '👤Профиль')
async def profile_user_handler(message: Message, state: FSMContext):
    await state.clear()

    client = await sql.get_client_sql(message.from_user.id)
    tasks_user = await sql.get_today_tasks_sql(message.from_user.id)
    tasks_user = tasks_user[0]
    all_daily_tasks = await sql.get_all_daily_tasks_sql(message.from_user.id)
    shock_mode = 0
    for day in all_daily_tasks:
        if '1' in day:
            shock_mode += 1
        elif day == all_daily_tasks[-1]:
            continue
        else:
            shock_mode = 0
    reg_date = str(client[3]).split('-')
    reg_date = reg_date[1] + '.' + reg_date[2] + '.' + reg_date[0]
    await message.answer(f'👤Ваш профиль:\n\nДата регестрации: {reg_date}\nКоличество напоминаний: {len(client[2].split("/"))}\nКоличество ударных дней: {shock_mode}\nКоличество заданий: {len(tasks_user)-1}')


    
@router.callback_query(F.data.startswith('number_'))
async def change_state_task_handler(callback: CallbackQuery):
    mes_date = str(callback.message.text).split()
    today = str(datetime.datetime.now(time_moscow).date())

    if mes_date[2] == today:
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
    else:
        await callback.answer(f'Это задания прошлых дней, чтобы отметить задания сегодня, нажмите ещё раз кнопку Выполнить задания')



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



@router.callback_query(F.data == 'add_task')
async def edit_task_add_handler(callback: CallbackQuery, state: FSMContext):
    global tasks_sl
    await state.clear()
    tasks_sl[callback.from_user.id] = []
    await callback.answer()
    await callback.message.answer('‼️Напишите новые задание, которое хотите добавить. Пишите каждое задание по отдельному сообщению', reply_markup=kb.inline_cancel_kb)
    await state.set_state(AddTask.title)



@router.message(AddTask.title)
async def edit_task_add_state_handler(message: Message, state: FSMContext):
    global tasks_sl
    columns = await sql.get_all_columns_sql(message.from_user.id)
    text = message.text.replace(' ', '_')
    if text not in columns and text not in tasks_sl[message.from_user.id]:
        await message.answer('✍Напишите ещё одно задание или нажмите кнопку хватит', reply_markup=kb.stop_added_task_inlinekeyboard)
        new_tasks = list(tasks_sl[message.from_user.id])
        new_tasks.append(text)
        tasks_sl[message.from_user.id] = new_tasks
    else:
        await message.answer('‼️Точно такоеже задание у вас уже есть. Напишите другое задание или нажмите кнопку Хватит', reply_markup=kb.inline_cancel_kb)



@router.callback_query(F.data == 'stop_add_task')
async def stop_add_task_handler(callback: CallbackQuery, state: FSMContext):
    global tasks_sl
    await callback.answer()
    await state.clear()

    if callback.from_user.id in tasks_sl.keys() and len(tasks_sl[callback.from_user.id]) != 0:
        await sql.add_columns_sql(callback.from_user.id, tasks_sl[callback.from_user.id])
        await callback.message.answer(f'✅Вы добавили задания')
        del tasks_sl[callback.from_user.id]



@router.callback_query(F.data == 'delete_task')
async def edit_task_delete_handler(callback: CallbackQuery):
    await callback.answer()
    aval_tasks = await sql.availability_of_table(callback.from_user.id)
    if aval_tasks == 'yes':
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
    else:
        await callback.message.answer('‼️У вас итак нет заданий, чтобы создать их нажите на кнопку Добавить задания')



@router.callback_query(F.data.startswith('deletetask_'))
async def edit_task_delete_state_handler(callback: CallbackQuery):
    await callback.answer()
    number = str(callback.data).split('_')
    number = int(number[1])
    columns = await sql.get_all_columns_sql(callback.from_user.id)
    await sql.delete_one_column_sql(callback.from_user.id, columns[number])
    await callback.message.delete()
    await callback.message.answer(f"✅Задание {str(columns[number]).replace('_', ' ')} удалено")
    
    aval_tasks = await sql.availability_of_table(callback.from_user.id)
    if aval_tasks == 'yes':
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
    else:
        await callback.message.answer('‼️У вас больше нет заданий!')



@router.callback_query(F.data == 'cancel')
async def cancel_callback_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Действие отменено')



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
        all_code = await sql.get_all_friends_codes_sql()
        while True:
            code = await otf.generation_code()
            if code not in all_code:
                await sql.add_code_friend_statistics_sql(callback.from_user.id, code)
                await callback.message.edit_text(f'🔑Ваш код: `{code}`\n🫵Кликните по нему чтобы скопировать\n\n🔓Любой кому вы отправите этот код, сможет посмотреть вашу статистику\n\n🗑Если вы хотите удалить код, чтобы ваши друзья потеряли доступ к вашей статистике, нажмите кнопку Удалить код', reply_markup=kb.inline_create_delete_code_kb, parse_mode="MARKDOWN")
                break
    else:
        await callback.message.answer('‼️У вас уже есть код')



@router.callback_query(F.data == 'delete_code')
async def delete_code_handler(callback: CallbackQuery):
    await callback.answer()
    data = await sql.get_user_friend_statistics_sql(callback.from_user.id)
    if data == None:
        await callback.message.answer('‼️У вас нет кода')
    else:
        await sql.not_active_code_friend_statistics_sql(callback.from_user.id)
        await callback.message.edit_text('🔑У вас пока нет кода. Вы можете его создать, нажав на кнопку создать код', reply_markup=kb.inline_create_delete_code_kb)
        


@router.callback_query(F.data == 'friend_code')
async def friend_code_state_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('🔑Отправьте код, который вы получили от друга')
    await state.set_state(PasswordFriend.password)



@router.message(PasswordFriend.password)
async def friend_code_state_password_handler(message: Message, state: FSMContext):
    all_codes = await sql.get_all_friends_codes_sql()
    if message.text in all_codes:
        id_by_code = await sql.get_id_by_password_sql(message.text)

        if str(message.from_user.id) == id_by_code:
            await message.answer('‼️Это ваш собственный код. Введите другой код или нажмите кнопку отменить!')
        elif message.text in all_codes:
            await message.answer(f'🔐Код который вы ввели: `{message.text}`\n\n🙋‍♂️Вы можете посмотреть 2 статистики вашего друга', reply_markup=kb.inline_friend_statistics_all_kb, parse_mode="MARKDOWN")
            await state.clear()
    else:
        await message.answer('‼️Такого кода нет или он уже неактивен. Введите другой код или нажмите кнопку Отменить', reply_markup=kb.inline_cancel_kb)



@router.callback_query(F.data == 'general_statistics_friend')
async def general_statistics_friend_handler(callback: CallbackQuery):
    await callback.answer()
    time_moscow = datetime.timezone(datetime.timedelta(hours=3))
    today = str(datetime.datetime.now(time_moscow).date())
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

                if data[i][0] == today:
                    shock_mode += 0
                    if data[i][j] == '1':
                        shock_mode += 1
                elif data[i][j] == '0':
                    shock_mode = 0
                else:
                    shock_mode += 1

            mes += f'{j} Задание "{str(columns[j]).replace("_", " ")}":\nСделано всего - {total_task}\nУдарный режим - {shock_mode}\n\n'
        await callback.message.answer(mes)
    else:
        await callback.message.answer('‼️У вашего друга не созданы задания')



@router.callback_query(F.data == 'default_statistics_friend')
async def daily_statics_friend_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    friend_password = list(str(callback.message.text).split())
    id_user = await sql.get_id_by_password_sql(friend_password[4])
    aval_tasks = await sql.availability_of_table(id_user)

    if aval_tasks == 'yes':
        daily_tasks = await sql.get_all_daily_tasks_sql(id_user)
        main_mes = f'🔐Код вашего друга: {friend_password[4]}\n\n📈Ежедневник друга:\n\n'
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
        main_mes = f'🔐Код вашего друга: {code}\n\n📈Ежедневная статистика\n\n'
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
        main_mes = f'🔐Код вашего друга: {code}\n\n📈Ежедневная статистика\n\n'
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



@router.callback_query(F.data == 'edit_time')
async def edit_time_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    count_colon = str(callback.message.text).count(':')
    if count_colon == 0:
        await callback.message.answer('👨‍💻Нажмите на определённое время, в которое вам нужно отправить напоминание. Если вы хотите удалить определённое время, то нажмите на это время ещё раз и оно удалится\n\n⏳Время устанавливается по МСК!\n\n📒Ваши напоминания сработают в это время по МСК:', reply_markup=kb.inline_all_times_reminder_kb)
    else:
        times_data = str(callback.message.text).split('📒Ваши напоминания сработают в это время по МСК:')
        await callback.message.answer(f'👨‍💻Нажмите на определённое время, в которое вам нужно отправить напоминание. Если вы хотите удалить определённое время, то нажмите на это время ещё раз и оно удалится\n\n⏳Время устанавливается по МСК!\n\n📒Ваши напоминания сработают в это время по МСК:{times_data[1]}', reply_markup=kb.inline_all_times_reminder_kb)
    await callback.message.delete()



@router.callback_query(F.data.startswith('remtime_'))
async def edit_time_callback_handler(callback: CallbackQuery):
    await callback.answer()
    callback_time = list(str(callback.data).split('_'))[1]
    callback_time = callback_time[:2] + ':' + callback_time[2:]
    
    mes_split = str(callback.message.text).split('📒Ваши напоминания сработают в это время по МСК:')
    times_data = mes_split[1].split('\n')
    del times_data[0]
    if callback_time not in times_data:
        text = callback.message.text + '\n' + callback_time
        await callback.message.edit_text(text=text, reply_markup=kb.inline_all_times_reminder_kb)
    else:
        ind_callback_time = times_data.index(callback_time)
        del times_data[ind_callback_time]
        text = mes_split[0] + '📒Ваши напоминания сработают в это время по МСК:' + '\n' + '\n'.join(times_data)
        await callback.message.edit_text(text=text, reply_markup=kb.inline_all_times_reminder_kb)



@router.callback_query(F.data == 'save_time')
async def add_time_stop_state_handler(callback: CallbackQuery):    
    await callback.answer()
    times = list(str(callback.message.text).split('📒Ваши напоминания сработают в это время по МСК:'))[1]
    if times == '':
        await sql.add_times_user_sql(callback.from_user.id, '0')
        await callback.message.delete()
        await callback.message.answer('⏰️Нажав на кнопку Редактировать время, вы сможете добавить время, в которое вам нужно отправить напоминание и удалить время напоминаний, которое уже вам не нужно.\n\n⏳Время устанавливается по МСК!\n\n📒У вас пока нет напоминаний', reply_markup=kb.inline_add_delete_reminder_kb)
        await callback.message.answer('✅Сохранено!')
    else:
        times = times.replace('\n', '/')
        times = times[1:]
        await sql.add_times_user_sql(callback.from_user.id, times)
        await callback.message.delete()
        
        data = await sql.get_times_user_sql(callback.from_user.id)
        times = str(data[2]).replace('/', '\n')
        await callback.message.answer(f'⏰️Нажав на кнопку Редактировать время, вы сможете добавить время, в которое вам нужно отправить напоминание и удалить время напоминаний, которое уже вам не нужно.\n\n⏳Время устанавливается по МСК!\n\n📒Ваши напоминания сработают в это время по МСК:\n{times}', reply_markup=kb.inline_add_delete_reminder_kb)
            
        await callback.message.answer('✅Сохранено!')



