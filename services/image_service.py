import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL")


class ImageService:

    @staticmethod
    def generate_image(prompt: str):

        client = InferenceClient(
            api_key=HF_TOKEN
        )

        image = client.text_to_image(
            prompt=prompt,
            model=HF_MODEL
        )

        image_dir = Path("generated_images")
        image_dir.mkdir(exist_ok=True)

        filename = f"{uuid.uuid4().hex}.png"
        filepath = image_dir / filename

        image.save(filepath)

        return f"/generated_images/{filename}"