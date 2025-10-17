from typing import List
from app.util.attch import process_attachments
from app.util.github import create_repo, upload_files, enable_github_pages, list_repo_files
from app.util.gen_ai import generate_project, generate_prompt
from app.util.prompt import prompt_1, prompt_2
from app.schema.schema import Data, TaskRequest
from github import Auth,Github
import os
from dotenv import load_dotenv
import httpx
import time


load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables")


auth = Auth.Token(GITHUB_TOKEN)
gh = Github(auth=auth)  #type: ignore
user = gh.get_user()

def task_controller(task: TaskRequest):
    if task.round == 1:
        task_1_controller(task)
    elif task.round ==2:
        task_2_controller(task)
    else:
        ...





def task_1_controller(task: TaskRequest, max_retries: int = 3):
    for attempt in range(max_retries):        
        brief = task.brief
        check = task.checks
        processed_attachments = None
        if task.attachments:
            att: List[Data] | None = task.attachments
            processed_attachments = process_attachments(att) #type: ignore
        final_prompt = prompt_1(brief, check,attached_files=processed_attachments) #type: ignore
        prompt = generate_prompt(final_prompt)
        if task.attachments:
            prompt += f"""
            The attached files content samples are:
            {processed_attachments}
            """
        files = generate_project(prompt)
        files["round_1.txt"] = f"prior prompt  {prompt}\n task brief : {brief}\n task checks : {check}\n" #type: ignore
        if not files:
            if attempt < max_retries - 1:
                delay = 2 ** attempt
                time.sleep(delay)
                continue
            else:
                return
        
        repo = None
        commit_sha = None
        pages_url = None
        
        try:
            repo_name = "".join(task.task.split()).lower()
            repo = create_repo(user,repo_name, "Generated repo")
            commit_sha = upload_files(repo, files)
            pages_url = enable_github_pages(repo, GITHUB_TOKEN, user)
        except Exception as e:
            if attempt < max_retries - 1:
                delay = 2 ** attempt
                time.sleep(delay)
                continue
            else:
                return
        time.sleep(5)
        break

    for _ in range(3):
        page = httpx.get(pages_url)
        if page.status_code == 200:
            break
        time.sleep(10)
    else:
        pages_url = enable_github_pages(repo, GITHUB_TOKEN, user)
    submission_successful = False
    for submit_attempt in range(max_retries):
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
            
            if response.status_code == 200:
                submission_successful = True
                break  # Success! Exit submission loop
            else:
                raise httpx.HTTPStatusError(
                    f"Expected 200, got {response.status_code}",
                    request=response.request,
                    response=response
                )
                
        except httpx.HTTPError as e:
            if submit_attempt < max_retries - 1:
                delay = 2 ** submit_attempt
                time.sleep(delay)
        if submission_successful:
            return
        if attempt < max_retries - 1:
            delay = 2 ** attempt
            time.sleep(delay)
        break



def task_2_controller(task: TaskRequest, max_retries: int = 3):
    for attempt in range(max_retries):
        brief = task.brief
        processed_attachments = None
        if task.attachments:
            att: List[Data] | None = task.attachments
            processed_attachments = process_attachments(att) #type: ignore
        check = task.checks
        repo_name = "".join(task.task.split()).lower()
        repo = user.get_repo(repo_name)
        file_contents = repo.get_contents("round_1.txt")
        file_data = file_contents.decoded_content.decode('utf-8') #type: ignore
        existing_files = list_repo_files(repo)
        final_prompt = prompt_2(brief, check, attached_files=processed_attachments) #type: ignore
        final_prompt += f"""
                The existing files in the repository are:
                {existing_files}
                and the prior round prompt and information that you gave is:
                {file_data}
                """
        prompt = generate_prompt(final_prompt)
        prompt += f"""
                The existing files in the repository are:
                {existing_files}
                Make necessary modifications to these files to meet the task requirements.
                """
        if processed_attachments:
            prompt += f"""
            The attached files content samples are:
            {processed_attachments}
            """
        files = generate_project(prompt)
        if not files:
            if attempt < max_retries - 1:
                delay = 2 ** attempt
                time.sleep(delay)
                continue
            else:
                return
        commit_sha = None
        pages_url = None
        try:
            commit_sha = upload_files(repo, files)
        except Exception as e:
            if attempt < max_retries - 1:
                delay = 2 ** attempt
                time.sleep(delay)
                continue
            else:
                return
        time.sleep(10)
        break
    for _ in range(3):
        pages_url = f"https://{user.login}.github.io/{repo.name}/" #type: ignore
        page = httpx.get(pages_url)
        if page.status_code == 200:
            break
        time.sleep(10)
    else:
        pages_url = enable_github_pages(repo, GITHUB_TOKEN, user)
    submission_successful = False
    for submit_attempt in range(max_retries):
        try:
            response = httpx.post(
                task.evaluation_url,
                json={
                    "email": task.email,
                    "task": task.task,
                    "round": task.round,
                    "nonce": task.nonce,
                    "repo_url": repo.html_url, #type: ignore
                    "commit_sha": commit_sha,
                    "pages_url": pages_url
                },
                timeout=10.0
            )
            response.raise_for_status()
            
            if response.status_code == 200:
                submission_successful = True
                break
            else:
                raise httpx.HTTPStatusError(
                    f"Expected 200, got {response.status_code}",
                    request=response.request,
                    response=response
                )
                
        except httpx.HTTPError as e:
            if submit_attempt < max_retries - 1:
                delay = 2 ** submit_attempt
                time.sleep(delay)
        if submission_successful:
            return
        if attempt < max_retries - 1:
            delay = 2 ** attempt
            time.sleep(delay)
        break
