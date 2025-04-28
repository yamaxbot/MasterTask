import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router

from config import TOKEN
from app.database.sqlite_db import start_sql

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    await start_sql()
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())