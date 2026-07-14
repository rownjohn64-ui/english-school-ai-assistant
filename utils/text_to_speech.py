from pathlib import Path
from uuid import uuid4

from config import settings
from services.openai_client import async_client
from utils.files import ensure_temp_dir

async def text_to_speech(text: str) -> Path | None:
    output_path = ensure_temp_dir() / f"{uuid4().hex}.mp3"

    try:
        response = await async_client.audio.speech.create(
            model=settings.tts_model,
            voice=settings.tts_voice,
            input=text[:4000],
        )
        await response.astream_to_file(output_path)
        return output_path
    except Exception:
        return None
