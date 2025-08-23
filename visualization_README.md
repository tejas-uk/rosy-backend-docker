# Graph Architecture Visualization Scripts

This directory contains utility scripts to visualize the Rosy AI multi-agent architecture.

## Scripts

### 1. `visualize_graph.py`
Creates comprehensive architecture diagrams showing:
- Full multi-agent system architecture with all components
- Communication flows between agents
- Tool integrations (Tavily, Pinecone, Mem0)
- State management flow

### 2. `visualize_langgraph.py`
Generates LangGraph-specific visualizations:
- Conceptual graph flow (START → Agent → Memory → END)
- Detailed supervisor agent internals
- Emotion detection and routing logic

## Installation

```bash
pip install -r requirements-viz.txt
```

## Usage

Generate all visualizations:
```bash
python visualize_graph.py
python visualize_langgraph.py
```

## Output Files

The scripts generate the following files:
- `rosy_architecture_diagram.png/pdf` - Complete system architecture
- `rosy_state_flow_diagram.png/pdf` - State flow through the system
- `langgraph_conceptual_flow.png` - LangGraph implementation flow
- `supervisor_agent_detail.png` - Detailed view of supervisor internals

## Architecture Overview

The visualizations show:

1. **Three-Layer Architecture**:
   - User/API Layer (FastAPI endpoints)
   - Agent Layer (Supervisor + specialized agents)
   - Tool/Storage Layer (Tavily, Pinecone, Mem0)

2. **Communication Patterns**:
   - Black arrows: Synchronous API calls
   - Blue arrows: Agent handoffs
   - Purple arrows: Tool invocations
   - Orange arrows: Memory operations

3. **Key Components**:
   - **Supervisor Agent (GPT-4o)**: Orchestrates the system
   - **Research Agent (GPT-4.1-mini)**: Handles web search and knowledge retrieval
   - **Memory Agent (GPT-4.1-mini)**: Manages persistent user context
   - **Mem0 Memory Layer**: Provides 90% token reduction with hybrid storage

## Customization

You can modify the scripts to:
- Change colors in the `colors` dictionary
- Add new components or connections
- Adjust layout and positioning
- Generate additional diagram types