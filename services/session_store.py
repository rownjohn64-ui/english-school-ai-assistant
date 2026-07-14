from collections import defaultdict
from typing import Any

_modes: dict[int, str] = defaultdict(lambda: "text")
_history: dict[int, list[dict[str, Any]]] = defaultdict(list)

MAX_HISTORY_MESSAGES = 12

def get_mode(user_id: int) -> str:
    return _modes[user_id]

def set_mode(user_id: int, mode: str) -> None:
    _modes[user_id] = mode

def get_history(user_id: int) -> list[dict[str, Any]]:
    return list(_history[user_id])

def append_history(user_id: int, role: str, content: str) -> None:
    _history[user_id].append({"role": role, "content": content})
    _history[user_id] = _history[user_id][-MAX_HISTORY_MESSAGES:]

def clear_history(user_id: int) -> None:
    _history[user_id].clear()
