import sqlite3
conn = sqlite3.connect("database/data.db")
cur = conn.cursor()

cur.execute("""
INSERT INTO estudiantes (dni, pin, nombre, curso)
VALUES (?, ?, ?, ?)
""", ("12345678", "4321", "Alumno Prueba", "1A"))

conn.commit()
conn.close()

print("Estudiante insertado.")
cur.execute("""
INSERT INTO horarios (curso, dia, hora_inicio, hora_fin, materia, profesor) VALUES
('1A', 'Lunes', '08:00', '09:00', 'Matemáticas', 'Juan Pérez'),
('1A', 'Lunes', '09:00', '10:00', 'Lengua', 'María Gómez'),
('1A', 'Martes', '08:00', '09:00', 'Ciencias', 'Luis Rodríguez'),
('1A', 'Martes', '09:00', '10:00', 'Historia', 'Ana Martínez'),

('1B', 'Lunes', '08:00', '09:00', 'Matemáticas', 'Carlos Sánchez'),
('1B', 'Lunes', '09:00', '10:00', 'Lengua', 'Laura Fernández'),
('1B', 'Martes', '08:00', '09:00', 'Ciencias', 'Javier López'),
('1B', 'Martes', '09:00', '10:00', 'Historia', 'Sofía Díaz');
""")

conn.commit()
conn.close()

print("Horario insertado.")