from app.util.github import github_main
from app.util.gen_ai import generate_project
from app.util.prompt_1 import prompt_1
from app.schema.schema import TaskRequest
import os
from dotenv import load_dotenv
import httpx

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables")
def task_1_controller(task: TaskRequest):
    prompt = task.brief
    files = generate_project(prompt_1(prompt))
    if not files:
        print("No files generated.")
        return
    commit_sha, pages_url, repo_url = github_main(GITHUB_TOKEN,"hdfbdzXffdbfh", files, private=False, description="Generated repo") #type: ignore
    if not repo_url:
        print("Failed to create GitHub repository.")
        return
    print(f"Repository created at: {repo_url}")
    try:
        response = httpx.post(
            task.evaluation_url,
            json={
                "email": task.email,
                "task": task.task,
                "round": task.round,
                "nonce": task.nonce,
                "repo_url": repo_url,
                "commit_sha": commit_sha,
                "pages_url": pages_url
            },
            timeout=10.0
        )
        response.raise_for_status()
        print(f"Successfully notified evaluation endpoint: {task.evaluation_url}")
    except httpx.HTTPError as e:
        print(f"Failed to notify evaluation endpoint: {e}")



def task_controller(task: TaskRequest):
    print(task)
    if task.round == 1:
        task_1_controller(task)
    else:
        print(f"Unknown task: {task.task}")
