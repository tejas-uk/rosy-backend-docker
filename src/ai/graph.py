import os
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from ai.schemas import AgentState
from ai.agents import get_supervisor_agent
from langchain_core.messages import AIMessage, HumanMessage
from ai.checkpointer import get_checkpointer
from ai.tools.memory import add_to_memory
from langchain_core.runnables import RunnableConfig

def agent_node(state: AgentState) -> AgentState:
    supervisor_agent = get_supervisor_agent()
    response = supervisor_agent.invoke({"messages": state["messages"]})

    return {
        "messages": state["messages"] + [AIMessage(content=response["messages"][-1].content)]
    }

def memory_node(state: AgentState) -> AgentState:
    readable_messages = []
    for m in state["messages"]:
        if isinstance(m, HumanMessage):
            readable_messages.append({"role": "user", "content": m.content})
        elif isinstance(m, AIMessage):
            readable_messages.append({"role": "assistant", "content": m.content})
    add_to_memory.invoke({"messages": readable_messages})
    return state


def get_agent():
    # Get the checkpointer instance
    checkpointer = get_checkpointer()
    
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("memory", memory_node)
    graph.add_edge(START, "agent")
    graph.add_edge("agent", "memory")
    graph.add_edge("memory", END)

    # Compile the graph with the checkpointer
    agent = graph.compile(checkpointer=checkpointer)
    
    return agent
