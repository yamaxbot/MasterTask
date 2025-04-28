import sqlite3 as sq

async def start_sq():
    global db, cur

    db = sq.connect('data.db')
    cur = sq.Cursor(db)
    
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT, username TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS goods(name TEXT photo TEXT des TEXT price INTEGER)")

    db.commit()


async def sql_add_user(tg_id, name, username):
    cur.execute("INSERT INTO users VALUES(?, ?, ?)", (tg_id, name, username))
    db.commit()


async def sql_get_user(tg_id):
    data = cur.execute("SELECT * FROM users WHERE id = ?", (tg_id,)).fetchone()
    return data


async def sql_update_user(tg_id):
    cur.execute("UPDATE users SET id = ?, name = ?, username = ? WHERE id = ?", (tg_id, 0, 0, tg_id))
    db.commit()


async def sql_delete_user(tg_id):
    cur.execute("DELETE FROM users WHERE id = ?", (tg_id, ))
    db.commit()



async def get_tovars_categories(category):
    return cur.execute("SELECT * FROM catalog WHERE categories = ?", (category, )).fetchall()
    
    
async def get_tovar(n):
    return cur.execute("SELECT * FROM catalog WHERE name = ?", (n, )).fetchone()


async def delete_tovar(n):
    cur.execute("DELETE FROM catalog WHERE name = ?", (n, ))
    db.commit()


async def admin_or_no(user):
    admin = cur.execute("SELECT * FROM admin WHERE user = ?", (user, )).fetchone()
    if admin:
        return True
    else:
        return False
    

async def add_admin_sql(username):
    cur.execute("INSERT INTO admin VALUES(?)", tuple(username.values()))
    db.commit()


async def delete_admin_sql(username):
    cur.execute("DELETE FROM admin WHERE user = ?", tuple(username.values()))
    db.commit()


async def get_categories():
    return cur.execute("SELECT * FROM categories").fetchall()


async def add_category_sql(c):
    cur.execute("INSERT INTO categories VALUES(?)", tuple(c.values()))
    db.commit()


async def delete_category_sql(categ):
    cur.execute("DELETE FROM categories WHERE category = ?", tuple(categ.values()))
    db.commit()


async def category_yes_no_sql(categ):
    categor = cur.execute("SELECT * FROM categories WHERE category = ?", tuple(categ.values())).fetchone()
    if categor:
        return True
    else:
        return False
    

async def category_tovar(tovar):
    return cur.execute("SELECT category FROM catalog ")


async def get_name_tovars():
    return cur.execute("SELECT name FROM catalog").fetchall()


async def get_admins_sql():
    return cur.execute("SELECT * from admin").fetchall()

