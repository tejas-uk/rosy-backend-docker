import os

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

# OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL") or None
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") or None
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY") or None

if not OPENAI_API_KEY:
    raise NotImplementedError("OPENAI_API_KEY is not set")

if not ANTHROPIC_API_KEY:
    raise NotImplementedError("ANTHROPIC_API_KEY is not set")

def get_llm(provider: str = "openai", model_name: str = "gpt-4.1-mini"):
    if provider == "openai":
        openai_params = {
            "model": model_name,
            "api_key": OPENAI_API_KEY,
        }
        return ChatOpenAI(**openai_params)
    
    elif provider == "anthropic":
        anthropic_params = {
            "model": model_name,
            "api_key": ANTHROPIC_API_KEY,
        }
        return ChatAnthropic(**anthropic_params)
    
    else:
        raise NotImplementedError(f"Provider {provider} is not supported")
    