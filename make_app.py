from github_repo import github_main
from gen_gemini import generate_project
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables")
if __name__ == "__main__":
    prompts = [
        "Build a calculator",
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"\n{'='*60}")
        print(f"Generating project {i+1}: {prompt[:50]}...")
        print('='*60)
        files = generate_project(prompt)
        commit_sha, pages_url, repo_url = github_main(
            token=GITHUB_TOKEN,
            repo_name=f"generated-repo-{i+1}",
            files=files,
            des="A test repository created with Python",
            enable_pages=True
        )
        print(f"\nCommit SHA: {commit_sha}")
        print(f"Repository URL: {repo_url}")
        if pages_url:
            print(f"GitHub Pages URL: {pages_url}")
    