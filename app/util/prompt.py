def prompt_1(prompt):
    return f"""
{prompt}

Return your response as JSON with this exact structure:
{{
  "files": [
    {{"name": "filename.ext", "content": "file content here"}},
    ...
  ]
}}

Include ALL necessary files (HTML, CSS, JS, etc.) also make the readme of the project and give it a description. Return ONLY valid JSON, no explanations.
"""

def prompt_2(prompt,repo_url):
    return f"""
I have created a repository for you. The URL is {repo_url}.
and i want you make the following changes to the project:
{prompt}
Return your response as JSON with this exact structure:
{{
  "files": [
    {{"name": "filename.ext", "content": "file content here"}},
    ...
  ]
}}
Repo URL: {repo_url}
"""