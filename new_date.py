import datetime
import app.database.sqlite_db as sql
import asyncio

async def new_date():
    await sql.connection_sql()
    old_date = '2025-05-04'
    while True:
        time_moscow = datetime.timezone(datetime.timedelta(hours=3))
        today = str(datetime.datetime.now(time_moscow).date())
        if old_date != today:
            old_date = today
            await sql.new_date_sql()
        await asyncio.sleep(60)

        
async def main():
    await new_date()


if __name__ == "__main__":
    asyncio.run(main())