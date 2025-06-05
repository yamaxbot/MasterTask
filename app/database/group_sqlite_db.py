import sqlite3 as sql
import datetime

time_moscow = datetime.timezone(datetime.timedelta(hours=3))

async def start_group_sql():
    global db, cur

    db = sql.connect('data/group_data.db')
    cur = sql.Cursor(db)

    cur.execute("CREATE TABLE IF NOT EXISTS groups(g_id TEXT, name TEXT)")

    db.commit()


async def add_group_gsql(id, name):
    table_name = 'group_' + str(id)
    today = str(datetime.datetime.now(time_moscow).date())
    cur.execute("INSERT INTO groups VALUES(?, ?)", (id, name, ))
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}(date TEXT, points TEXT, people TEXT)")
    cur.execute(f"INSERT INTO {table_name} VALUES(?, ?, ?)", (today, 0, 0, ))
    db.commit()