# memory/memory.py
import os
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
MEMORY_DIR = BASE_DIR / "user_memory"
MEMORY_DIR.mkdir(exist_ok=True)

def get_memory_path(user_id):
    return MEMORY_DIR / f"{user_id}.json"

def load_memory(user_id):
    path = get_memory_path(user_id)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                return []
    return []

def save_memory(user_id, messages):
    path = get_memory_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def add_message(user_id, role, content):
    messages = load_memory(user_id)
    timestamp = datetime.utcnow().isoformat()
    messages.append({"role": role, "content": content, "timestamp": timestamp})
    save_memory(user_id, messages)
  ##RAHL XMD AI
