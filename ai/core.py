
#Rahl xmd 
#Albert Nyasimi 
#rahl
#lord rahl 
#
# ai/core.py
import os
import requests

MODES = {
    "royal": {
        "label": "ROYAL",
        "system": "You are RAHL-X in Royal Mode — a wise, authoritative, and supremely confident AI advisor. Speak with elegance and gravitas. Provide structured clarity. Always sign responses nobly.",
    },
    "tech": {
        "label": "TECH",
        "system": "You are RAHL-X in Tech Mode — a precise, analytical AI engineer. Provide code, diagrams in text, and step-by-step solutions. Avoid fluff.",
    },
    "creative": {
        "label": "CREATIVE",
        "system": "You are RAHL-X in Creative Mode — an imaginative AI muse. Use vivid language, storytelling, and artistic exploration.",
    }
}

API_URL = "https://api.anthropic.com/v1/messages"
API_KEY = os.getenv("RAHL_API_KEY")  

def generate_response(messages, mode="royal", max_tokens=1000):
    if mode not in MODES:
        mode = "royal"

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": max_tokens,
        "system": MODES[mode]["system"],
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        # Some APIs return a 'content' or 'completion' object, adjust if needed
        reply = data.get("content", "") or data.get("completion", "")
        return reply
    except Exception as e:
        return f"Error: {str(e)}"
