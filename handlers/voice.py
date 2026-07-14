from pathlib import Path
from uuid import uuid4

from aiogram import F, Router
from aiogram.types import FSInputFile, Message

from services.router import route_voice_request
from services.session_store import get_mode
from utils.files import ensure_temp_dir

router = Router()

@router.message(F.voice)
async def voice_handler(message: Message) -> None:
    user_id = message.from_user.id
    mode = get_mode(user_id)

    if mode != "voice":
        await message.answer("Сначала включите голосовой режим командой /mode voice")
        return

    temp_dir = ensure_temp_dir()
    ogg_path = temp_dir / f"{uuid4().hex}.ogg"

    try:
        file = await message.bot.get_file(message.voice.file_id)
        await message.bot.download_file(file.file_path, destination=ogg_path)

        result = await route_voice_request(user_id, ogg_path)

        await message.answer(
            f"Отправил голосовое: {result['transcript']}\n\n"
            f"{result['answer']}"
        )

        audio_path = result.get("audio_path")
        if audio_path and Path(audio_path).exists():
            await message.answer_voice(FSInputFile(audio_path))
    except Exception as exc:
        await message.answer(f"Ошибка обработки голосового сообщения: {exc}")
    finally:
        if ogg_path.exists():
            ogg_path.unlink(missing_ok=True)
