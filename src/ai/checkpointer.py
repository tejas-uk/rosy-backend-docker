import os
import asyncio
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.memory import MemorySaver

# Global checkpointer instance
_checkpointer_instance = None
_checkpointer_context = None

async def get_checkpointer():
    global _checkpointer_instance, _checkpointer_context
    
    # Return existing instance if already created
    if _checkpointer_instance is not None:
        return _checkpointer_instance
    
    CHECKPOINTER = os.environ.get("CHECKPOINTER", None)
    print(f"CHECKPOINTER: {CHECKPOINTER}")
    
    if CHECKPOINTER == "postgres":
        DATABASE_URL = os.getenv("DATABASE_URL")

        if not DATABASE_URL:
            raise NotImplementedError("`DATABASE_URL` is not set")

        print("Using AsyncPostgresSaver")
        print(f"Connection String: {DATABASE_URL}")
        
        try:
            # Create the AsyncPostgresSaver context manager
            _checkpointer_context = AsyncPostgresSaver.from_conn_string(DATABASE_URL)
            
            # Enter the context to get the actual checkpointer
            _checkpointer_instance = await _checkpointer_context.__aenter__()
            
            # Setup the checkpointer tables
            await _checkpointer_instance.setup()
            print("AsyncPostgresSaver setup complete")
            
        except Exception as e:
            print(f"Error setting up AsyncPostgresSaver: {e}")
            print("Falling back to MemorySaver")
            _checkpointer_instance = MemorySaver()
        
    else:
        print("Using MemorySaver")
        _checkpointer_instance = MemorySaver()
    
    return _checkpointer_instance

# Synchronous wrapper for backward compatibility
def get_checkpointer_sync():
    """Synchronous wrapper for get_checkpointer - use only for sync operations"""
    try:
        # Try to get the existing async instance
        if _checkpointer_instance is not None:
            return _checkpointer_instance
        
        # If no instance exists, create one synchronously
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(get_checkpointer())
    except RuntimeError:
        # If no event loop is running, create a new one
        return asyncio.run(get_checkpointer())