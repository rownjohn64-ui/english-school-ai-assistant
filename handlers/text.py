from aiogram import F, Router
from aiogram.types import Message

from services.router import route_rag_request, route_text_request
from services.session_store import get_mode

router = Router()

@router.message(F.text)
async def text_handler(message: Message) -> None:
    text = (message.text or "").strip()
    if not text or text.startswith("/"):
        return

    user_id = message.from_user.id
    mode = get_mode(user_id)

    try:
        if mode == "rag":
            answer = await route_rag_request(user_id, text)
        else:
            answer = await route_text_request(user_id, text)

        await message.answer(answer)
    except Exception as exc:
        await message.answer(f"Не удалось обработать запрос: {exc}")
