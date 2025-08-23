#!/usr/bin/env python3
"""
Visualization script for Rosy AI's multi-agent architecture
Generates a graph diagram showing the agent flow and communication patterns
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import networkx as nx

def create_architecture_diagram():
    """Create a visual representation of the multi-agent architecture"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define colors
    colors = {
        'supervisor': '#FF6B6B',
        'research': '#4ECDC4',
        'memory': '#45B7D1',
        'memory_store': '#FFA07A',
        'api': '#98D8C8',
        'user': '#F7DC6F',
        'tools': '#DDA0DD'
    }
    
    # Title
    ax.text(5, 9.5, 'Rosy AI: Multi-Agent Architecture', 
            fontsize=20, weight='bold', ha='center')
    ax.text(5, 9.1, 'LangGraph Supervisor Pattern with Emotional Context Engineering', 
            fontsize=12, ha='center', style='italic')
    
    # User/API Layer
    user_box = FancyBboxPatch((0.5, 7.5), 2, 1, 
                               boxstyle="round,pad=0.1",
                               facecolor=colors['user'],
                               edgecolor='black',
                               linewidth=2)
    ax.add_patch(user_box)
    ax.text(1.5, 8, 'User\n(Parent)', ha='center', va='center', fontsize=10, weight='bold')
    
    api_box = FancyBboxPatch((3, 7.5), 2.5, 1,
                             boxstyle="round,pad=0.1",
                             facecolor=colors['api'],
                             edgecolor='black',
                             linewidth=2)
    ax.add_patch(api_box)
    ax.text(4.25, 8, 'FastAPI\nEndpoints', ha='center', va='center', fontsize=10, weight='bold')
    
    # Supervisor Agent
    supervisor_box = FancyBboxPatch((3.5, 5), 3, 1.5,
                                    boxstyle="round,pad=0.15",
                                    facecolor=colors['supervisor'],
                                    edgecolor='black',
                                    linewidth=3)
    ax.add_patch(supervisor_box)
    ax.text(5, 5.75, 'Supervisor Agent\n(GPT-4o)', ha='center', va='center', 
            fontsize=11, weight='bold')
    ax.text(5, 5.3, 'Emotion Detection\nAgent Routing', ha='center', va='center', 
            fontsize=8, style='italic')
    
    # Research Agent
    research_box = FancyBboxPatch((0.5, 2.5), 2.5, 1.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor=colors['research'],
                                  edgecolor='black',
                                  linewidth=2)
    ax.add_patch(research_box)
    ax.text(1.75, 3.25, 'Research Agent\n(GPT-4.1-mini)', ha='center', va='center', 
            fontsize=10, weight='bold')
    
    # Memory Agent  
    memory_box = FancyBboxPatch((7, 2.5), 2.5, 1.5,
                                boxstyle="round,pad=0.1",
                                facecolor=colors['memory'],
                                edgecolor='black',
                                linewidth=2)
    ax.add_patch(memory_box)
    ax.text(8.25, 3.25, 'Memory Agent\n(GPT-4.1-mini)', ha='center', va='center', 
            fontsize=10, weight='bold')
    
    # Tools for Research Agent
    tavily_box = FancyBboxPatch((0.2, 0.8), 1.5, 0.8,
                                boxstyle="round,pad=0.05",
                                facecolor=colors['tools'],
                                edgecolor='black',
                                linewidth=1)
    ax.add_patch(tavily_box)
    ax.text(0.95, 1.2, 'Tavily\nWeb Search', ha='center', va='center', fontsize=8)
    
    pinecone_box = FancyBboxPatch((2, 0.8), 1.5, 0.8,
                                   boxstyle="round,pad=0.05",
                                   facecolor=colors['tools'],
                                   edgecolor='black',
                                   linewidth=1)
    ax.add_patch(pinecone_box)
    ax.text(2.75, 1.2, 'Pinecone\nVector DB', ha='center', va='center', fontsize=8)
    
    # Memory Store
    mem0_box = FancyBboxPatch((6.5, 0.5), 3.5, 1.2,
                              boxstyle="round,pad=0.1",
                              facecolor=colors['memory_store'],
                              edgecolor='black',
                              linewidth=2)
    ax.add_patch(mem0_box)
    ax.text(8.25, 1.1, 'Mem0 Memory Layer', ha='center', va='center', 
            fontsize=10, weight='bold')
    ax.text(8.25, 0.7, 'Vector + KV + Graph DB', ha='center', va='center', 
            fontsize=8, style='italic')
    
    # Add connections with arrows
    # User to API
    ax.annotate('', xy=(3, 8), xytext=(2.5, 8),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    # API to Supervisor
    ax.annotate('', xy=(5, 6.5), xytext=(4.25, 7.5),
                arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
    
    # Supervisor to Research Agent
    ax.annotate('', xy=(2.5, 4), xytext=(4, 5),
                arrowprops=dict(arrowstyle='<->', lw=2, color='blue', 
                               connectionstyle="arc3,rad=0.3"))
    ax.text(2.5, 4.5, 'Handoff', ha='center', fontsize=8, color='blue')
    
    # Supervisor to Memory Agent
    ax.annotate('', xy=(7.5, 4), xytext=(6, 5),
                arrowprops=dict(arrowstyle='<->', lw=2, color='blue',
                               connectionstyle="arc3,rad=-0.3"))
    ax.text(7.5, 4.5, 'Handoff', ha='center', fontsize=8, color='blue')
    
    # Research Agent to Tools
    ax.annotate('', xy=(0.95, 1.6), xytext=(1.25, 2.5),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='purple'))
    ax.annotate('', xy=(2.75, 1.6), xytext=(2.25, 2.5),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='purple'))
    
    # Memory Agent to Mem0
    ax.annotate('', xy=(8.25, 1.7), xytext=(8.25, 2.5),
                arrowprops=dict(arrowstyle='<->', lw=2, color='orange'))
    
    # Add State Flow indicator
    state_flow_box = FancyBboxPatch((4, 1.8), 2, 0.8,
                                    boxstyle="round,pad=0.05",
                                    facecolor='lightgray',
                                    edgecolor='black',
                                    linewidth=1,
                                    alpha=0.7)
    ax.add_patch(state_flow_box)
    ax.text(5, 2.2, 'Shared State', ha='center', va='center', fontsize=9, weight='bold')
    ax.text(5, 1.95, '(AgentState)', ha='center', va='center', fontsize=8, style='italic')
    
    
    plt.tight_layout()
    return fig

def create_state_flow_diagram():
    """Create a diagram showing the state flow through the system"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'LangGraph State Flow', fontsize=18, weight='bold', ha='center')
    
    # Define nodes
    nodes = {
        'START': (1, 7),
        'Supervisor': (3, 7),
        'Research': (2, 4),
        'Memory': (4, 4),
        'Memory Node': (5, 7),
        'END': (7, 7)
    }
    
    # Draw nodes
    for node, (x, y) in nodes.items():
        if node in ['START', 'END']:
            circle = plt.Circle((x, y), 0.4, facecolor='lightgray', 
                               edgecolor='black', linewidth=2)
        else:
            circle = plt.Circle((x, y), 0.6, facecolor='lightblue', 
                               edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, node, ha='center', va='center', fontsize=10, weight='bold')
    
    # Draw edges
    edges = [
        ('START', 'Supervisor', 'straight'),
        ('Supervisor', 'Research', 'arc'),
        ('Supervisor', 'Memory', 'arc'),
        ('Research', 'Memory Node', 'arc'),
        ('Memory', 'Memory Node', 'arc'),
        ('Memory Node', 'END', 'straight')
    ]
    
    for start, end, style in edges:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]
        
        if style == 'straight':
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        else:
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black',
                                     connectionstyle="arc3,rad=0.3"))
    
    # Add state information
    ax.text(5, 2, 'State Schema:\n{\n  messages: List[Message],\n  user_id: int,\n  thread_id: int\n}',
            fontsize=10, ha='center', bbox=dict(boxstyle="round,pad=0.5", 
                                               facecolor='lightyellow'))
    
    # Add checkpointing info
    ax.text(8.5, 5, 'PostgreSQL\nCheckpointing',
            fontsize=10, ha='center', bbox=dict(boxstyle="round,pad=0.3", 
                                               facecolor='lightgreen'))
    ax.annotate('', xy=(7.5, 5), xytext=(8, 5),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='green'))
    
    plt.tight_layout()
    return fig

def save_diagrams():
    """Generate and save both diagrams"""
    # Create architecture diagram
    fig1 = create_architecture_diagram()
    fig1.savefig('rosy_architecture_diagram.png', dpi=300, bbox_inches='tight')
    fig1.savefig('rosy_architecture_diagram.pdf', bbox_inches='tight')
    print("✅ Saved architecture diagram as rosy_architecture_diagram.png and .pdf")
    
    # Create state flow diagram
    fig2 = create_state_flow_diagram()
    fig2.savefig('rosy_state_flow_diagram.png', dpi=300, bbox_inches='tight')
    fig2.savefig('rosy_state_flow_diagram.pdf', bbox_inches='tight')
    print("✅ Saved state flow diagram as rosy_state_flow_diagram.png and .pdf")
    
    # Show diagrams
    plt.show()

if __name__ == "__main__":
    print("🎨 Generating Rosy AI architecture visualizations...")
    save_diagrams()
    print("✨ Done! Check the generated PNG and PDF files.")