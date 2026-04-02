# server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid

from core import generate_reply
from memory.memory import load_memory, add_message

app = FastAPI(title="RAHL-X Backend")

origins = ["*"]  # In production, replace "*" with your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    user_id: str
    content: str
    mode: str

@app.post("/chat")
async def chat(msg: ChatMessage):
    if not msg.content.strip():
        raise HTTPException(status_code=400, detail="Empty message not allowed")

    if not msg.user_id:
        msg.user_id = str(uuid.uuid4())

    add_message(msg.user_id, "user", msg.content)
    history = load_memory(msg.user_id)
    
    response = generate_reply(msg.content, msg.mode, history)
    
    add_message(msg.user_id, "assistant", response)
    return {"user_id": msg.user_id, "reply": response}
