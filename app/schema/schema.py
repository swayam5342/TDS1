from pydantic import BaseModel
from typing import Optional,List


class Data(BaseModel):
    name: str
    url: str

class TaskResponse(BaseModel):
    usercode: str

class TaskRequest(BaseModel):
    email: str
    secret: str
    task: str
    round: int
    nonce: str
    brief: str
    checks: List[str]
    evaluation_url: str
    attachments: Optional[List[Data]] = []


class EvaluationRequest(BaseModel):
    email: str
    task: str
    round: int
    nonce: str
    repo_url: str
    commit_sha: str
    pages_url: str

