import sqlite3 as sql
import datetime
time_moscow = datetime.timezone(datetime.timedelta(hours=3))

async def start_sql():
    global db, cur 

    db = sql.connect('data.db')
    cur = sql.Cursor(db)

    cur.execute("CREATE TABLE IF NOT EXISTS clients(id TEXT, subscription TEXT, reminder TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS friend_statistics(id TEXT, password TEXT)")


async def connection_sql():
    global db, cur 

    db = sql.connect('data.db')
    cur = sql.Cursor(db)


async def add_client_sql(tg_id):
    cur.execute("INSERT INTO clients VALUES(?, ?, ?)", (tg_id, 0, 0,))
    db.commit()


async def get_all_id_users_sql():
    data = cur.execute("SELECT id FROM clients").fetchall()
    all_id = []
    for tup in data:
        all_id.append(tup[0])
    return all_id


async def create_new_table_sql(tasks, tg_id):
    today = datetime.datetime.now(time_moscow).date()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {'tasks_table'+str(tg_id)}(date TEXT)")

    for task in tasks:
        cur.execute(f"ALTER TABLE {'tasks_table'+str(tg_id)} ADD COLUMN [{task}] TEXT DEFAULT '0'")
    str_mark = str(['?' for i in range(len(tasks)+1)]).replace("'", '')
    sql_request = f"INSERT INTO {'tasks_table'+str(tg_id)} VALUES({str_mark[1:-1]})"
    values_ls = [str(today)]
    for i in range(len(tasks)):
        values_ls.append('0')
    cur.execute(sql_request, tuple(values_ls))
    db.commit()


async def get_today_tasks_sql(tg_id):
    today = datetime.datetime.now(time_moscow).date()
    return cur.execute(f"SELECT * FROM {'tasks_table'+str(tg_id)} WHERE date = ?", (str(today), )).fetchall()


async def get_all_columns_sql(tg_id):
    data = cur.execute(f"PRAGMA table_info({'tasks_table'+str(tg_id)})").fetchall()
    columns = []
    for column in data:
        columns.append(column[1])
    return columns
    

async def change_state_task_sql(tg_id, number):
    today = str(datetime.datetime.now(time_moscow).date())
    data = cur.execute(f"PRAGMA table_info({'tasks_table'+str(tg_id)})").fetchall()
    get_state = cur.execute(f"SELECT [{data[int(number)][1]}] FROM {'tasks_table'+str(tg_id)} WHERE date = ?", (str(today), )).fetchone()[0]

    if get_state == '0':
        cur.execute(f"UPDATE {'tasks_table'+str(tg_id)} SET [{data[int(number)][1]}] = ? WHERE date = ?", ('1', today, ))
    else:
        cur.execute(f"UPDATE {'tasks_table'+str(tg_id)} SET [{data[int(number)][1]}] = ? WHERE date = ?", ('0', today, ))

    db.commit()


async def get_all_daily_tasks_sql(tg_id):
    return cur.execute(f"SELECT * FROM {'tasks_table'+str(tg_id)}").fetchall()
    

async def add_one_column_sql(tg_id, text):
    cur.execute(f"ALTER TABLE {'tasks_table'+str(tg_id)} ADD [{text}] TEXT DEFAULT '0'")
    db.commit()


async def delete_one_column_sql(tg_id, column):
    cur.execute(f"ALTER TABLE {'tasks_table'+str(tg_id)} DROP COLUMN [{column}]")
    db.commit()


async def new_date_sql():
    data = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    ls_table = [i[0] for i in data]
    today = str(datetime.datetime.now(time_moscow).date())
    for name in ls_table:
        if 'tasks_table' in name:
            tables = cur.execute(f"PRAGMA table_info({name})").fetchall()
            columns = []
            for column in tables:
                columns.append(column[1])
                
            str_mark = str(['?' for i in range(len(columns))]).replace("'", '')
            sql_request = f"INSERT INTO {name} VALUES({str_mark[1:-1]})"
            values_ls = [str(today)]
            for i in range(len(columns)-1):
                values_ls.append('0')
            cur.execute(sql_request, tuple(values_ls))
    db.commit()


async def availability_of_table(tg_id):
    data = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    name_table = 'tasks_table'+str(tg_id)
    data = [i[0] for i in data]
    if name_table in data:
        return 'yes'
    else:
        return 'no'


async def get_user_friend_statistics_sql(tg_id):
    return cur.execute("SELECT * FROM friend_statistics WHERE id = ?", (tg_id, )).fetchone()


async def add_code_friend_statistics_sql(tg_id, code):
    cur.execute('INSERT INTO friend_statistics VALUES(?, ?)', (tg_id, code, ))
    db.commit()


async def delete_code_friend_statistics_sql(tg_id):
    cur.execute("DELETE FROM friend_statistics WHERE id = ?", (tg_id, ))
    db.commit()


async def get_all_friends_codes_sql():
    data = cur.execute("SELECT * FROM friend_statistics").fetchall()
    all_date = []
    for code in data:
        all_date.append(code[1])
    return all_date


async def get_id_by_password_sql(password):
    data = cur.execute("SELECT * FROM friend_statistics WHERE password = ?", (password, )).fetchone()
    return data[0]