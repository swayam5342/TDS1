from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_prompt(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )  
    return response.text

def generate_project(prompt):
    prompt +="""
    Return your response as JSON with this exact structure:
        {{
          "files": [
            {{"name": "filename.ext", "content": "file content here"}},
            ...
          ]
        }}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
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
    ...