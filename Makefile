.PHONY: backend frontend dev test install install-backend install-frontend docker-up docker-down clean migrate migrate-down

install: install-backend install-frontend

install-backend:
	cd backend && uv sync --all-extras --python 3.11

install-frontend:
	cd frontend && pnpm install

backend:
	cd backend && uv run --python 3.11 uvicorn app.main:app --reload

frontend:
	cd frontend && pnpm dev

dev:
	@echo "Запустите backend и frontend в разных терминалах:"
	@echo "  make backend"
	@echo "  make frontend"

test:
	cd backend && uv run --python 3.11 pytest
	cd frontend && pnpm test

build:
	cd frontend && pnpm build

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

migrate:
	cd backend && uv run --python 3.11 alembic revision --autogenerate -m "$(message)"

migrate-up:
	cd backend && uv run --python 3.11 alembic upgrade head

migrate-down:
	cd backend && uv run --python 3.11 alembic downgrade -1

clean:
	rm -rf backend/.venv backend/uv.lock backend/astro4.db \
		frontend/node_modules frontend/pnpm-lock.yaml frontend/dist
