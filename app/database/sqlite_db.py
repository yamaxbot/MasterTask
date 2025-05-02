import sqlite3 as sql
from datetime import date


async def start_sql():
    global db, cur 

    db = sql.connect('data.db')
    cur = sql.Cursor(db)

    cur.execute("CREATE TABLE IF NOT EXISTS clients(id TEXT, subscription TEXT)")
    db.commit()


async def get_all_id_users_sql():
    data = cur.execute("SELECT id FROM clients").fetchall()
    all_id = []
    for tup in data:
        all_id.append(tup[0])
    return all_id


async def create_new_table_sql(tasks, tg_id):
    today = date.today()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {'tasks_table'+str(tg_id)}(date TEXT)")
    for task in tasks:
        cur.execute(f"ALTER TABLE {'tasks_table'+str(tg_id)} ADD COLUMN {task} TEXT NOT NULL")
    str_mark = str(['?' for i in range(len(tasks)+1)]).replace("'", '')
    sql_request = f"INSERT INTO {'tasks_table'+str(tg_id)} VALUES({str_mark[1:-1]})"
    values_ls = [str(today)]
    for i in range(len(tasks)):
        values_ls.append('0')
    cur.execute(sql_request, tuple(values_ls))
    db.commit()


async def get_today_tasks_sql(tg_id):
    today = date.today()
    return cur.execute(f"SELECT * FROM {'tasks_table'+str(tg_id)} WHERE date = ?", (str(today), )).fetchall()


async def get_all_table_sql(tg_id):
    data = cur.execute(f"PRAGMA table_info({'tasks_table'+str(tg_id)})").fetchall()
    columns = []
    for column in data:
        columns.append(column[1])
    return columns
    

async def change_state_task_sql(tg_id, number):
    today = str(date.today())
    data = cur.execute(f"PRAGMA table_info({'tasks_table'+str(tg_id)})").fetchall()
    get_state = cur.execute(f"SELECT {data[int(number)][1]} FROM {'tasks_table'+str(tg_id)} WHERE date = ?", (str(today), )).fetchone()[0]
    
    if get_state == '0':
        cur.execute(f"UPDATE {'tasks_table'+str(tg_id)} SET {data[int(number)][1]} = ? WHERE date = ?", ('1', today, ))
    else:
        cur.execute(f"UPDATE {'tasks_table'+str(tg_id)} SET {data[int(number)][1]} = ? WHERE date = ?", ('0', today, ))

    db.commit()


async def get_all_daily_tasks_sql(tg_id):
    return cur.execute(f"SELECT * FROM {'tasks_table'+str(tg_id)}").fetchall()
    

async def add_one_column_sql(tg_id, text):
    cur.execute(f"ALTER TABLE {'tasks_table'+str(tg_id)} ADD {text} TEXT DEFAULT '0'")
    db.commit()


async def delete_one_column_sql(tg_id, column):
    cur.execute(f"ALTER TABLE {'tasks_table'+str(tg_id)} DROP COLUMN {column}")
    db.commit()