from fastapi import APIRouter,HTTPException
from app.schema.schema import TaskRequest, TaskResponse
from fastapi import BackgroundTasks
from app.controller.task import task_controller
import os
from dotenv import load_dotenv
load_dotenv()
task_router = APIRouter()


secrate=os.getenv("Secrate")
@task_router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskRequest, background_tasks: BackgroundTasks) -> TaskResponse:  # Add BackgroundTasks as dependency
    if task.signature == secrate:
        background_tasks.add_task(task_controller, task)  # Use the injected instance
        return TaskResponse(usercode=secrate) #type: ignore
    else:
        raise HTTPException(status_code=403, detail="Forbidden")