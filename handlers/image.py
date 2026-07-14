from uuid import uuid4

from aiogram import F, Router
from aiogram.types import Message

from services.router import route_image_request
from utils.files import ensure_temp_dir

router = Router()

@router.message(F.photo)
async def image_handler(message: Message) -> None:
    temp_dir = ensure_temp_dir()
    image_path = temp_dir / f"{uuid4().hex}.jpg"

    try:
        photo = message.photo[-1]
        file = await message.bot.get_file(photo.file_id)
        await message.bot.download_file(file.file_path, destination=image_path)

        prompt = message.caption or """
        Проанализируй изображение как преподаватель английского языка.

        Если на изображении учебное задание:
        1. Распознай текст задания.
        2. Определи тему.
        3. Кратко объясни, что нужно сделать.
        4. Предложи пользователю выбрать один из вариантов:
           — дать правильные ответы;
           — проверить его ответы;
           — объяснить правило;
           — разобрать ошибки.
        5. Не пиши общие рассуждения о пользе упражнения.
        6. Не используй Markdown-разметку.
        """.strip()
        answer = await route_image_request(message.from_user.id, image_path, prompt)
        await message.answer(answer)
    except Exception as exc:
        await message.answer(f"Ошибка анализа изображения: {exc}")
    finally:
        image_path.unlink(missing_ok=True)
