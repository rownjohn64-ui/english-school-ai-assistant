from openai import AsyncOpenAI, OpenAI

from config import settings

async_client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
)

sync_client = OpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
)
