FROM node:22-alpine AS build

WORKDIR /app

ENV CI=true

RUN corepack enable && corepack prepare pnpm@latest --activate

COPY frontend/pnpm-lock.yaml frontend/package.json ./
RUN pnpm install --frozen-lockfile

COPY frontend/ .
RUN pnpm build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
