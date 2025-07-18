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
        self._agent = None
        self._checkpointer = None
        self._initialized = False
    
    async def _ensure_initialized(self):
        """Ensure agent and checkpointer are initialized."""
        if not self._initialized:
            self._agent = await get_agent()
            self._checkpointer = await get_checkpointer()
            self._initialized = True
    
    @property
    def agent(self):
        if not self._initialized:
            raise RuntimeError("ChatService not initialized. Call _ensure_initialized() first.")
        return self._agent
    
    @property
    def checkpointer(self):
        if not self._initialized:
            raise RuntimeError("ChatService not initialized. Call _ensure_initialized() first.")
        return self._checkpointer
    
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
        
        try:
            # Get the latest checkpoint from the checkpointer
            print(f"Getting checkpoint with config: {config}")
            checkpoint_tuple = await self.checkpointer.aget_tuple(config)
            print(f"Checkpoint tuple type: {type(checkpoint_tuple)}")
            
            if checkpoint_tuple and checkpoint_tuple[1]:
                # Extract messages from the checkpoint state
                checkpoint = checkpoint_tuple[1]
                print(f"Checkpoint: {checkpoint}")
                
                # Messages are stored in channel_values
                channel_values = checkpoint.get("channel_values", {})
                print(f"Channel values: {channel_values}")
                
                messages = channel_values.get("messages", [])
                print(f"Found {len(messages)} messages in checkpoint")
            else:
                print("No checkpoint found, returning empty messages")
                messages = []
                
        except Exception as e:
            print(f"Error getting messages from checkpointer: {e}")
            import traceback
            traceback.print_exc()
            messages = []
        
        # Convert messages to response format
        message_responses = []
        for msg in messages:
            # Determine message type based on the message class
            if hasattr(msg, 'type'):
                msg_type = msg.type
            elif hasattr(msg, '__class__'):
                if 'HumanMessage' in str(msg.__class__):
                    msg_type = "user"
                elif 'AIMessage' in str(msg.__class__):
                    msg_type = "ai"
                else:
                    msg_type = "unknown"
            else:
                msg_type = "unknown"
                
            message_responses.append(SimpleMessage(
                content=msg.content,
                type=msg_type
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
            print(f"Using config: {config}")
            
            # Get existing messages from the checkpoint
            existing_messages = []
            if checkpoint_tuple and checkpoint_tuple[1]:
                channel_values = checkpoint_tuple[1].get("channel_values", {})
                existing_messages = channel_values.get("messages", [])
                print(f"Found {len(existing_messages)} existing messages")
            
            # Add the new human message to the conversation
            all_messages = existing_messages + [HumanMessage(content=content)]
            print(f"Invoking agent with {len(all_messages)} total messages")
            
            response = await self.agent.ainvoke(
                {"messages": all_messages}, 
                config=config
            )
            print(f"Agent response keys: {response.keys()}")
            print(f"Agent response messages count: {len(response.get('messages', []))}")
            
            # Extract the AI response
            last_message = next((m for m in reversed(response["messages"])
                                if isinstance(m, AIMessage)), None)
            
            ai_content = last_message.content if last_message else "No response from AI"
            print(f"AI content: {ai_content}")
            
            # Check if the checkpoint was saved
            print("Checking if checkpoint was saved...")
            checkpoint_tuple = await self.checkpointer.aget_tuple(config)
            if checkpoint_tuple and checkpoint_tuple[1]:
                channel_values = checkpoint_tuple[1].get("channel_values", {})
                saved_messages = channel_values.get("messages", [])
                print(f"Saved messages count: {len(saved_messages)}")
            else:
                print("No checkpoint found after sending message")
            
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