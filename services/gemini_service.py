import os

from dotenv import load_dotenv
from google import genai

from services.prompt_builder import build_story_prompt

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def generate_story(data):
    prompt = build_story_prompt(data)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text