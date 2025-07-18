import uuid
from typing import List, Optional
from sqlmodel import Session, select
from api.models import Chat, User, get_utc_now
from ai.graph import get_agent
from ai.checkpointer import get_checkpointer
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.base import CheckpointTuple
from api.models import SimpleMessage, ChatHistory


class ChatService:
    """Service for managing chats using LangGraph checkpointer."""
    
    def __init__(self):
        self.agent = None
        self.checkpointer = None
    
    async def _ensure_initialized(self):
        """Ensure agent and checkpointer are initialized."""
        if self.agent is None:
            self.agent = await get_agent()
        if self.checkpointer is None:
            self.checkpointer = await get_checkpointer()
    
    def create_chat(self, session: Session, user: User, title: Optional[str] = None) -> Chat:
        """Create a new chat with a unique thread ID."""
        thread_id = str(uuid.uuid4())
        
        chat = Chat(
            user_id=user.id,
            thread_id=thread_id,
            title=title or "New Chat"
        )
        
        session.add(chat)
        session.commit()
        session.refresh(chat)
        
        return chat
    
    async def get_chat_messages(self, session: Session, chat: Chat, user: User) -> ChatHistory:
        """Get all messages for a chat from LangGraph checkpointer."""
        await self._ensure_initialized()
        
        config = {"configurable": {"thread_id": chat.thread_id, "user_id": user.id}}
        
        print(f"Getting messages for chat {chat.id} with thread_id: {chat.thread_id}")
        print(f"Checkpointer type: {type(self.checkpointer)}")
        
        try:
            # Get the latest checkpoint
            state = self.agent.get_state(config)
            messages = state.values.get("messages", []) if state.values else []
        except Exception:
            # If no state exists, return empty conversation
            messages = []
        
        # Convert messages to response format
        message_responses = []
        for msg in messages:
            message_responses.append(SimpleMessage(
                content=msg.content,
                type=msg.type
            ))
        
        return ChatHistory(
            messages=message_responses,
            title=chat.title,
            thread_id=chat.thread_id
        )

    
    async def send_message(self, session: Session, chat: Chat, content: str, user: User) -> dict:
        """Send a message and get AI response using LangGraph."""
        await self._ensure_initialized()
        
        config = {"configurable": {"thread_id": chat.thread_id, "user_id": user.id}}
        
        print(f"Sending message to chat {chat.id} with thread_id: {chat.thread_id}")
        
        # Check if this is the first message to set the title
        checkpoint_tuple = await self.checkpointer.aget_tuple(config)
        is_first_message = checkpoint_tuple is None or not checkpoint_tuple[1].get("messages")
        print(f"Is first message: {is_first_message}")
        
        # Set title from first message if not already set
        if is_first_message and not chat.title:
            chat.title = f"{content[:20]}..."
        
        # Update chat timestamp
        chat.updated_at = get_utc_now()

        session.add(chat)
        session.commit()
        
        # Invoke the agent with the message
        try:
            print(f"Invoking agent with message: {content}")
            response = await self.agent.ainvoke(
                {"messages": [HumanMessage(content=content)]}, 
                config=config
            )
            print(f"Agent response keys: {response.keys()}")
            print(f"Agent response messages count: {len(response.get('messages', []))}")
            
            # Extract the AI response
            last_message = next((m for m in reversed(response["messages"])
                                if isinstance(m, AIMessage)), None)
            
            ai_content = last_message.content if last_message else "No response from AI"
            print(f"AI content: {ai_content}")
            
            return {
                "content": ai_content,
            }
            
        except Exception as e:
            print(f"Error invoking agent: {e}")
            import traceback
            traceback.print_exc()
            return {
                "content": "Sorry, I encountered an error processing your message."
            }
    
    def delete_chat(self, session: Session, chat: Chat) -> bool:
        """Delete a chat and its associated thread data."""
        try:
            # Delete the thread from LangGraph checkpointer
            config = {"configurable": {"thread_id": chat.thread_id}}
            # Note: LangGraph doesn't have a direct delete method, but we can mark as deleted
            chat.is_deleted = True
            session.add(chat)
            session.commit()
            return True
        except Exception as e:
            print(f"Error deleting chat: {e}")
            return False
    
    def update_chat_title(self, session: Session, chat: Chat, title: str) -> bool:
        """Update the chat title."""
        try:
            chat.title = title
            chat.updated_at = get_utc_now()
            session.add(chat)
            session.commit()
            return True
        except Exception as e:
            print(f"Error updating chat title: {e}")
            return False 