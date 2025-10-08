from fastapi import FastAPI
from app.routes.task import task_router



def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(
        task_router,
        prefix="/tasks"
    )
    return app

app = create_app()