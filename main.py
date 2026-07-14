import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import settings
from handlers import start, text, voice, image, document_upload

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(document_upload.router)
    dp.include_router(voice.router)
    dp.include_router(image.router)
    dp.include_router(text.router)

    logging.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
