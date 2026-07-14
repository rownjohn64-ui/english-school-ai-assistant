from pathlib import Path

from aiogram import F, Router
from aiogram.types import Message

from config import settings
from rag.index import index_documents

router = Router()

ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}

@router.message(F.document)
async def document_handler(message: Message) -> None:
    if settings.admin_id and message.from_user.id != settings.admin_id:
        await message.answer("Загрузка документов доступна только администратору.")
        return

    filename = message.document.file_name or "document.txt"
    suffix = Path(filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        await message.answer("Поддерживаются файлы TXT, MD, PDF и DOCX.")
        return

    destination = Path("data") / filename
    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        file = await message.bot.get_file(message.document.file_id)
        await message.bot.download_file(file.file_path, destination=destination)
        result = index_documents()
        await message.answer(
            f"Файл {filename} сохранён и проиндексирован.\n"
            f"Документов: {result['documents']}, чанков: {result['chunks']}"
        )
    except Exception as exc:
        await message.answer(f"Ошибка загрузки документа: {exc}")
