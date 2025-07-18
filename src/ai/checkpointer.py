import os
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.memory import MemorySaver

# Global checkpointer instance
_checkpointer_instance = None
_checkpointer_context = None

def get_checkpointer():
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

        print("Using PostgresSaver")
        print(f"Connection String: {DATABASE_URL}")
        
        try:
            # Create the PostgresSaver context manager
            _checkpointer_context = PostgresSaver.from_conn_string(DATABASE_URL)
            
            # Enter the context to get the actual checkpointer
            _checkpointer_instance = _checkpointer_context.__enter__()
            
            # Setup the checkpointer tables
            _checkpointer_instance.setup()
            print("PostgresSaver setup complete")
            
        except Exception as e:
            print(f"Error setting up PostgresSaver: {e}")
            print("Falling back to MemorySaver")
            _checkpointer_instance = MemorySaver()
        
    else:
        print("Using MemorySaver")
        _checkpointer_instance = MemorySaver()
    
    return _checkpointer_instance