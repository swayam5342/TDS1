from fastapi import FastAPI
from app.routes.task import task_router

__all__ = ["app"]

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(task_router)
    return app

app = create_app()