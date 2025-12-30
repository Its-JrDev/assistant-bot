import sqlite3
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def query(sql, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    results = cur.fetchall()
    conn.close()
    return results

def execute(sql, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    conn.close()

def login_user(dni, pin, telegram_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, curso FROM estudiantes WHERE dni=? AND pin=?", (dni, pin))
    user = cur.fetchone()
    if not user:
        conn.close()
        return None

    cur.execute("UPDATE estudiantes SET telegram_id=?, logged=1 WHERE dni=?", (telegram_id, dni))
    conn.commit()

    # Retornar usuario ya con estado actualizado
    cur.execute("SELECT id, nombre, curso, logged FROM estudiantes WHERE dni=?", (dni,))
    updated_user = cur.fetchone()
    conn.close()
    return updated_user

def logout_user(telegram_id):
    """
    Logs out a user by setting logged to 0 and clearing their telegram_id.
    Note: On logout, telegram_id is set to NULL and logged is set to 0.
    This differs from login, which sets both fields.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM estudiantes WHERE telegram_id=? AND logged=1",
        (telegram_id,)
    )
    user = cur.fetchone()

    if not user:
        conn.close()
        return False

    # On logout, both logged is set to 0 and telegram_id is cleared (set to NULL)
    cur.execute(
        "UPDATE estudiantes SET logged=0, telegram_id=NULL WHERE telegram_id=?",
        (telegram_id,)
    )
    conn.commit()
    conn.close()
    return True
