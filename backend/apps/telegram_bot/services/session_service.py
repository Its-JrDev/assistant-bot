from database.db import query


def get_user_by_telegram(tid):
    rows = query(
        'SELECT id, nombre, curso, logged FROM estudiantes WHERE telegram_id=?',
        (tid,)
    )
    return rows[0] if rows else None
