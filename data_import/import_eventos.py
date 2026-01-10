from database.db import execute
import pandas as pd

REQUIRED_COLUMNS = [
    "curso",
    "evento",
    "fecha",
    "descripcion",
]

def insert_evento(row):
    fecha = row["fecha"]
    if pd.notna(fecha):
        fecha = fecha.strftime("%Y-%m-%d")
    else:
        fecha = None
        
    execute(
        """
        INSERT INTO eventos (curso, evento, fecha, descripcion)
        VALUES (?, ?, ?, ?)
        """,
        (
                row["curso"],
                row["evento"],
                fecha,
                row["descripcion"],
            )
        )