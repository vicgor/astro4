# Astro 4 + FastAPI Starter

Готовый шаблон веб-сайта с фронтендом на **Astro 4** и бэкендом на **FastAPI**.

Менеджеры зависимостей:
- Backend: [uv](https://docs.astral.sh/uv/)
- Frontend: [pnpm](https://pnpm.io/)

Миграции базы данных: [Alembic](https://alembic.sqlalchemy.org/)

## Структура

```
astro4/
├── backend/      # FastAPI приложение
│   ├── alembic/  # миграции БД
│   └── app/
├── frontend/     # Astro 4 приложение
├── docker-compose.yml
├── Makefile
└── README.md
```

## Требования

- Python 3.11+
- Node.js 20+
- pnpm 9.x (`corepack enable` или `npm install -g pnpm@9.15.0`)
- uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Быстрый старт

### 1. Клонирование и установка

```bash
cd ~/projects/astro4
make install
```

### 2. Настройка окружения backend

```bash
cp backend/.env.example backend/.env
```

### 3. Применение миграций

```bash
cd backend
uv run --python 3.11 alembic upgrade head
```

Или через Makefile:

```bash
make migrate-up
```

### 4. Локальная разработка

Запустите в разных терминалах:

```bash
# Терминал 1 — backend
make backend

# Терминал 2 — frontend
make frontend
```

Откройте http://localhost:4320

API документация: http://localhost:8000/docs

### Docker

```bash
docker-compose up --build
```

Frontend: http://localhost  
Backend API: http://localhost:8000  
API Docs: http://localhost:8000/docs

## Команды

### Общие

```bash
make install          # установить все зависимости
make backend          # запустить FastAPI в dev-режиме
make frontend         # запустить Astro в dev-режиме
make test             # запустить тесты
make build            # собрать frontend
make docker-up        # поднять весь стек в Docker
make clean            # удалить зависимости и артефакты
```

### Миграции

```bash
# Создать новую миграцию по изменениям моделей
make migrate message="add posts table"

# Применить все миграции
make migrate-up

# Откатить последнюю миграцию
make migrate-down
```

## CI/CD

Проект включает GitHub Actions для автоматизации:

### CI — `.github/workflows/ci.yml`

Запускается при push и pull request в `main`:

- Линтер backend (`ruff`)
- Тесты backend (`pytest`)
- Сборка frontend (`pnpm build`)

### Deploy — `.github/workflows/deploy.yml`

Запускается при push в `main` и деплоит проект на сервер через SSH.

### Настройка secrets

В настройках репозитория GitHub добавьте secrets:

| Secret | Описание |
|---|---|
| `SSH_HOST` | IP или домен сервера |
| `SSH_USER` | Имя пользователя на сервере |
| `SSH_KEY` | Приватный SSH-ключ |
| `SSH_PORT` | Порт SSH (по умолчанию 22) |
| `DEPLOY_PATH` | Путь к проекту на сервере, например `/var/www/astro4` |

### Требования к серверу

- Установлен Git, Docker и docker-compose
- Настроен SSH-доступ по ключу
- Проект склонирован в `DEPLOY_PATH`

## Возможности

- FastAPI с асинхронным SQLAlchemy 2.0
- Alembic для миграций базы данных
- JWT-авторизация (регистрация и вход)
- Astro 4 со статическим рендерингом
- React-острова для интерактивных форм
- Tailwind CSS для стилей
- Docker и docker-compose для деплоя
- GitHub Actions CI/CD
- Тесты backend на pytest

## Дальнейшие шаги

- Подключите PostgreSQL в production
- Добавьте админ-панель
- Добавьте загрузку файлов
- Настройте мониторинг и логирование
