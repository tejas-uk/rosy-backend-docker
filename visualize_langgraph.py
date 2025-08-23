#!/usr/bin/env python3
"""
Visualization script that generates the actual LangGraph representation
This shows the exact graph structure as implemented in the code
"""

from typing import Dict, Any
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch
import asyncio

# Import the actual graph from the project
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def visualize_actual_graph():
    """Visualize the actual LangGraph implementation"""
    try:
        from ai.graph import get_agent
        from langgraph.graph import Graph
        
        # Get the compiled graph
        agent = await get_agent()
        
        # If the agent has a graph attribute, use it
        if hasattr(agent, 'graph'):
            graph = agent.graph
            
            # Create a networkx graph from the LangGraph
            G = nx.DiGraph()
            
            # Add nodes and edges from the graph
            if hasattr(graph, 'nodes'):
                for node in graph.nodes:
                    G.add_node(node)
            
            if hasattr(graph, 'edges'):
                for edge in graph.edges:
                    G.add_edge(edge[0], edge[1])
            
            # Visualize
            plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                   node_size=3000, font_size=10, font_weight='bold',
                   arrows=True, arrowsize=20, edge_color='gray')
            
            plt.title('Actual LangGraph Structure from Code', fontsize=16, weight='bold')
            plt.savefig('actual_langgraph_structure.png', dpi=300, bbox_inches='tight')
            print("✅ Saved actual graph structure as actual_langgraph_structure.png")
            
    except Exception as e:
        print(f"⚠️  Could not import actual graph: {e}")
        print("Generating conceptual diagram instead...")
        create_conceptual_graph()

def create_conceptual_graph():
    """Create a conceptual graph based on the code structure"""
    G = nx.DiGraph()
    
    # Add nodes based on the code
    nodes = {
        '__start__': {'color': 'green', 'label': 'START'},
        'agent': {'color': 'lightcoral', 'label': 'Agent Node\n(Supervisor)'},
        'memory': {'color': 'lightblue', 'label': 'Memory Node\n(Mem0)'},
        '__end__': {'color': 'red', 'label': 'END'}
    }
    
    # Add edges based on the graph.py code
    edges = [
        ('__start__', 'agent'),
        ('agent', 'memory'),
        ('memory', '__end__')
    ]
    
    # Build the graph
    for node_id, attrs in nodes.items():
        G.add_node(node_id, **attrs)
    
    G.add_edges_from(edges)
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    
    # Layout
    pos = {
        '__start__': (0, 1),
        'agent': (2, 1),
        'memory': (4, 1),
        '__end__': (6, 1)
    }
    
    # Draw nodes
    for node, (x, y) in pos.items():
        node_attrs = nodes[node]
        circle = plt.Circle((x, y), 0.5, color=node_attrs['color'], 
                           ec='black', linewidth=2)
        plt.gca().add_patch(circle)
        plt.text(x, y, node_attrs['label'], ha='center', va='center', 
                fontsize=10, weight='bold')
    
    # Draw edges
    for start, end in edges:
        x1, y1 = pos[start]
        x2, y2 = pos[end]
        plt.arrow(x1 + 0.5, y1, x2 - x1 - 1, y2 - y1, 
                 head_width=0.1, head_length=0.1, fc='black', ec='black')
    
    # Add state information
    plt.text(3, 2, 'State passed between nodes:\n{\n  messages: List[Message]\n}',
            ha='center', va='top', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow'))
    
    # Add agent details
    plt.text(2, 0, 'Supervisor contains:\n• Research Agent\n• Memory Agent',
            ha='center', va='top', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray'))
    
    plt.xlim(-1, 7)
    plt.ylim(-0.5, 2.5)
    plt.axis('off')
    plt.title('LangGraph Implementation Flow', fontsize=16, weight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('langgraph_conceptual_flow.png', dpi=300, bbox_inches='tight')
    print("✅ Saved conceptual graph as langgraph_conceptual_flow.png")

def create_supervisor_detail():
    """Create a detailed view of the supervisor agent"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Supervisor Agent Internal Structure', 
            fontsize=18, weight='bold', ha='center')
    
    # Main supervisor box
    supervisor_box = FancyBboxPatch((1, 3), 8, 5,
                                    boxstyle="round,pad=0.2",
                                    facecolor='lightcoral',
                                    edgecolor='black',
                                    linewidth=3,
                                    alpha=0.3)
    ax.add_patch(supervisor_box)
    ax.text(5, 7.5, 'Supervisor Agent (GPT-4o)', fontsize=14, weight='bold', ha='center')
    
    # Research agent box
    research_box = FancyBboxPatch((1.5, 5), 3, 1.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor='lightgreen',
                                  edgecolor='black',
                                  linewidth=2)
    ax.add_patch(research_box)
    ax.text(3, 5.75, 'Research Agent\n(GPT-4.1-mini)', ha='center', va='center', fontsize=11)
    
    # Memory agent box
    memory_box = FancyBboxPatch((5.5, 5), 3, 1.5,
                               boxstyle="round,pad=0.1",
                               facecolor='lightblue',
                               edgecolor='black',
                               linewidth=2)
    ax.add_patch(memory_box)
    ax.text(7, 5.75, 'Memory Agent\n(GPT-4.1-mini)', ha='center', va='center', fontsize=11)
    
    # Tools
    ax.text(3, 4.5, 'Tools:\n• web_search\n• search_pinecone', 
            ha='center', va='top', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='lightyellow'))
    
    ax.text(7, 4.5, 'Tools:\n• get_from_memory', 
            ha='center', va='top', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='lightyellow'))
    
    # Prompt info
    ax.text(5, 3.5, 'Supervisor Prompt:\nEmotion detection + Routing logic', 
            ha='center', fontsize=10, style='italic')
    
    # Input/Output
    ax.text(5, 2, 'Input: User Message → Emotion Analysis → Agent Selection → Output: Response',
            ha='center', fontsize=11,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray'))
    
    # Emotion examples
    ax.text(1, 1, 'Negative Emotions:\n"overwhelmed", "sad", "anxious"\n↓\n"I\'m here for you..."',
            fontsize=9, va='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#ffcccc'))
    
    ax.text(9, 1, 'Positive Emotions:\n"proud", "excited", "happy"\n↓\n"That\'s wonderful..."',
            fontsize=9, va='top', ha='right',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#ccffcc'))
    
    plt.tight_layout()
    plt.savefig('supervisor_agent_detail.png', dpi=300, bbox_inches='tight')
    print("✅ Saved supervisor detail as supervisor_agent_detail.png")

if __name__ == "__main__":
    print("🎨 Generating LangGraph visualizations...")
    
    # Try to visualize actual graph
    # asyncio.run(visualize_actual_graph())
    
    # Create conceptual graph
    create_conceptual_graph()
    
    # Create supervisor detail
    create_supervisor_detail()
    
    print("✨ Done! Check the generated PNG files.")