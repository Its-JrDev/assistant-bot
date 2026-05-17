# assistant-bot v2 — Plan de Reestructuración

## Stack

| Capa | Tecnología |
|---|---|
| Backend API | Django 5 + DRF + SimpleJWT |
| Base de datos | PostgreSQL 16 (prod), SQLite (dev) |
| Frontend | SvelteKit + Shadcn-Svelte (Tailwind) |
| Auth | JWT + roles (directivo / profesor) |
| Bot Telegram | pyTelegramBotAPI (Django management command) |

## Estructura del Repo

```
assistant-bot/
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── nginx.conf
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── dev.py
│   │   │   └── prod.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── apps/
│       ├── accounts/           # CustomUser, roles
│       ├── students/           # Student, PIN hash, telegram_id
│       ├── academics/          # Course, Schedule, Task, Event, Grade, TeacherAssignment
│       └── telegram_bot/       # management command + handlers
├── frontend/
│   ├── package.json
│   ├── svelte.config.js
│   ├── tailwind.config.ts
│   └── src/
│       ├── routes/{login,dashboard,events,tasks,schedules,grades}
│       └── lib/{components/ui,api}
├── scripts/
│   ├── cleanup_git_history.sh
│   ├── migrate_sqlite_to_django.py
│   └── seed_sample_data.py
└── docs/
    ├── architecture.md
    ├── api.md
    └── deployment.md
```

## Modelo de Datos

- **accounts.CustomUser**: email, role (directivo|profesor), password, full_name
- **students.Student**: dni, pin_hash, nombre, course FK, telegram_id (unique)
- **academics.Course**: name (1A, 2B...), academic_year
- **academics.TeacherAssignment**: teacher FK→User, course FK, subject
- **academics.Schedule**: course FK, day, start_time, end_time, subject, teacher FK→User
- **academics.Task**: course FK, subject, title, description, due_date, created_by FK
- **academics.Event**: course FK, title, date, description, created_by FK
- **academics.Grade**: student FK, subject, grade (decimal), period, created_by FK

## Roles y Permisos

| Rol | Alcance |
|---|---|
| **directivo** | CRUD completo en todas las entidades |
| **profesor** | CRUD en tareas/eventos/notas de sus cursos (via TeacherAssignment). Read-only en schedules/students |

## Fases

### F0 — Incident Response + Fundación (secuencial)

| # | Acción |
|---|---|
| F0.0 | Revocar tokens (Telegram + OpenRouter) |
| F0.1 | git rm --cached secrets, .gitignore, crear develop |
| F0.2 | Fix requirements.txt UTF-16 → UTF-8 |
| F0.3 | Crear estructura de directorios |
| F0.4 | .env.example + settings base/dev/prod |
| F0.5 | Django skeleton (startproject + startapp) |
| F0.6 | Migrar bot a telegram_bot app |
| F0.7 | Migration script SQLite → Django ORM |
| F0.8 | Merge chore/foundation → develop |

### F1 — Contratos (secuencial, sobre develop)

| # | Acción |
|---|---|
| F1.0 | Modelos Django + migraciones |
| F1.1 | DRF Serializers + ViewSets |
| F1.2 | Roles y permisos |
| F1.3 | docs/api.md con endpoints |
| F1.4 | Tag v0.1-contracts |

### F2 — Paralelo (worktrees)

| Worktree | Branch | Contenido |
|---|---|---|
| assistant-bot-backend | feat/backend-api | ViewSets, permisos, tests, seed |
| assistant-bot-frontend | feat/frontend-svelte | SvelteKit + Shadcn + CRUD pages |
| assistant-bot-bot | feat/bot-refactor | Handlers Django ORM, /tareas, /eventos, /notas, IA |

### F3 — Integración + Deploy

- Merge features → develop → test end-to-end
- Docker compose full stack
- Deploy local → Vercel (frontend) → VPS (backend+bot+DB)
- Merge develop → main con tag release

## Branch Strategy

```
main (prod) ← merge solo desde develop, tags v*
  └── develop (integración)
       ├── chore/foundation
       ├── feat/contracts
       ├── feat/backend-api
       ├── feat/frontend-svelte
       ├── feat/bot-refactor
       └── chore/deploy-*
```

## Worktree Setup

```bash
git worktree add ../assistant-bot-backend  feat/backend-api
git worktree add ../assistant-bot-frontend feat/frontend-svelte
git worktree add ../assistant-bot-bot      feat/bot-refactor
```
