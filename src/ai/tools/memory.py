import os
from mem0 import AsyncMemoryClient
from typing import List, Dict, Optional
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

MEM0_API_KEY = os.environ.get("MEM0_API_KEY") or None

if not MEM0_API_KEY:
    raise NotImplementedError("MEM0_API_KEY is not set")

client = AsyncMemoryClient(api_key=MEM0_API_KEY)


@tool
async def add_to_memory(messages: list[dict], config: RunnableConfig) -> str:
    """Add a message to the memory.
    
    Args:
        messages: The latest conversation messages to add to the memory.
        user_id: The id of the user to add the memory to.
        metadata: The metadata to add to the memory. Format: {"category": "string"}
    """
    global client
    user_id = config["metadata"].get("user_id")
    await client.add(
        messages,
        user_id=user_id,
    )
    return "Memory added successfully"

@tool
async def get_from_memory(query: str, config: RunnableConfig) -> str:
    """Get the memory for a user.
    
    Args:
        query: The query to get the memory for.
        user_id: The id of the user to get the memory for.
    
    Returns:
        Top matching memories for the user.
    """
    global client
    user_id = config["metadata"].get("user_id")
    print(f"User ID: {user_id}")
    memories = await client.search(query, user_id=user_id)
    print(f"Memories: {memories}")
    return memories