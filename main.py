import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router

import time
import datetime
from config import TOKEN
import app.database.sqlite_db as sql

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    await sql.start_sql()
    task1 = await asyncio.create_task(new_date())
    dp.include_router(router=router)
    await dp.start_polling(bot)


async def new_date():
    old_date = '2025-05-02'
    time_moscow = datetime.timezone(datetime.timedelta(hours=3))
    today = datetime.datetime.now(time_moscow).date()
    if old_date != today:
        old_date = today
        await sql.new_date_sql()


if __name__ == "__main__":
    asyncio.run(main())