from fastapi import FastAPI
from app.routes.task import task_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(task_router)
    
    @app.get("/")
    def read_root():
        return {"message": "Task Router is working"}

    @app.get("/health", tags=["Monitoring"])
    async def health_check():
        """Simple health check endpoint."""
        return {"status": "ok", "service": "Task Router"}
    return app