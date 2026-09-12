from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import engine
from app.migrations import run_migrations
from app.routers import auth, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run database migrations on startup
    run_migrations()
    yield
    await engine.dispose()


app = FastAPI(title="Astro4 + FastAPI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
