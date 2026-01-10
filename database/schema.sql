-- Tabla de estudiantes
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT NOT NULL UNIQUE,
    pin TEXT NOT NULL,
    nombre TEXT NOT NULL,
    curso TEXT NOT NULL,
    telegram_id INTEGER UNIQUE,
    logged INTEGER DEFAULT 0
);

-- Tabla de horarios
CREATE TABLE IF NOT EXISTS horarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    curso TEXT NOT NULL,
    dia TEXT NOT NULL,
    hora_inicio TEXT NOT NULL,
    hora_fin TEXT NOT NULL,
    asignatura TEXT NOT NULL,
    profesor TEXT NOT NULL
);


-- Tabla de eventos
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    curso TEXT NOT NULL,
    evento TEXT NOT NULL,
    fecha TEXT NOT NULL,
    descripcion TEXT NOT NULL
);

-- Tabla de tareas
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    curso TEXT NOT NULL,
    materia TEXT NOT NULL,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_entrega TEXT NOT NULL
);
