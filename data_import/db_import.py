import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

DB_PATH = "database/data.db"
EXCEL_PATH = "excel/data.xlsx"  # ajusta si lo necesitas


# ─────────────────────────────────────────────
# MAIN IMPORT
# ─────────────────────────────────────────────

def import_excel():
    """
    Importa todas las hojas del Excel y decide qué hacer según su nombre.
    """
    if not Path(EXCEL_PATH).exists():
        print("❌ Archivo Excel no encontrado")
        return

    xls = pd.ExcelFile(EXCEL_PATH)

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        sheet = sheet_name.lower().strip()

        if sheet == "horarios":    
            import_horarios(df)
        elif sheet == "tareas":
            import_tareas(df)
        elif sheet == "eventos":
            import_eventos(df)
        else:
            print(f"⚠️ Hoja ignorada: {sheet_name}")


# ─────────────────────────────────────────────
# HORARIOS
# ─────────────────────────────────────────────

def import_horarios(df: pd.DataFrame):
    from data_import.import_horarios import REQUIRED_COLUMNS, insert_horario
    
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            print(f"❌ Falta la columna requerida en horarios: {col}")
            return

    inserted = 0
    
    for _, row in df.iterrows():
        insert_horario(row)
        inserted += 1

    print(f"✅ Horarios importados correctamente: {inserted}")


# ─────────────────────────────────────────────
# TAREAS
# ─────────────────────────────────────────────

def import_tareas(df: pd.DataFrame):
    from data_import.import_tareas import REQUIRED_COLUMNS, insert_tarea
    
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            print(f"❌ Falta la columna requerida en tareas: {col}")
            return

    inserted = 0

    for _, row in df.iterrows():
        insert_tarea(row)
        inserted += 1

    print(f"✅ Tareas importadas correctamente: {inserted}")

# ─────────────────────────────────────────────
# EVENTOS
# ─────────────────────────────────────────────

def import_eventos(df: pd.DataFrame):
    from data_import.import_eventos import REQUIRED_COLUMNS, insert_evento

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            print(f"❌ Falta la columna requerida en eventos: {col}")
            return

    inserted = 0

    for _, row in df.iterrows():
        insert_evento(row)
        inserted += 1

    print(f"✅ Eventos importados correctamente: {inserted}")

# ─────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import_excel()
