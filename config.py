from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    openai_api_key: str
    openai_base_url: str
    text_model: str
    vision_model: str
    stt_model: str
    tts_model: str
    tts_voice: str
    embedding_model: str
    admin_id: int

def load_settings() -> Settings:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not token:
        raise RuntimeError("Не задан TELEGRAM_BOT_TOKEN в файле .env")
    if not api_key:
        raise RuntimeError("Не задан OPENAI_API_KEY в файле .env")

    return Settings(
        telegram_bot_token=token,
        openai_api_key=api_key,
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").strip(),
        text_model=os.getenv("TEXT_MODEL", "gpt-4o-mini").strip(),
        vision_model=os.getenv("VISION_MODEL", "gpt-4o-mini").strip(),
        stt_model=os.getenv("STT_MODEL", "whisper-1").strip(),
        tts_model=os.getenv("TTS_MODEL", "gpt-4o-mini-tts").strip(),
        tts_voice=os.getenv("TTS_VOICE", "alloy").strip(),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small").strip(),
        admin_id=int(os.getenv("ADMIN_ID", "0")),
    )

settings = load_settings()
