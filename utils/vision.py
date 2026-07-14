import base64
from pathlib import Path

from config import settings
from services.openai_client import async_client
from utils.text_cleaner import clean_telegram_text


def encode_image(image_path: Path) -> str:
    return base64.b64encode(image_path.read_bytes()).decode("utf-8")


async def analyze_image(image_path: Path, prompt: str) -> str:
    encoded_image = encode_image(image_path)

    system_prompt = """
    Ты преподаватель английского языка и помощник ученика.

    Если пользователь отправляет изображение с упражнением:

    1. Полностью распознай текст задания.
    2. Обязательно перепиши все предложения и варианты, которые видны на изображении.
    3. Определи тему упражнения.
    4. Кратко объясни, что нужно сделать.
    5. Предложи пользователю выбрать:
       1) дать правильные ответы;
       2) проверить его ответы;
       3) объяснить правило;
       4) разобрать ошибки.

    Очень важно: не ограничивайся общим описанием изображения.
    Полный распознанный текст задания должен присутствовать в ответе, чтобы его можно было использовать в следующих сообщениях диалога.

    Не используй Markdown-разметку.
    Не используй символы **, __, # и ```.

    Если изображение не относится к изучению английского языка, кратко опиши его содержимое.
    """.strip()
    user_prompt = prompt or """
Проанализируй изображение. Распознай задание, определи тему и объясни, что нужно сделать.
""".strip()

    response = await async_client.chat.completions.create(
        model=settings.vision_model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        },
                    },
                ],
            },
        ],
        max_tokens=1000,
    )

    answer = (
        response.choices[0].message.content
        or "Не удалось проанализировать изображение."
    )

    return clean_telegram_text(answer)