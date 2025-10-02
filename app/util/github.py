from github import Github, GithubException, Auth, InputGitTreeElement
import base64
import requests
import time
def create_repo_with_files(user, repo_name, files_dict, private=False, description=""):
    try:
        print(f"Creating repository: {repo_name}")
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=False,
            auto_init=True,
            license_template="mit"
        )
        print(f"Repository created: {repo.html_url}")
        time.sleep(2)
        
        default_branch = repo.default_branch
        ref = repo.get_git_ref(f"heads/{default_branch}")
        base_commit = repo.get_git_commit(ref.object.sha)
        base_tree = base_commit.tree
        
        tree_elements = []
        for file_path, content in files_dict.items():
            print(f"Creating blob for: {file_path}")
            if isinstance(content, str):
                blob = repo.create_git_blob(content, "utf-8")
            else:
                encoded_content = base64.b64encode(content).decode('utf-8')
                blob = repo.create_git_blob(encoded_content, "base64")
            
            element = InputGitTreeElement(
                path=file_path,
                mode="100644",
                type="blob",
                sha=blob.sha
            )
            tree_elements.append(element)
        
        print("Creating tree...")
        tree = repo.create_git_tree(tree_elements, base_tree)
        
        print("Creating commit...")
        commit = repo.create_git_commit(
            message="Initial commit with files",
            tree=tree,
            parents=[base_commit]
        )
        
        print("Updating branch reference...")
        ref.edit(sha=commit.sha)
        
        print(f"\n✓ Success!")
        print(f"Repository URL: {repo.html_url}")
        print(f"Commit SHA: {commit.sha}")
        
        return commit.sha, repo
        
    except GithubException as e:
        print(f"Error: {e.status} - {e.data}")
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        raise


def enable_github_pages(repo, token, user):
    url = f"https://api.github.com/repos/{user.login}/{repo.name}/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "source": {"branch": "main", "path": "/"}
    }
    
    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        response_data = r.json()
        html_url = response_data.get("html_url", "")        
        return html_url
        
    except requests.exceptions.HTTPError as e:
        if r.status_code == 409: #type: ignore
            print("GitHub Pages is already enabled for this repository")
            return f"https://{user.login}.github.io/{repo.name}/"
        else:
            print(f"Error enabling GitHub Pages: {e}")
            print(f"Response: {r.text}") #type: ignore
            raise
    except Exception as e:
        print(f"Error: {str(e)}")
        raise


def github_main(token, repo_name, files, des, enable_pages=True):
    auth = Auth.Token(token)
    g = Github(auth=auth)
    user = g.get_user()
    
    commit_sha, repo = create_repo_with_files(
        user=user,
        repo_name=repo_name,
        files_dict=files,
        private=False,
        description=des
    )
    
    pages_url = ""
    if enable_pages:
        pages_url = enable_github_pages(repo, token, user)
    return commit_sha, pages_url, repo.html_url


if __name__ == "__main__":
    ...