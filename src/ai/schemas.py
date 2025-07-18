from typing import Annotated, List
from pydantic import BaseModel, Field
from typing import TypedDict, Literal, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """State of the agent."""
    messages: Annotated[List[BaseMessage], add_messages]



class AIResponse(BaseModel):
    """Response from the AI model."""
    content: str

class WebSearchResponse(BaseModel):
    """Response from the web search."""
    content: str = Field(description="The main content or summary from the web search results")
    sources: List[str] = Field(description="List of URLs or source references used in the web search")
