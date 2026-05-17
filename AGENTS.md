# assistant-bot — AGENTS

## Contexto General

Bot de Telegram escolar + panel web para gestión de tareas, eventos, horarios y notas.

- **Backend**: Django 6 + DRF + SimpleJWT (Python 3.12)
- **Frontend**: SvelteKit + Shadcn-Svelte (Tailwind)
- **DB**: SQLite (dev) / PostgreSQL (prod)
- **Bot**: pyTelegramBotAPI (Django management command)
- **Auth**: JWT + roles (directivo / profesor)
- **Seed users**: directivo/admin123, profesor1/profesor123, Student DNI 12345678/PIN 4321

### Estructura

```
backend/
├── manage.py
├── requirements.txt
├── config/settings/{base,dev,prod}.py
├── config/urls.py           ← rutas API
└── apps/
    ├── accounts/            ← CustomUser (role: directivo|profesor)
    ├── students/            ← Student (dni, pin_hash, telegram_id)
    ├── academics/           ← Course, Schedule, Task, Event, Grade, TeacherAssignment
    └── telegram_bot/        ← management command + handlers
frontend/                    ← SvelteKit (estructura vacía)
scripts/                     ← seed, migración SQLite
docs/api.md                  ← contratos API
```

### Comandos base

```bash
source .venv/bin/activate
cd backend
python manage.py check --settings=config.settings.dev   # lint
python manage.py migrate --settings=config.settings.dev  # migrar
python manage.py runserver --settings=config.settings.dev  # dev server
python manage.py test --settings=config.settings.dev       # tests
DJANGO_SETTINGS_MODULE=config.settings.dev python ../scripts/seed_sample_data.py  # seed
```

### Contratos

- `docs/api.md` — endpoints DRF con shapes de respuesta
- Tag `v0.1-contracts` — modelos, serializers, permisos ya creados
- URL base: `http://localhost:8000/api/`
- Auth: `Authorization: Bearer <jwt_access_token>`

---

## feat/backend-api — Backend API

### Objetivo

Refinar endpoints DRF existentes: filtros, búsqueda, permisos granulares, tests, y endpoints adicionales que necesite el frontend.

### Qué tocar

| Archivo | Qué hacer |
|---|---|
| `apps/academics/views.py` | Agregar filtros por curso, materia, fecha. Optimizar querysets con select_related/prefetch_related |
| `apps/academics/permissions.py` | Refinar permisos: profesor solo puede editar lo de sus TeacherAssignment |
| `apps/academics/serializers.py` | Agregar validación, campos calculados si hacen falta |
| `apps/students/views.py` | Filtro por curso, search |
| `apps/accounts/views.py` | Solo directivo puede crear/editar usuarios |
| `config/urls.py` | No tocar a menos que se agreguen endpoints nuevos |
| `apps/*/tests.py` | Tests para cada endpoint (mínimo: list, create, permiso denegado) |
| `docs/api.md` | Mantener actualizado |

### Convenciones

-命名 querysets con `select_related('course', 'created_by')` donde corresponda
- Usar `@extend_schema` de drf-spectacular si se agrega documentación
- Tests con `APITestCase` y `force_authenticate`
- No agregar dependencias nuevas sin justificación

### Cómo probar

```bash
cd backend
python manage.py test --settings=config.settings.dev
python manage.py runserver --settings=config.settings.dev
# Probar con curl o httpie:
# http POST http://localhost:8000/api/token/ username=directivo password=admin123
```

---

## feat/frontend-svelte — Admin Panel UI

### Objetivo

Crear el panel web de administración escolar con SvelteKit + Shadcn-Svelte. Login JWT y CRUD de todas las entidades.

### Setup inicial

```bash
cd frontend
npm create svelte@latest . -- --template minimal
npx svelte-add@latest tailwindcss
npm install bits-ui lucide-svelte
npx shadcn-svelte@latest init
npx shadcn-svelte@latest add button card input table dialog select
```

### Qué crear

| Ruta | Descripción |
|---|---|
| `src/routes/+layout.svelte` | Layout con sidebar nav + header |
| `src/routes/+page.svelte` | Login page |
| `src/routes/dashboard/+page.svelte` | Dashboard con cards (eventos próximos, tareas x curso) |
| `src/routes/events/+page.svelte` | CRUD eventos (table + modal create/edit) |
| `src/routes/tasks/+page.svelte` | CRUD tareas |
| `src/routes/schedules/+page.svelte` | CRUD horarios (por curso/día) |
| `src/routes/grades/+page.svelte` | CRUD notas (tabla estudiante × materia) |
| `src/lib/api/client.ts` | Cliente HTTP con fetch wrapper + JWT |
| `src/lib/components/ui/` | Componentes Shadcn-Svelte (generados) |

### Contrato API

Ver `docs/api.md`. Endpoints base:

```
POST  /api/token/         → {access, refresh}
GET   /api/events/        → {count, results: [{id, title, date, course_name, ...}]}
POST  /api/events/        → {id, title, date, ...}
GET   /api/tasks/         → similar
POST  /api/tasks/         → {course, subject, title, description, due_date}
... (mismo patrón para schedules, grades, students, courses)
```

### Convenciones

- Shadcn-Svelte para componentes de UI (no crear desde cero)
- Tailwind utility classes para estilos
- Fetch directo con `fetch()` (sin axios) o TanStack Query
- Auth store con Svelte writable + localStorage
- Formularios con `superforms` + Zod para validación
- idioma: español (AR), formato fecha DD/MM/YYYY

### Cómo correr

```bash
cd frontend
npm install
npm run dev  # http://localhost:5173
```

Backend debe estar corriendo en `http://localhost:8000` (o configurar VITE_API_URL).

---

## feat/bot-refactor — Telegram Bot v2

### Objetivo

Migrar los handlers del bot de SQLite crudo (`database.db`) a Django ORM. Implementar comandos faltantes (`/tareas`, `/eventos`, `/notas`) y conectar IA real con OpenRouter.

### Estado actual

Los handlers usan `database.db` (SQLite directa) y `config.py`. Hay que migrar a usar `Student.objects.get(telegram_id=...)` y demás modelos Django.

### Archivos a migrar

| Actual (legacy) | Nuevo (Django ORM) |
|---|---|
| `telegram_bot/services/session_service.py` | `Student.objects.filter(telegram_id=tid).first()` |
| `telegram_bot/handlers/schedules.py` | `Schedule.objects.filter(course=student.course).order_by(...)` |
| `telegram_bot/handlers/tasks.py` | `Task.objects.filter(course=student.course)` |
| `telegram_bot/handlers/events.py` | `Event.objects.filter(course=student.course)` |
| `telegram_bot/handlers/ai.py` | Llamada real a OpenRouter API con `openai` SDK |
| `telegram_bot/handlers/login.py` | `Student.objects.get(dni=dni)` + `check_password(pin, student.pin_hash)` |
| `telegram_bot/handlers/logout.py` | Update `telegram_id=None` en Student |

### Comandos a implementar

- `/start` — ✅ ya existe
- `/login` — migrar a Django ORM + PIN hasheado
- `/logout` — migrar a Django ORM
- `/horario` — migrar a Django ORM
- `/tareas` — **nuevo**: lista tareas del curso del estudiante (ordenado por fecha)
- `/eventos` — **nuevo**: lista eventos próximos del curso
- `/notas` — **nuevo**: lista notas del estudiante (por período)

### Comportamiento IA

El handler `ai.py` debe implementar llamada real a OpenRouter:

```python
from openai import OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)
```

Pero limitado a responder SOLO sobre datos escolares (horario, tareas, eventos, notas). No exponer datos sensibles del estudiante al modelo. En v1, usarlo solo como ayuda conversacional acotada, NO para responder consultas libres.

### Convenciones

- Los handlers NO acceden a `database.db` ni SQLite directo
- Todo via Django ORM: `from students.models import Student`, `from academics.models import ...`
- PIN validation usa `django.contrib.auth.hashers.check_password`
- No tocar `run_bot.py` a menos que sea para agregar comandos nuevos
- Mensajes de respuesta en español, con emojis

### Cómo probar

```bash
source .venv/bin/activate
cd backend
python manage.py migrate --settings=config.settings.dev
DJANGO_SETTINGS_MODULE=config.settings.dev python ../scripts/seed_sample_data.py
TELEGRAM_BOT_TOKEN=tu-token python manage.py run_bot
```

Para tests unitarios de handlers (sin Telegram real):

```bash
python manage.py test apps/telegram_bot --settings=config.settings.dev
```
