from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from services.session_store import (
    clear_history,
    get_mode,
    set_mode,
)
from rag.index import index_documents
from rag.loader import get_stats

router = Router()

HELP_TEXT = """
Я AI-ассистент онлайн-школы английского языка.

Команды:
/start — запустить бота
/help — показать справку
/mode text — обычный текстовый режим
/mode rag — ответы по базе знаний
/mode voice — голосовой режим
/reset — очистить историю
/index — проиндексировать документы из data/
/stats — показать состояние базы знаний

Также можно отправить изображение для анализа.
""".strip()

@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "Здравствуйте! Я AI-ассистент онлайн-школы английского языка.\n\n"
        + HELP_TEXT
    )

@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(HELP_TEXT)

@router.message(Command("mode"))
async def mode_handler(message: Message) -> None:
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) == 1:
        await message.answer(f"Текущий режим: {get_mode(message.from_user.id)}")
        return

    mode = parts[1].strip().lower()
    if mode not in {"text", "rag", "voice"}:
        await message.answer("Допустимые режимы: text, rag, voice")
        return

    set_mode(message.from_user.id, mode)
    await message.answer(f"Режим {mode} включён.")

@router.message(Command("reset"))
async def reset_handler(message: Message) -> None:
    clear_history(message.from_user.id)
    set_mode(message.from_user.id, "text")
    await message.answer("История очищена. Включён режим text.")

@router.message(Command("index"))
async def index_handler(message: Message) -> None:
    await message.answer("Начинаю индексацию документов...")
    try:
        result = index_documents()
        await message.answer(
            "Индексация завершена.\n"
            f"Файлов обработано: {result['documents']}\n"
            f"Чанков создано: {result['chunks']}"
        )
    except Exception as exc:
        await message.answer(f"Ошибка индексации: {exc}")

@router.message(Command("stats"))
async def stats_handler(message: Message) -> None:
    stats = get_stats()
    await message.answer(
        "Статус базы знаний:\n"
        f"• Коллекция: {stats['collection']}\n"
        f"• Документов: {stats['documents']}\n"
        f"• Чанков: {stats['chunks']}\n"
        f"• Статус: {stats['status']}"
    )
