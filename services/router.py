from pathlib import Path

from config import settings
from rag.query import answer_with_rag
from services.openai_client import async_client
from services.session_store import append_history, get_history
from utils.speech_to_text import speech_to_text
from utils.text_to_speech import text_to_speech
from utils.vision import analyze_image
from utils.text_cleaner import clean_telegram_text
import re

SYSTEM_PROMPT = """
Ты дружелюбный AI-ассистент онлайн-школы английского языка.

Отвечай понятно, вежливо и по существу.

Не используй Markdown-разметку.
Не используй символы **, __, #, ``` и другие служебные символы.
Для оформления используй обычный текст, нумерацию и переносы строк.
""".strip()

async def route_text_request(user_id: int, text: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *get_history(user_id),
        {"role": "user", "content": text},
    ]

    response = await async_client.chat.completions.create(
        model=settings.text_model,
        messages=messages,
        temperature=0.4,
    )
    answer = response.choices[0].message.content or "Не удалось сформировать ответ."
    answer = clean_telegram_text(answer)

    append_history(user_id, "user", text)
    append_history(user_id, "assistant", answer)
    return answer

async def route_rag_request(user_id: int, text: str) -> str:
    answer = await answer_with_rag(text, get_history(user_id))
    append_history(user_id, "user", text)
    append_history(user_id, "assistant", answer)
    return answer

async def route_voice_request(user_id: int, audio_path: Path) -> dict:
    transcript = await speech_to_text(audio_path)
    answer = await route_text_request(user_id, transcript)
    audio_answer_path = await text_to_speech(answer)
    return {
        "transcript": transcript,
        "answer": answer,
        "audio_path": str(audio_answer_path) if audio_answer_path else None,
    }

async def route_image_request(user_id: int, image_path: Path, prompt: str) -> str:
    answer = await analyze_image(image_path, prompt)
    answer = clean_telegram_text(answer)

    append_history(user_id, "user", f"[Изображение] {prompt}")
    append_history(user_id, "assistant", answer)
    return answer

def clean_telegram_text(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"`{1,3}(.*?)`{1,3}", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    return text.strip()
