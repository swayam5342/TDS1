from app.util.github import create_repo, upload_files, enable_github_pages
from app.util.gen_ai import generate_project
from app.util.prompt import prompt_1
from app.schema.schema import TaskRequest
from github import Auth,Github
import os
from dotenv import load_dotenv
import httpx

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables")


auth = Auth.Token(GITHUB_TOKEN)
gh = Github(auth=auth)  #type: ignore
user = gh.get_user()
def task_1_controller(task: TaskRequest):
    prompt = task.brief
    files = generate_project(prompt_1(prompt))
    print(f"Generated {len(files)} files for task: {task.task}")
    if not files:
        print("No files generated.")
        return
    try:
        repo = create_repo(user, task.task, "Generated repo")
        commit_sha = upload_files(repo, files)
        pages_url = enable_github_pages(repo, GITHUB_TOKEN, user)
        print(f"GitHub Pages URL: {pages_url}")
    except Exception as e:
        print(f"GitHub operation failed: {e}")
        return
    try:
        response = httpx.post( 
            task.evaluation_url,
            json={
                "email": task.email,
                "task": task.task,
                "round": task.round,
                "nonce": task.nonce,
                "repo_url": repo.html_url,
                "commit_sha": commit_sha,
                "pages_url": pages_url
            },
            timeout=10.0
        )
        response.raise_for_status()
        print(f"Successfully notified evaluation endpoint: {task.evaluation_url}")
    except httpx.HTTPError as e:
        print(f"Failed to notify evaluation endpoint: {e}")

def task_2_controller(task: TaskRequest):
    print(task.round)
    ...

def task_controller(task: TaskRequest):
    print(task)
    if task.round == 1:
        task_1_controller(task)
    elif task.round ==2:
        task_2_controller(task)
    else:
        print(f"Unknown task: {task.task}")
