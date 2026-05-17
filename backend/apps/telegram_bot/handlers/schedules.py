from database.db import get_connection


def get_schedule(curso: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT dia, hora_inicio, hora_fin, asignatura, profesor
        FROM horarios
        WHERE curso=?
        ORDER BY
            CASE dia
                WHEN 'Lunes' THEN 1
                WHEN 'Martes' THEN 2
                WHEN 'Miércoles' THEN 3
                WHEN 'Jueves' THEN 4
                WHEN 'Viernes' THEN 5
                WHEN 'Sábado' THEN 6
                WHEN 'Domingo' THEN 7
            END,
            hora_inicio
    """, (curso,))
    rows = cur.fetchall()
    conn.close()
    return rows


def format_schedule(rows):
    if not rows:
        return '❌ No hay horario cargado para tu curso.'
    text = '📚 *Horario semanal*\n'
    current_day = None
    for dia, h_ini, h_fin, materia, profesor in rows:
        if dia != current_day:
            text += f'\n📆 *{dia}*\n'
            current_day = dia
        text += f'🕒 {h_ini}-{h_fin} — *{materia}*'
        if profesor:
            text += f' ({profesor})'
        text += '\n'
    return text


def is_valid_dni(dni: str) -> bool:
    return dni.isdigit() and 7 <= len(dni) <= 11


def is_valid_pin(pin: str) -> bool:
    return pin.isdigit() and 4 <= len(pin) <= 6
