from database.db import execute 
import pandas as pd

REQUIRED_COLUMNS = [
    "curso",
    "materia",
    "titulo",
    "descripcion",
    "fecha_entrega",
]

def insert_tarea(row):
    fecha_entrega = row["fecha_entrega"]
    if pd.notna(fecha_entrega):
        fecha_entrega = fecha_entrega.strftime("%Y-%m-%d")
    else:
        fecha_entrega = None

    execute(
        """
        INSERT INTO tareas (curso, materia, titulo, descripcion, fecha_entrega)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            row["curso"],
            row["materia"],
            row["titulo"],
            row["descripcion"],
            fecha_entrega,
        )
    )