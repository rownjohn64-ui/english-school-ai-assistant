from pathlib import Path

def ensure_temp_dir() -> Path:
    path = Path("temp")
    path.mkdir(parents=True, exist_ok=True)
    return path
