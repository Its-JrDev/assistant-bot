from database.db import query

def get_user_by_telegram(tid):
    """
    Retrieve a user by their Telegram ID.

    Args:
        tid (int): Telegram user ID.

    Returns:
        tuple: (id, nombre, curso, logged) if user is found, otherwise None.
    """
    rows = query(
        "SELECT id, nombre, curso, logged FROM estudiantes WHERE telegram_id=?",
        (tid,)
    )
    return rows[0] if rows else None
