# core.py
import os
import openai  # You can replace with Anthropic or other LLM provider

openai.api_key = os.getenv("OPENAI_API_KEY")  # Do not store real key in repo

MODES = {
    "royal": {
        "system": "You are RAHL-X in Royal Mode — wise, authoritative, and eloquent. Speak with gravitas, structure, and vision."
    },
    "tech": {
        "system": "You are RAHL-X in Tech Mode — precise, analytical, and solution-focused. Provide structured code, diagrams, and step-by-step breakdowns."
    },
    "creative": {
        "system": "You are RAHL-X in Creative Mode — imaginative, artistic, and expressive. Use vivid storytelling and bold ideas."
    }
}

def generate_reply(user_input: str, mode: str, history: list) -> str:
    system_prompt = MODES.get(mode, MODES["royal"])["system"]
    messages = [{"role": "system", "content": system_prompt}]
    
    for h in history[-20:]:  # only last 20 messages to save context
        messages.append({"role": h["role"], "content": h["content"]})
    
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        reply = response.choices[0].message.content.strip()
        return reply
    except Exception as e:
        return f"RAHL-X encountered an error: {str(e)}"
