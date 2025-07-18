from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, DateTime

def get_utc_now():
    return datetime.now().replace(tzinfo=timezone.utc)

class User(SQLModel, table=True):
    """A single account that owns chat threads."""

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True)
    email: str | None = Field(default=None, sa_column_kwargs={"unique": True})
    password_hash: str | None = Field(default=None, max_length=128)
    auth_provider: str = Field(default="local", nullable=False)
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=False
        )
    last_login_at: Optional[datetime] = Field(
        sa_type=DateTime(timezone=True),
        nullable=True
        )

    # Relationships
    chats: List["Chat"] = Relationship(back_populates="user")


class Chat(SQLModel, table=True):
    """A chat conversation (a.k.a. thread) that groups an ordered list of messages."""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    thread_id: str = Field(unique=True, nullable=False, index=True)  # LangGraph thread ID
    title: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=False,
        index=True
        )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=False,
        index=True
        )
    is_deleted: bool = Field(default=False, nullable=False)

    # Relationships
    user: User = Relationship(back_populates="chats")


# ---------------------------------------------------------------------------
# 🆕  Pydantic / response‑layer schemas
# ---------------------------------------------------------------------------

class MessagePayload(SQLModel):
    """User message to the AI model."""
    content: str

class SimpleMessage(SQLModel):
    """Simple message Pydantic model for API responses."""
    content: str
    type: str  # "user" or "ai"

class ChatHistory(SQLModel):
    """Chat history Pydantic model for API responses."""
    messages: List[SimpleMessage]
    title: str
    thread_id: str