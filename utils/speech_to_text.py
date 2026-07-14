from pathlib import Path

from config import settings
from services.openai_client import async_client

async def speech_to_text(audio_path: Path) -> str:
    with audio_path.open("rb") as audio_file:
        response = await async_client.audio.transcriptions.create(
            model=settings.stt_model,
            file=audio_file,
        )
    return response.text.strip()
