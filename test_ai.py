from google import genai
import os
import json
from dotenv import load_dotenv



def prompt_3(prompt, check):
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

extctly give me only prompt nothing else.
You are an AI assistant. Summarize all responses under 100 tokens, concise and factual.
"""



load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_project(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    return response.text


def generate_files(prompt):
    data = json.loads(generate_project(prompt))
    
    files = {}
    for file_data in data.get('files', []):
        filename = file_data.get('name', f'file_{len(files)}.txt') #type: ignore
        content = file_data.get('content', '')
        files[filename] = content #type: ignore
    return files

if __name__ == "__main__":
    prompts = "Build a calculator"
    check = """1. The application must be fully functional and visually appealing.
    Make sure it has readme.md file."""
    
    final_prompt = prompt_3(prompts, check)
    p =generate_project(final_prompt)
    p = json.loads(p).get("prompt",p)
    actual_prompt = p + """
            Return your response as JSON with this exact structure:
        {{
          "files": [
            {{"name": "filename.ext", "content": "file content here"}},
            ...
          ]
        }}
    """
    data = generate_project(actual_prompt)
    files = generate_files(data)
    
    print(files)
    for filename, content in files.items():
        filepath = os.path.join("generated_project", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Saved: {filepath}")