from pydantic import BaseModel
from typing import Optional,List


class Attachment(BaseModel):
    name: str
    url: str

class TaskResponse(BaseModel):
    usercode: str

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


class EvaluationRequest(BaseModel):
    email: str
    task: str
    round: int
    nonce: str
    repo_url: str
    commit_sha: str
    pages_url: str

