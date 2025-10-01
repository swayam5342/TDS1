from google import genai
import os  
from dotenv import load_dotenv
load_dotenv()


# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt = """
Generate a complete,snake ladder game for web using html,css and javascript.
"""
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt
)
print(response.text)