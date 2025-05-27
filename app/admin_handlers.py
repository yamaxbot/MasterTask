from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandObject
from aiogram import Bot, F, Router
from config import ADMINS
import app.database.sqlite_db as sql


router_admin = Router()


class NewsLetterState(StatesGroup):
    mes = State()


@router_admin.message(Command('admin_commands'))
async def all_admin_commands_handler(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer('Все команды администратора в этом боте:\n\n/statistics - показывает статистику по боту\n\n/newsletter - после нажатия этой команды, бот попросит текст, который в последующем, если вы ему предоставите текст, данный текст будет рассылаться по всем пользователям бота\n\n/refund+ключ доната - возврат звёзд задоначенных пользователем\n\n/add_channel+username канала - добавление канала в объязательные подписки\n\n/get_channels - бот вам отправит все каналы, в которых стоит объязательная подписка\n\n/delete_channel+username канала - бот удалит канал с данным юзернеймом с объязательной подписки')



@router_admin.message(Command('statistics'))
async def statistics_admin_command_handler(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id in ADMINS:
        all_users, new_users = await sql.statistics_command_sql()
        await message.answer(f'📈Статистика:\n\n👨‍💻Всего пользователей: {all_users}\n\n⏰️ Новых за сегодня: {new_users}')



@router_admin.message(Command('newsletter'))
async def newsletter_admins_command_handler(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id in ADMINS:
        await state.set_state(NewsLetterState.mes)
        await message.answer('Отправьте сообщение которое хотите разослать')



@router_admin.message(NewsLetterState.mes)
async def newsletter_admins_command_state_handler(message: Message, state: FSMContext):
    clients = await sql.get_all_id_users_sql()
    await state.clear()
    total = 0
    for client in clients:
        try:
            await message.send_copy(chat_id=client)
            total = total + 1
        except:
            continue
    await message.answer(text=f'Сообщение разослано, {total} людей')



@router_admin.message(Command('refund'))
async def command_refund_handler(message: Message, bot: Bot, command: CommandObject, state: FSMContext):
    await state.clear()
    if message.from_user.id in ADMINS:
        transaction_id = command.args
        data = await sql.get_id_by_transaction_id_sql(transaction_id)
        user_id = data[0]
        try:
            await bot.refund_star_payment(
                user_id=user_id,
                telegram_payment_charge_id=transaction_id
            )
        except Exception as e:
            print(e)



@router_admin.message(Command('add_channel'))
async def add_subscribe_channel_handler(message: Message, bot: Bot):
    if message.from_user.id in ADMINS:
        try:
            channel_username = list(str(message.text).split())[1]
            chat = await bot.get_chat(channel_username)
            member = await bot.get_chat_member(chat_id=chat.id, user_id=message.from_user.id)
            await sql.add_username_channel_sql(channel_username)
            await message.answer('Канал добавлен')
        except:
            await message.answer('Бота нет в канале или такого канала не существует')



@router_admin.message(Command('get_channels'))
async def get_cubscribe_channels_handler(message: Message):
    if message.from_user.id in ADMINS:
        sub_channels = await sql.get_all_username_channels_sql()
        if len(sub_channels) != 0:
            mes = 'Каналы с объязательной подпиской:\n'
            for channel in sub_channels:
                mes += f'{channel}\n'
            await message.answer(mes)
        else:
            await message.answer('Каналов с объязательной подпиской пока нет')



@router_admin.message(Command('delete_channel'))
async def delete_channel_subscribe_handler(message: Message):
    if message.from_user.id in ADMINS:
        sub_channels = await sql.get_all_username_channels_sql()
        channel_username = list(str(message.text).split())[1]
        if channel_username in sub_channels:
            await sql.delete_channel_subscribe_sql(channel_username)
            await message.answer('Этот канал успешно удалён')
        else:
            await message.answer('Такого канала в списке нет')
