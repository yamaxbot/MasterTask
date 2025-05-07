import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router

from config import TOKEN
import app.database.sqlite_db as sql

async def main():
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    await sql.start_sql()
    dp.include_router(router=router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())