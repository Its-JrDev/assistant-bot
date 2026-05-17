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
| GET | /api/users/ | List users (admin only) |
| POST | /api/users/ | Create user |
| GET | /api/users/{id}/ | User detail |
| PUT/PATCH | /api/users/{id}/ | Update user |
| DELETE | /api/users/{id}/ | Delete user |

### Students
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/students/ | List students |
| POST | /api/students/ | Create student |
| GET | /api/students/{id}/ | Student detail |
| PUT/PATCH | /api/students/{id}/ | Update student |
| DELETE | /api/students/{id}/ | Delete student |

Search: `GET /api/students/?search=nombre_o_dni`

### Courses
| Method | Endpoint |
|--------|----------|
| GET/POST | /api/courses/ |
| GET/PUT/PATCH/DELETE | /api/courses/{id}/ |

### Schedules
| Method | Endpoint |
|--------|----------|
| GET/POST | /api/schedules/ |
| GET/PUT/PATCH/DELETE | /api/schedules/{id}/ |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/tasks/ | List tasks |
| POST | /api/tasks/ | Create task |
| GET | /api/tasks/{id}/ | Task detail |
| PUT/PATCH | /api/tasks/{id}/ | Update task |
| DELETE | /api/tasks/{id}/ | Delete task |

**Filter by course:** `GET /api/tasks/?course=1`

### Events
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/events/ | List events |
| POST | /api/events/ | Create event |
| GET | /api/events/{id}/ | Event detail |
| PUT/PATCH | /api/events/{id}/ | Update event |
| DELETE | /api/events/{id}/ | Delete event |

### Grades
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/grades/ | List grades |
| POST | /api/grades/ | Create grade |
| GET | /api/grades/{id}/ | Grade detail |
| PUT/PATCH | /api/grades/{id}/ | Update grade |
| DELETE | /api/grades/{id}/ | Delete grade |

**Filter by student:** `GET /api/grades/?student=1`

### Teacher Assignments
| Method | Endpoint |
|--------|----------|
| GET/POST | /api/assignments/ |
| GET/PUT/PATCH/DELETE | /api/assignments/{id}/ |

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
