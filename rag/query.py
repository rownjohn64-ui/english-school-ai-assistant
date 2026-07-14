from config import settings
from rag.store import get_collection
from services.openai_client import async_client
from utils.text_cleaner import clean_telegram_text

RAG_SYSTEM_PROMPT = """
Ты AI-ассистент онлайн-школы английского языка.
Отвечай только на основании найденного контекста.
Если в контексте нет ответа, честно скажи, что информация не найдена.
В конце ответа обязательно укажи источники в формате:
Источник: имя_файла
""".strip()

async def answer_with_rag(question: str, history: list[dict]) -> str:
    collection = get_collection()

    if collection.count() == 0:
        return "База знаний пуста. Выполните команду /index."

    result = collection.query(
        query_texts=[question],
        n_results=min(4, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]

    context_parts: list[str] = []
    sources: list[str] = []

    for document, metadata in zip(documents, metadatas):
        source = metadata.get("source", "неизвестный файл")
        context_parts.append(f"[Источник: {source}]\n{document}")
        if source not in sources:
            sources.append(source)

    context = "\n\n".join(context_parts)

    messages = [
        {"role": "system", "content": RAG_SYSTEM_PROMPT},
        *history[-6:],
        {
            "role": "user",
            "content": f"Контекст:\n{context}\n\nВопрос: {question}",
        },
    ]

    response = await async_client.chat.completions.create(
        model=settings.text_model,
        messages=messages,
        temperature=0.1,
    )

    answer = response.choices[0].message.content or "Не удалось сформировать ответ."

    if "Источник:" not in answer:
        answer += "\n\nИсточник: " + ", ".join(sources)
    answer = clean_telegram_text(answer)
    return answer
