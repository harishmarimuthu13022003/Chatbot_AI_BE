from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId

from models import ChatCreate, ChatMessage, ChatResponse, MessageResponse
from database import get_collection
from auth import get_current_user
from services.llm import generate_chat_response

router = APIRouter()

# Helper to fix MongoDB ObjectId to string
def fix_id(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@router.post("/chats", response_model=ChatResponse)
async def create_chat(chat: ChatCreate, email: str = Depends(get_current_user)):
    chats_collection = get_collection("chats")
    new_chat = {
        "user_email": email,
        "title": chat.title,
        "created_at": datetime.utcnow()
    }
    result = await chats_collection.insert_one(new_chat)
    new_chat["_id"] = result.inserted_id
    return fix_id(new_chat)

@router.get("/history", response_model=List[ChatResponse])
async def get_history(email: str = Depends(get_current_user)):
    chats_collection = get_collection("chats")
    cursor = chats_collection.find({"user_email": email}).sort("created_at", -1)
    chats = await cursor.to_list(length=100)
    return [fix_id(chat) for chat in chats]

@router.get("/chats/{chat_id}/messages", response_model=List[MessageResponse])
async def get_chat_messages(chat_id: str, email: str = Depends(get_current_user)):
    chats_collection = get_collection("chats")
    messages_collection = get_collection("messages")
    try:
        obj_id = ObjectId(chat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid chat ID")
        
    chat = await chats_collection.find_one({"_id": obj_id, "user_email": email})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
        
    cursor = messages_collection.find({"chat_id": chat_id}).sort("created_at", 1)
    messages = await cursor.to_list(length=100)
    return [fix_id(msg) for msg in messages]

@router.post("/chat", response_model=MessageResponse)
async def send_message(message: ChatMessage, email: str = Depends(get_current_user)):
    chats_collection = get_collection("chats")
    messages_collection = get_collection("messages")
    try:
        obj_id = ObjectId(message.chat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid chat ID")
        
    # Verify chat belongs to user
    chat = await chats_collection.find_one({"_id": obj_id, "user_email": email})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Save user message
    user_msg = {
        "chat_id": message.chat_id,
        "role": "user",
        "content": message.content,
        "created_at": datetime.utcnow()
    }
    await messages_collection.insert_one(user_msg)

    # Fetch previous messages for context
    cursor = messages_collection.find({"chat_id": message.chat_id}).sort("created_at", 1)
    db_messages = await cursor.to_list(length=20) # get last 20 messages for context
    
    formatted_messages = [{"role": msg["role"], "content": msg["content"]} for msg in db_messages]
    
    # Generate AI response
    ai_content = await generate_chat_response(formatted_messages)

    # Save AI message
    ai_msg = {
        "chat_id": message.chat_id,
        "role": "assistant",
        "content": ai_content,
        "created_at": datetime.utcnow()
    }
    result = await messages_collection.insert_one(ai_msg)
    ai_msg["_id"] = result.inserted_id

    return fix_id(ai_msg)
