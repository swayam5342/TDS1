from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_project(prompt):
    """
    Generate a web project using Gemini and save all files.
    Works with any number of files.
    """

    full_prompt = f"""
{prompt}

Return your response as JSON with this exact structure:
{{
  "files": [
    {{"name": "filename.ext", "content": "file content here"}},
    ...
  ]
}}

Include ALL necessary files (HTML, CSS, JS, etc.). Return ONLY valid JSON, no explanations.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt,
        config={"response_mime_type": "application/json"}
    )
    try:
        data = json.loads(response.text) #type: ignore
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Raw response:\n{response.text}")
        with open("error/raw_response.txt", "w", encoding="utf-8") as f:
            f.write(str(response.text))
        return {}
    files = {}
    for file_data in data.get('files', []):
        filename = file_data.get('name', f'file_{len(files)}.txt')
        content = file_data.get('content', '')
        files[filename] = content
    return files



if __name__ == "__main__":
    prompts = [
        "Build a calculator",
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"\n{'='*60}")
        print(f"Generating project {i+1}: {prompt[:50]}...")
        print('='*60)
        files = generate_project(prompt)
        for filename, content in files.items():
            filepath = os.path.join("generated_project", filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✓ Saved: {filepath}")