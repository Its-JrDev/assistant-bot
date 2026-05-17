# assistant-bot — fix/docker-frontend-admin

## Objetivo

Arreglar Docker compose para que admin de Django y frontend funcionen correctamente.

## Problemas

### 1. Admin de Django en `:8000/admin/` — sin CSS/JS
`DEBUG=False`, gunicorn no sirve estáticos. Falta whitenoise.

### 2. CORS roto en producción
`base.py` solo permite `localhost:5173` y `:4173`. `prod.py` usa env var que no está seteada → `CORS_ALLOWED_ORIGINS = []`. Frontend en `localhost:80` hace requests a `http://localhost:8000/api` y CORS las bloquea.

### 3. VITE_API_URL no seteado en build Docker
Frontend usa `VITE_API_URL ?? 'http://localhost:8000/api'` → requests cross-origin en vez de usar `/api` por nginx proxy.

## Qué tocar

| Archivo | Cambio |
|---|---|
| `backend/config/settings/base.py` | Agregar `whitenoise` a INSTALLED_APPS y MIDDLEWARE. Agregar `http://localhost` a CORS_ALLOWED_ORIGINS |
| `backend/config/settings/prod.py` | `CORS_ALLOWED_ORIGINS` obtener del env o default `['http://localhost']` |
| `backend/requirements.txt` | Agregar `whitenoise` |
| `docker-compose.yml` | Agregar `CORS_ALLOWED_ORIGINS` y `VITE_API_URL=/api` |

## Convenciones

- Edit ordenado, sin comentarios
- Probar con `docker compose up --build`

## Cómo probar

```bash
docker compose up --build -d
# Probar:
# - http://localhost/admin/  (admin con CSS via nginx)
# - http://localhost/        (frontend login, login funciona)
# - http://localhost/api/token/  (POST con credenciales)
```
