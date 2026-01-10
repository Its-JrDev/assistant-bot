from database.db import execute

REQUIRED_COLUMNS = [
    "curso",
    "dia",
    "hora_inicio",
    "hora_fin",
    "asignatura",
    "profesor",
]

def insert_horario(row):
    hora_inicio = (
        row["hora_inicio"].strftime("%H:%M")
        if hasattr(row["hora_inicio"], "strftime")
        else str(row["hora_inicio"])
    )

    hora_fin = (
        row["hora_fin"].strftime("%H:%M")
        if hasattr(row["hora_fin"], "strftime")
        else str(row["hora_fin"])
    )

    execute(
        """
        INSERT INTO horarios (curso, dia, hora_inicio, hora_fin, asignatura, profesor)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            row["curso"],
            row["dia"],
            hora_inicio,
            hora_fin,
            row["asignatura"],
            row["profesor"],
        )
    )
