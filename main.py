from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List, Optional,Any
import os
from dotenv import load_dotenv
load_dotenv()

secrate = os.getenv("Secrate")
app = FastAPI()

# Pydantic model for parsing
class Attachment(BaseModel):
    name: str
    url: str

class TaskRequest(BaseModel):
    email: str
    task: str
    round: int
    nonce: str
    brief: str
    checks: List[str]
    evaluation_url: str
    attachments: Optional[List[Attachment]] = []
    signature: str

@app.post("/task")
async def receive_task(payload: TaskRequest) -> dict[str, Any]:
    if payload.signature == secrate:
        return {
            "email": payload.email,
            "task": payload.task,
            "round": payload.round,
            "nonce": payload.nonce,
            "brief": payload.brief,
            "checks": payload.checks,
            "evaluation_url": payload.evaluation_url,
            "attachments": payload.attachments,
            "signature": payload.signature
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid Secrate")
