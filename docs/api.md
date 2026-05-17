# API Reference

## Authentication

### POST /api/token/
Obtener JWT token.

```json
{"username": "directivo", "password": "admin123"}
```

Response:
```json
{"access": "eyJ...", "refresh": "eyJ..."}
```

### POST /api/token/refresh/
Refrescar token.

```json
{"refresh": "eyJ..."}
```

---

## Endpoints

All endpoints require `Authorization: Bearer <token>` header.

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/users/ | List users (directivo only) |
| POST | /api/users/ | Create user (directivo only) |
| GET | /api/users/{id}/ | User detail |
| PUT/PATCH | /api/users/{id}/ | Update user |
| DELETE | /api/users/{id}/ | Delete user |

**Permissions:** Solo `directivo` puede acceder.

### Students
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/students/ | List students |
| POST | /api/students/ | Create student |
| GET | /api/students/{id}/ | Student detail |
| PUT/PATCH | /api/students/{id}/ | Update student |
| DELETE | /api/students/{id}/ | Delete student |

**Filters:**
- `?course=1` — filtrar por curso
- `?search=nombre_o_dni` — búsqueda por nombre o DNI
- `?ordering=nombre` — ordenar por nombre (`-nombre` para descendente)

### Courses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | /api/courses/ | List / Create |
| GET/PUT/PATCH/DELETE | /api/courses/{id}/ | Detail / Update / Delete |

**Filters:**
- `?search=nombre` — búsqueda por nombre
- `?ordering=name` — ordenar

**Permissions:** `directivo` full access; `profesor` read-only.

### Schedules
| Method | Endpoint |
|--------|----------|
| GET/POST | /api/schedules/ |
| GET/PUT/PATCH/DELETE | /api/schedules/{id}/ |

**Filters:**
- `?course=1` — filtrar por curso
- `?day=Lunes` — filtrar por día
- `?ordering=day` — ordenar

**Permissions:** `directivo` full access; `profesor` read-only.

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/tasks/ | List tasks |
| POST | /api/tasks/ | Create task |
| GET | /api/tasks/{id}/ | Task detail |
| PUT/PATCH | /api/tasks/{id}/ | Update task |
| DELETE | /api/tasks/{id}/ | Delete task |

**Filters:**
- `?course=1` — filtrar por curso
- `?subject=Matemática` — filtrar por materia
- `?due_date_from=2026-01-01&due_date_to=2026-12-31` — rango de fechas
- `?search=título` — búsqueda en título/descripción
- `?ordering=due_date` — ordenar

**Permissions:** `directivo` full access; `profesor` solo courses asignados.

### Events
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/events/ | List events |
| POST | /api/events/ | Create event |
| GET | /api/events/{id}/ | Event detail |
| PUT/PATCH | /api/events/{id}/ | Update event |
| DELETE | /api/events/{id}/ | Delete event |

**Filters:**
- `?course=1` — filtrar por curso
- `?date_from=2026-01-01&date_to=2026-12-31` — rango de fechas
- `?search=título` — búsqueda en título/descripción
- `?ordering=date` — ordenar

### Grades
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/grades/ | List grades |
| POST | /api/grades/ | Create grade |
| GET | /api/grades/{id}/ | Grade detail |
| PUT/PATCH | /api/grades/{id}/ | Update grade |
| DELETE | /api/grades/{id}/ | Delete grade |

**Filters:**
- `?student=1` — filtrar por estudiante
- `?subject=Matemática` — filtrar por materia
- `?period=1er%20Trimestre` — filtrar por período
- `?ordering=student` — ordenar

**Validation:** Grade value must be between 0 and 10.

### Teacher Assignments
| Method | Endpoint |
|--------|----------|
| GET/POST | /api/assignments/ |
| GET/PUT/PATCH/DELETE | /api/assignments/{id}/ |

**Filters:**
- `?teacher=1` — filtrar por docente
- `?course=1` — filtrar por curso
- `?search=materia` — búsqueda por materia

**Permissions:** `directivo` full access; `profesor` read-only.

---

## Response Format

All list endpoints return paginated results:
```json
{
    "count": 42,
    "next": "http://.../?page=2",
    "previous": null,
    "results": [...]
}
```
