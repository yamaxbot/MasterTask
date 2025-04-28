import sqlite3 as sql

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