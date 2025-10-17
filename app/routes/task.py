from fastapi import APIRouter,HTTPException
from app.schema.schema import TaskRequest, TaskResponse
from fastapi import BackgroundTasks
from app.controller.task import task_controller
import os
from dotenv import load_dotenv
load_dotenv()
task_router = APIRouter()


secret = os.getenv("s")
@task_router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskRequest, background_tasks: BackgroundTasks) -> TaskResponse:
    if task.secret == secret:
        background_tasks.add_task(task_controller, task)
        return TaskResponse(usercode=secret) #type: ignore
    else:
        print(secret,task.secret)
        raise HTTPException(status_code=403, detail="Forbidden")