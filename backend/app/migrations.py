import subprocess

from app.core.config import settings


def run_migrations() -> None:
    """Run Alembic migrations."""
    subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=".",
        check=True,
        env={**__import__("os").environ, "DATABASE_URL": settings.DATABASE_URL},
    )
