from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlmodel import Session, select
from typing import List
from api.db import get_session
from api.models import (
    Chat,
    User,
    MessagePayload,
    ChatHistory
)
from api.auth.routing import get_current_user
from ai.schemas import AIResponse
from api.chat.service import ChatService

router = APIRouter(prefix="/api/chats", tags=["chats"])
chat_service = ChatService()

# Health check
@router.get("/health")
async def health_check():
    return {"status": "healthy"}

# 1. List chats
@router.get("/list_chats", response_model=List[Chat])
async def list_chats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    chats = session.exec(select(Chat).where(Chat.user_id == current_user.id, Chat.is_deleted == False)).all()
    return chats

# 2. Create chat
@router.post("/create_chat", response_model=Chat)
async def create_chat(
    chat: Chat,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return chat_service.create_chat(session, current_user, chat.title)

# 3. Get chat Messages
@router.get("/get_chat_messages", response_model=ChatHistory)
async def get_chat_messages(
    chat_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    chat = session.get(Chat, chat_id)
    if not chat or chat.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this chat")
    
    messages = chat_service.get_chat_messages(session, chat, current_user)
    return messages

# 4. Send message and 5. Get message from AI model
@router.post("/send_message", response_model=AIResponse)
async def send_message(
    chat_id: int,
    payload: MessagePayload,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    chat = session.get(Chat, chat_id)
    if not chat or chat.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this chat")
    
    result = chat_service.send_message(session, chat, payload.content, current_user)
    return AIResponse(content=result["content"])

# Edit title of chat
@router.put("/edit_chat_title", status_code=status.HTTP_200_OK)
async def edit_chat_title(
    chat_id: int,
    title: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    chat = session.get(Chat, chat_id)
    if not chat or chat.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this chat")
    
    success = chat_service.update_chat_title(session, chat, title)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update chat title")
    
    return {"detail": "Chat title updated successfully"}

# Delete chat
@router.delete("/{chat_id}/delete_chat", status_code=status.HTTP_200_OK)
async def delete_chat(
    chat_id: int = Path(..., description="The ID of the chat"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    chat = session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    if chat.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this chat")
    
    success = chat_service.delete_chat(session, chat)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete chat")
    
    return {"detail": "Chat deleted successfully"}