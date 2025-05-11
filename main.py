import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
import datetime
from config import TOKEN
import app.database.sqlite_db as sql


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    asyncio.create_task(new_date(bot))
    await sql.start_sql()
    dp.include_router(router=router)
    await dp.start_polling(bot)


async def new_date(bot):
    await sql.connection_sql()
    old_date = '2025-05-11'
    while True:
        time_moscow = datetime.timezone(datetime.timedelta(hours=3))
        today = str(datetime.datetime.now(time_moscow).date())
        if old_date != today:
            old_date = today
            await sql.new_date_sql()

        time = str(datetime.datetime.now(time_moscow).time())[:5]
        users = await sql.get_times_all_users_sql()

        for user in users:
            if user[1] == '0':
                continue
            task_user = await sql.get_today_tasks_sql(user[0])

            task_user = list(task_user[0])
            del task_user[0]

            if user[2] != 0 and '0' in task_user:
                times = str(user[2]).split('/')
                if time in times:
                    await bot.send_message(text='У вас есть невыполненные задания', chat_id=user[0])

        await asyncio.sleep(60)


async def start_project():
    await asyncio.gather(main())


if __name__ == "__main__":
    asyncio.run(start_project())