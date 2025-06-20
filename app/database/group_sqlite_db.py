# Этот файл не подключен в файле main


import sqlite3 as sql
import datetime

time_moscow = datetime.timezone(datetime.timedelta(hours=3))

async def start_group_gsql():
    global db, cur

    db = sql.connect('data/group_data.db')
    cur = sql.Cursor(db)

    cur.execute("CREATE TABLE IF NOT EXISTS groups(g_id TEXT, name TEXT, points TEXT)")

    db.commit()


async def add_group_gsql(id, name):
    table_name = 'group_' + str(id)[1:]
    today = str(datetime.datetime.now(time_moscow).date())
    cur.execute("INSERT INTO groups VALUES(?, ?, ?)", (id, name, 0, ))
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}(date TEXT)")
    cur.execute(f"INSERT INTO {table_name} VALUES(?)", (today,))
    db.commit()


async def get_all_groups_id_gsql():
    ls = []
    data = cur.execute("SELECT * FROM groups").fetchall()
    for d in data:
        ls.append(d[0])
    return ls


async def get_group_columns_gsql(chat_id):
    table_name = f'group_{str(chat_id)[1:]}'
    data = cur.execute(f"PRAGMA table_info({table_name})").fetchall()
    columns = []
    for column in data:
        columns.append(column[1])
    return columns


async def add_new_user_group_gsql(chat_id, user_id, total_points):
    table_name = f'group_{str(chat_id)[1:]}'
    today = str(datetime.datetime.now(time_moscow).date())
    cur.execute(f"ALTER TABLE {table_name} ADD {'id_'+str(user_id)} TEXT DEFAULT 0")
    cur.execute(f"UPDATE {table_name} SET {'id_'+str(user_id)} = ? WHERE date = ?", (total_points, today, ))
    db.commit()


async def add_points_main_groups_gsql(chat_id, total_points):
    data = cur.execute("SELECT * FROM groups WHERE g_id = ?", (chat_id, )).fetchone()
    points = data[2]
    points = int(points) + total_points
    cur.execute("UPDATE groups SET points = ? WHERE g_id = ?", (points, chat_id, ))
    db.commit()


async def get_activity_user_today_gsql(chat_id, user_id):
    name_column = 'id_' + str(user_id)
    table_name = 'group_' + str(chat_id)[1:]
    today = str(datetime.datetime.now(time_moscow).date())
    
    return cur.execute(f"SELECT {name_column} FROM {table_name} WHERE date = ?", (today, )).fetchone()



async def add_points_gsql(chat_id, user_id, total_points):
    old_points = list(cur.execute("SELECT points FROM groups WHERE g_id = ?", (chat_id, )).fetchone())[0]
    points = int(old_points) + total_points
    cur.execute("UPDATE groups SET points = ? WHERE g_id = ?", (points, chat_id, ))

    today = str(datetime.datetime.now(time_moscow).date())
    table_name = 'group_' + str(chat_id)[1:]
    user_old_points = cur.execute(f"SELECT {'id_'+str(user_id)} FROM {table_name} WHERE date = ?", (today, )).fetchone()
    user_points = int(user_old_points[0]) + total_points
    cur.execute(f"UPDATE {table_name} SET {'id_'+str(user_id)} = ? WHERE date = ?", (user_points, today, ))
    db.commit()


async def all_groups_gsql():
    return cur.execute("SELECT * FROM groups").fetchall()


async def get_all_group_gsql(chat_id):
    table_name = 'group_' + str(chat_id)[1:]
    return cur.execute(f"SELECT * FROM {table_name}").fetchall()


async def new_date_groups_gsql():
    today = str(datetime.datetime.now(time_moscow).date())
    all_groups_id = cur.execute("SELECT g_id FROM groups").fetchall()
    ls = []
    for id in all_groups_id:
        ls.append(id[0])
    
    for chat_id in ls:
        table_name = 'group_' + str(chat_id)[1:]
        columns = cur.execute(f'PRAGMA table_info("{table_name}")').fetchall()
        columns = [column[1] for column in columns]
        mark = ''
        added_ls = [today]
        for i in range(len(columns)):
            mark += '?,'
            if i != 0:
                added_ls.append(0)

        req = f"INSERT INTO {table_name} VALUES(" + mark[0:-1] + ")"

        cur.execute(req, tuple(added_ls))
        db.commit()


async def plus_minus_points_group_gsql(user_id, chat_id, total_points):
    table_name = 'group_' + str(chat_id)[1:]
    today = str(datetime.datetime.now(time_moscow).date())
    data = cur.execute(f"SELECT {'id_'+str(user_id)} FROM {table_name} WHERE date = ?", (today, )).fetchone()
    points = int(data[0]) + total_points
    cur.execute(f"UPDATE {table_name} SET {'id_'+str(user_id)} = ? WHERE date = ?", (points, today, ))
    db.commit()


async def rename_group_gsql(chat_id, name):
    cur.execute("UPDATE groups SET name = ? WHERE g_id = ?", (name, chat_id, ))
    db.commit()


async def get_points_group_gsql(chat_id, user_id):
    table_name = 'group_' + str(chat_id)[1:]
    data = cur.execute(f"SELECT {'id_'+str(user_id)} FROM {table_name}").fetchall()
    data = [int(d[0]) for d in data]
    return sum(data)

