import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router

from app.database.sqlite_db import start_sq         # Импортируем функцию

async def main():
    bot = Bot(token='7593277021:AAEgwGUAbhW6qhp-PvZo81IQeQsrDUC-ICQ')
    dp = Dispatcher()
    await start_sq()        # Запускаем функцию
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())