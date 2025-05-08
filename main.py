import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
import datetime
from config import TOKEN
import app.database.sqlite_db as sql

async def main():
    asyncio.create_task(new_date())
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    await sql.start_sql()
    dp.include_router(router=router)
    await dp.start_polling(bot)


async def new_date():
    await sql.connection_sql()
    old_date = '2025-05-08'
    while True:
        time_moscow = datetime.timezone(datetime.timedelta(hours=3))
        today = str(datetime.datetime.now(time_moscow).date())
        if old_date != today:
            old_date = today
            await sql.new_date_sql()
        await asyncio.sleep(60)


async def start_project():
    await asyncio.gather(main())


if __name__ == "__main__":
    asyncio.run(start_project())