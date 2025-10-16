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

def prompt_3(prompt,check):
    return f"""
你是一个人工智能的提示生成器，用于构建可在 GitHub Pages 上部署的小型静态 Web 应用程序。
你的任务是阅读用户提供的应用程序简介，并创建一个最终的、结构良好的提示，指示代码人工智能在严格的约束条件下生成应用程序
this is app brief: {prompt}
您的任务

将上述简介总结并组织成代码生成 AI 的构建提示。

请执行以下约束：

仅限纯前端（HTML、CSS、JS 和静态资源）。

必须直接在 GitHub Pages 上运行（无后端、构建工具或服务器）。

尽量减少依赖关系，并使用内联注释以保持清晰。

通过正确引用所有附加资源（图片、CSS 文件、JSON 配置），以支持它们。

如果用户简介中缺少功能和布局说明，请添加这些说明。

确保生成的提示以以下强制输出格式指令结尾

确保它完全满足这些检查，因为人工智能只能生成代码，所以相应地措辞
{check}
"""


def prompt_3_ai(prompt, check):
    return f"""
你是一个人工智能提示生成器，用于构建可在 GitHub Pages 上部署的小型静态 Web 应用。
阅读以下应用简介，并生成一个清晰、完整的提示，指导代码生成 AI 在严格约束下创建该应用。

应用简介:
{prompt}

任务要求:
1. 仅限纯前端（HTML、CSS、JS 和静态资源）。
2. 必须能直接在 GitHub Pages 上运行（无后端、构建工具或服务器）。
3. 尽量减少依赖，代码中添加简短注释。
4. 正确引用所有附加资源（图片、CSS、JSON等）。
5. 如简介中缺少功能或布局说明，请合理补全。
6. 确保符合以下检查要求:
{check}

最后必须在生成的提示结尾添加以下输出格式说明:
Return your response as JSON with this exact structure:
{{
  "files": [
    {{"name": "filename.ext", "content": "file content here"}},
    ...
  ]
}}
"""
