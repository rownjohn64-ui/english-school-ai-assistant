from pathlib import Path
from typing import Iterable

from docx import Document
from pypdf import PdfReader

from rag.store import COLLECTION_NAME, get_collection

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}

def _read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def _read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def _read_docx(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

def load_documents(data_dir: Path) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []

    for path in sorted(data_dir.iterdir()):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        if path.suffix.lower() in {".txt", ".md"}:
            text = _read_txt(path)
        elif path.suffix.lower() == ".pdf":
            text = _read_pdf(path)
        else:
            text = _read_docx(path)

        text = text.strip()
        if text:
            documents.append({"source": path.name, "text": text})

    return documents

def split_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)

    return chunks

def get_stats() -> dict[str, str | int]:
    collection = get_collection()
    count = collection.count()
    data_dir = Path("data")
    documents = sum(
        1
        for path in data_dir.glob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    return {
        "collection": COLLECTION_NAME,
        "documents": documents,
        "chunks": count,
        "status": "индексация завершена" if count else "база пуста",
    }
