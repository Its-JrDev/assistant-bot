# assistant-bot

Bot de Telegram escolar + panel web para gestión de tareas, eventos, horarios y notas.

## Stack

- **Backend**: Django 6 + DRF + SimpleJWT
- **Frontend**: SvelteKit + Shadcn-Svelte
- **DB**: PostgreSQL (prod) / SQLite (dev)
- **Bot**: pyTelegramBotAPI

## Desarrollo local

```bash
# 1. Clonar y preparar entorno
cp .env.example .env
# Editar .env con tus tokens (TELEGRAM_BOT_TOKEN, DJANGO_SECRET_KEY)

# 2. Backend
python -m venv .venv
source .venv/bin/activate
cd backend
pip install -r requirements.txt
python manage.py migrate --settings=config.settings.dev
python manage.py runserver --settings=config.settings.dev

# 3. Seed data (opcional)
cd ..
DJANGO_SETTINGS_MODULE=config.settings.dev python scripts/seed_sample_data.py

# 4. Bot (otra terminal)
source .venv/bin/activate
cd backend
TELEGRAM_BOT_TOKEN=tu-token python manage.py run_bot

# 5. Frontend (otra terminal)
cd frontend
npm install
npm run dev
```

### Usuarios seed

| Usuario | Contraseña | Rol |
|---|---|---|
| directivo | admin123 | Directivo |
| profesor1 | profesor123 | Profesor |
| Estudiante: DNI `12345678` / PIN `4321` | | |

## Producción

```bash
docker compose up -d
```

## Estructura

```
backend/         → Django API + bot
frontend/        → SvelteKit admin panel
scripts/         → Migración y seed data
docker/          → Dockerfiles + nginx
docs/            → Documentación
```

## Worktrees (F2 paralelo)

```bash
git worktree add ../assistant-bot-backend  feat/backend-api
git worktree add ../assistant-bot-frontend feat/frontend-svelte
git worktree add ../assistant-bot-bot      feat/bot-refactor
```

Ver `AGENTS.md` para instrucciones detalladas de cada worktree.
