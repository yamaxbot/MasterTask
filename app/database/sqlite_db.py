import sqlite3 as sql
import datetime

time_moscow = datetime.timezone(datetime.timedelta(hours=3))

async def start_sql():
    global db, cur 

    db = sql.connect('data/data.db')
    cur = sql.Cursor(db)

    cur.execute("CREATE TABLE IF NOT EXISTS clients(id TEXT, username TEXT, reminder TEXT, registration_date TEXT, firstname TEXT, all_points TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS friend_statistics(id TEXT, password TEXT, active TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS subscribe_channel(username TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS main_date_table(date TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS posts(post_id TEXT, user_id TEXT, username TEXT, date TEXT, avtor TEXT, name TEXT, photo TEXT, content TEXT)")
    db.commit()


async def connection_sql():
    global db, cur 

    db = sql.connect('data/data.db')
    cur = sql.Cursor(db)


async def get_date_sql():
    return cur.execute("SELECT * FROM main_date_table").fetchone()


async def new_main_date_sql(old_date):
    today = str(datetime.datetime.now(time_moscow).date())
    cur.execute("UPDATE main_date_table SET date = ? WHERE date = ?", (today, old_date, ))
    db.commit()


async def add_client_sql(tg_id, username, firstname):
    today = str(datetime.datetime.now(time_moscow).date())
    cur.execute("INSERT INTO clients VALUES(?, ?, ?, ?, ?, ?)", (tg_id, username, 0, today, firstname, 0, ))
    db.commit()


async def get_all_clients_sql():
    return cur.execute("SELECT * FROM clients").fetchall()


async def get_client_sql(tg_id):
    return cur.execute("SELECT * FROM clients WHERE id = ?", (tg_id, )).fetchone()

    
async def get_all_id_users_sql():
    data = cur.execute("SELECT id FROM clients").fetchall()
    all_id = []
    for tup in data:
        all_id.append(tup[0])
    return all_id


async def create_new_table_sql(tg_id):
    today = str(datetime.datetime.now(time_moscow).date())
    cur.execute(f"CREATE TABLE IF NOT EXISTS {'tasks_table'+str(tg_id)}(date TEXT)")
    cur.execute(f"INSERT INTO {'tasks_table'+str(tg_id)} VALUES(?)", (today, ))
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
    

async def add_columns_sql(tg_id, columns):
    for text in columns:
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
    data = cur.execute(f"SELECT * FROM {'tasks_table'+str(tg_id)}").fetchone()
    if len(data) > 1:
        return 'yes'
    else:
        return 'no'


async def get_user_friend_statistics_sql(tg_id):
    return cur.execute("SELECT * FROM friend_statistics WHERE id = ? AND active = ?", (tg_id, '1', )).fetchone()


async def add_code_friend_statistics_sql(tg_id, code):
    cur.execute('INSERT INTO friend_statistics VALUES(?, ?, ?)', (tg_id, code, '1'))
    db.commit()


async def not_active_code_friend_statistics_sql(tg_id):
    cur.execute("UPDATE friend_statistics SET active = ? WHERE id = ?", ('0', tg_id, ))
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


async def add_times_user_sql(tg_id, times):
    cur.execute("UPDATE clients SET reminder = ? WHERE id = ?", (times, tg_id, ))
    db.commit()


async def delete_times_user_sql(tg_id):
    cur.execute("UPDATE clients SET reminder = ? WHERE id = ?", ('0', tg_id, ))
    db.commit()


async def get_times_all_users_sql():
    return cur.execute("SELECT * FROM clients").fetchall()


async def get_times_user_sql(tg_id):
    return cur.execute("SELECT * FROM clients WHERE id = ?", (tg_id, )).fetchone()


async def statistics_command_sql():
    today = str(datetime.datetime.now(time_moscow).date())
    all_users = cur.execute("SELECT * FROM clients").fetchall()
    new_users = cur.execute("SELECT * FROM clients WHERE registration_date = ?", (today, )).fetchall()
    return len(all_users), len(new_users)


async def add_username_channel_sql(username):
    cur.execute("INSERT INTO subscribe_channel VALUES(?)", (username, ))
    db.commit()


async def get_all_username_channels_sql():
    data = cur.execute("SELECT * FROM subscribe_channel").fetchall()
    ls = []
    for c in data:
        ls.append(c[0])
    return ls


async def delete_channel_subscribe_sql(username):
    cur.execute("DELETE FROM subscribe_channel WHERE username = ?", (username, ))
    db.commit()


async def get_user_sql(tg_id):
    return cur.execute("SELECT * FROM clients WHERE id = ?", (tg_id, )).fetchone()


async def update_username_user_sql(tg_id, username):
    cur.execute("UPDATE clients SET username = ? WHERE id = ?", (username, tg_id, ))
    db.commit()


async def update_firstname_user_sql(tg_id, firstname):
    cur.execute("UPDATE clients SET firstname = ? WHERE id = ?", (firstname, tg_id, ))
    db.commit()


async def add_points_clients_sql(tg_id, total_points):
    client = cur.execute("SELECT * FROM clients WHERE id = ?", (tg_id, )).fetchone()
    points = int(client[5]) + total_points
    cur.execute("UPDATE clients SET all_points = ? WHERE id = ?", (points, tg_id, ))
    db.commit()
