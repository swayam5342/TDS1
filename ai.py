from pydantic_ai import Agent
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class FileData(BaseModel):
    """Represents a single file with name and content."""
    name: str = Field(description="The filename including extension")
    content: str = Field(description="The file content")


class ProjectResponse(BaseModel):
    """Response structure containing a list of project files."""
    files: List[FileData] = Field(description="List of files in the project")


# Initialize agent with Gemini model and structured output
agent = Agent(
    'gemini-2.5-flash',
    output_type=ProjectResponse,
    system_prompt=("""
        Return your response as JSON with this exact structure:
{{
  "files": [
    {{"name": "filename.ext", "content": "file content here"}},
    ...
  ]
}}

Include ALL necessary files (HTML, CSS, JS, etc.) also make the readme of the project and give it a description. Return ONLY valid JSON, no explanations.
don't add any explanations or additional text. like commenting the code or describing what the code does."""
    )
)


def generate_project(prompt: str) -> dict[str, str]:
    try:
        result = agent.run_sync(prompt)
        project_response = result.output
        
        # Convert to dictionary
        output = {}
        for file in project_response.files:
            output[file.name] = file.content
        
        return output
        
    except Exception as e:
        print(f"❌ Error generating project: {e}")
        return {}




def main():
    prompt = "Create a simple calculator"
    files = generate_project(prompt)
    
    if files:
        print(f"\n✅ Generated {len(files)} file(s):\n")
        for filename, content in files.items():
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Created file: {filename}")
    else:
        print("❌ No files were generated")


if __name__ == "__main__":
    main()