from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain_core.messages import HumanMessage, SystemMessage
from ai.checkpointer import get_checkpointer
from ai.llms import get_llm
from ai.tools import (
    add_to_memory,
    get_from_memory,
    web_search,
    search_pinecone
)
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Open the YAML file
with open(f'{BASE_DIR}/config.yaml', 'r') as file:
    config = yaml.safe_load(file)


def get_research_agent():
    model_config = config["llm_models"]["research_agent"]
    
    llm = get_llm(provider=model_config["provider"], model_name=model_config["model"])
    
    with open(f'{BASE_DIR}/prompts/{model_config["prompt_file"]}', 'r') as file:
        prompt = file.read()
    
    tools = [web_search, search_pinecone]
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt,
        name="research_agent",
    )

    return agent


def get_relevant_memory_agent():
    model_config = config["llm_models"]["relevant_memory_agent"]
    llm = get_llm(provider=model_config["provider"], model_name=model_config["model"])
    with open(f'{BASE_DIR}/prompts/{model_config["prompt_file"]}', 'r') as file:
        prompt = file.read()
    tools = [get_from_memory]
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt,
        name="relevant_memory_agent",  
    )

    return agent

async def get_supervisor_agent():
    model_config = config["llm_models"]["supervisor"]  
    # checkpointer = await get_checkpointer()

    llm = get_llm(provider=model_config["provider"], model_name=model_config["model"])
    with open(f'{BASE_DIR}/prompts/{model_config["prompt_file"]}', 'r') as file:
        prompt = file.read()

    research_agent = get_research_agent()
    relevant_memory_agent = get_relevant_memory_agent()

    supervisor_agent = create_supervisor(
        model=llm,
        agents=[research_agent, relevant_memory_agent],
        prompt=prompt,
        # add_handoff_back_messages=True,
        # output_mode="full_history"
    ).compile(
        # checkpointer=checkpointer
    )

    return supervisor_agent