from google import genai
import os
import json
import webbrowser
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_and_save_project(prompt, output_dir="generated_project"):
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

    # Parse JSON response
    try:
        data = json.loads(response.text) #type: ignore
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Raw response:\n{response.text}")
        with open("error/raw_response.txt", "w", encoding="utf-8") as f:
            f.write(str(response.text))
        return []

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Save all files
    saved_files = []
    for file_data in data.get('files', []):
        filename = file_data.get('name', f'file_{len(saved_files)}.txt')
        content = file_data.get('content', '')
        
        filepath = os.path.join(output_dir, filename)
        
        # Create subdirectories if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        saved_files.append(filepath)
        print(f"✓ Saved: {filepath} ({len(content)} chars)")

    return saved_files


def open_project(saved_files):
    """Open the main HTML file in browser."""
    html_file = next((f for f in saved_files if f.endswith('.html')), None)
    
    if html_file:
        print(f"\n🚀 Opening {html_file} in browser...")
        webbrowser.open(f'file://{os.path.abspath(html_file)}')
    else:
        print("⚠ No HTML file found")


# Example usage
if __name__ == "__main__":
    # Test with different projects
    prompts = [
        "Build a calculator",
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"\n{'='*60}")
        print(f"Generating project {i+1}: {prompt[:50]}...")
        print('='*60)
        
        output_dir = f"project_{3}"
        files = generate_and_save_project(prompt, output_dir)
        
        if files:
            print(f"\n✅ Generated {len(files)} files in '{output_dir}/'")
            open_project(files)
        else:
            print("❌ No files generated")