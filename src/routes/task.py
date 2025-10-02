from fastapi import APIRouter
from schema.schema import TaskRequest, TaskResponse
from fastapi import BackgroundTasks
import os
from dotenv import load_dotenv
load_dotenv()
router = APIRouter()


secrate=os.getenv("Secrate")

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskRequest):
    if task.signature == secrate:
        
        return TaskResponse(usercode=task.signature)