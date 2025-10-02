from util.github import github_main
from util.gen_ai import generate_project
import os
from dotenv import load_dotenv
import httpx

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables")

def task_controller(prompt, repo_name):
    files = generate_project(prompt)
    if not files:
        return None, None, None
    commit_sha, pages_url, repo_url = github_main(
        token=GITHUB_TOKEN,
        repo_name=repo_name,
        files=files,
        des="A repository created with Python",
        enable_pages=True
    )
    return commit_sha, pages_url, repo_url