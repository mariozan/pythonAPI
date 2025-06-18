import sqlite3

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        conn.commit()

def add_user(name, email, age):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, age) VALUES (?, ?, ?)
        """, (name, email, age))
        conn.commit()

def get_users():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

def get_user_by_id(user_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

def update_user(user_id, name, email, age):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?
        """, (name, email, age, user_id))
        conn.commit()

init_db()
# add_user('Mario', 'mario@correo.com', 32)
user = get_user_by_id(2)
print(user)
update_user(2, 'Luigi', 'luigi@correo.com', 35)
print(get_users())