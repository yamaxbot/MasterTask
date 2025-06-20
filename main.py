import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.admin_handlers import router_admin
from app.group_handlers import router_group
import datetime
from config import TOKEN

import app.database.sqlite_db as sql
import app.database.group_sqlite_db as gsql


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    asyncio.create_task(new_date(bot))
    await sql.start_sql()
    await gsql.start_group_gsql()
    dp.include_router(router=router)
    dp.include_router(router=router_admin)
    await dp.start_polling(bot)


async def new_date(bot):
    await sql.connection_sql()
    old_date = await sql.get_date_sql()
    old_date = list(old_date)[0]
    while True:
        time_moscow = datetime.timezone(datetime.timedelta(hours=3))
        today = str(datetime.datetime.now(time_moscow).date())
        time = str(datetime.datetime.now(time_moscow).time())[:5]
        if old_date != today:
            await sql.new_main_date_sql(old_date)
            old_date = today
            await sql.new_date_sql()

        users = await sql.get_times_all_users_sql()

        for user in users:
            if user[1] == '0':
                continue
            task_user = await sql.get_today_tasks_sql(user[0])

            task_user = list(task_user[0])
            del task_user[0]

            if user[2] != '0' and '0' in task_user:
                times = str(user[2]).split('/')
                if time in times:
                    await bot.send_message(text='У вас есть невыполненные задания', chat_id=user[0])

        await asyncio.sleep(60)


async def start_project():
    await asyncio.gather(main())


if __name__ == "__main__":
    asyncio.run(start_project())