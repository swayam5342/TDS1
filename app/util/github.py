from github import GithubException, InputGitTreeElement
import base64
import requests

def upload_files(repo, files_dict):
    try:
        if repo is None:
            raise ValueError("Repository object is None")
        default_branch = repo.default_branch
        ref = repo.get_git_ref(f"heads/{default_branch}")
        base_commit = repo.get_git_commit(ref.object.sha)
        base_tree = base_commit.tree
        tree_elements = []
        for file_path, content in files_dict.items():
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
        tree = repo.create_git_tree(tree_elements, base_tree)
        commit = repo.create_git_commit(
            message="Initial commit with files",
            tree=tree,
            parents=[base_commit]
        )
        ref.edit(sha=commit.sha)
        return commit.sha
    except GithubException as e:
        raise
    except Exception as e:
        raise


def create_repo(user, repo_name, description=""):
    try:
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=False,
            auto_init=True,
            license_template="mit"
        )
        return repo
    except GithubException as e:
        raise
    except Exception as e:
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
            return f"https://{user.login}.github.io/{repo.name}/"
        else:
            raise
    except Exception as e:
        raise e



def list_repo_files(repo):
    """List all files in repository with their paths."""
    try:
        contents = repo.get_contents("")
        files = []
        
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                files.append(file_content.path)
        
        return files
    except Exception as e:
        return []

if __name__ == "__main__":
    ...