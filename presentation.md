# Rosy AI: Multi-Agent Architecture for Empathetic Parenting Support
Check out app at [userosy.ai](https://userosy.ai/)

---

## Slide 1: System Overview - The Rosy AI Support Companion
### Context Engineering Framework: Hierarchical Multi-Agent Architecture

**Product Vision**: Empathetic AI support companion for new parents

**Core Architecture**: LangGraph Supervisor Pattern with specialized agents
- **Supervisor Agent (GPT-4o)**: Orchestrates and manages emotional context
- **Research Agent (GPT-4.1-mini)**: Web search via Tavily + Pinecone vector DB for parenting knowledge
- **Memory Agent (GPT-4.1-mini)**: Persistent context via Mem0 for personalized interactions

**Tech Stack**: 
- Backend: FastAPI + SQLModel + PostgreSQL
- AI Framework: LangGraph + LangChain
- Memory: Mem0 + Pinecone
- Deployment: Docker + Railway

**Key Differentiator**: Context-aware emotional intelligence with persistent memory across sessions

---

## Slide 2: Context Engineering Strategy - Building Empathy at Scale
### Framework: Write-Select-Compress-Isolate Pattern

**Write: Prompt Engineering for Emotional Intelligence**
- Emotion keyword detection (overwhelmed, scared, proud, excited)
- Contextual response templates with empathetic prefixes
- Negative emotions → "I'm here for you, and you're doing your best."
- Positive emotions → "That's wonderful—congratulations!"

**Select: Dynamic Agent Routing**
- Supervisor analyzes query intent and emotional content
- Routes to Memory Agent for personalized historical context
- Routes to Research Agent for factual parenting information

**Compress: Efficient Context Management**
- Mem0's two-phase pipeline (Extract → Update)
- 90% token cost reduction while maintaining context fidelity
- Intelligent summarization of long conversations

**Isolate: Clean Context Windows**
- Each agent receives only relevant context via handoffs
- No cross-contamination between agent contexts
- Tool-based communication prevents direct agent-to-agent chatter

---

## Slide 3: Memory Architecture - Persistent Personalization
### Mem0 Integration: Scalable Long-Term Memory

**Hybrid Storage System**:
- **Vector DB**: Semantic similarity for context retrieval
  - OpenAI embeddings for memory vectorization
  - Efficient similarity search for relevant memories
- **Key-Value Store**: Structured user preferences
  - User-specific settings and preferences
  - Quick access to frequently used data
- **Graph DB** (future): Relationship mapping between memories
  - Track evolution of parenting journey
  - Connect related experiences and milestones

**Memory Pipeline**:
1. **Extraction Phase**: 
   - Analyze latest exchange + rolling summary + recent messages
   - Extract candidate memories using LLM
2. **Update Phase**:
   - Deduplicate against existing memories
   - Merge or update related memories
   - Store with user_id association

**Performance Metrics**:
- 26% higher response accuracy than OpenAI Memory
- 91% lower p95 latency
- 90%+ token cost savings vs full-context approach

---

## Slide 4: Agent Orchestration - Supervisor Pattern Implementation
### LangGraph State Management & Communication Flow

**State Graph Architecture**:
```
START → Supervisor Agent → [Research Agent | Memory Agent] → Memory Node → END
         ↑                            ↓
         └────── State Updates ───────┘
```

**Supervisor Responsibilities**:
- **Emotional Context Detection**: Analyze user messages for emotional cues
- **Agent Delegation**: Route to appropriate specialist agent
- **Response Synthesis**: Combine agent outputs into empathetic response
- **State Management**: Maintain conversation flow and context

**Communication Protocol**:
- **Shared State**: AgentState schema with messages array
- **Tool-Based Handoffs**: No direct agent communication
- **Checkpointing**: PostgreSQL-based state persistence
- **Thread Management**: Unique thread_id per conversation

**API Integration**:
- RESTful endpoints: `/api/chats/*`
- WebSocket support for real-time responses
- JWT-based authentication
- Rate limiting and error handling

---

## Slide 5: Production Considerations & Scaling Strategy
### Enterprise-Ready Architecture

**Security & Compliance**:
- **Data Privacy**: SOC 2 & HIPAA compliant memory layer (Mem0)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Environment Management**: Secure .env configuration
- **API Security**: CORS configuration, rate limiting

**Scalability Features**:
- **Microservices**: Dockerized components for independent scaling
- **Async Processing**: FastAPI with uvicorn for high concurrency
- **Database**: PostgreSQL with connection pooling
- **Caching**: 15-minute memory cache for frequent queries

**Cost Optimization**:
- **Model Selection**: GPT-4o for supervisor, GPT-4.1-mini for agents
- **Context Compression**: Mem0 reduces tokens by 90%
- **Intelligent Routing**: Only activate necessary agents
- **Batch Processing**: Efficient memory updates

**Monitoring & Observability**:
- Health check endpoints
- Structured logging
- Error tracking
- Performance metrics collection

---

## Slide 6: 3H Evaluation Framework - Contextual Metrics for Rosy AI
### Applying Anthropic's Helpful, Harmless, Honest Framework

**Helpful Metrics** 🎯
- **Task Completion Rate**: % of parenting questions answered satisfactorily
  - Dataset curated using SME from a pediatrician
  - Target: >90% for emotional support
- **Information Retrieval Relevance**: Semantic similarity between query and information retrieved
  - Measured via embedding distance
- **Personalization Score**: % of responses utilizing user memory
  - Target: >70% for returning users
  - Track memory recall accuracy

**Harmless Metrics** 🛡️
- **Safety Filter Pass Rate**: % responses passing content moderation
  - No medical advice that hasn't been vetted
- **Emotional Harm Prevention**: 
  - Never dismiss parental concerns
  - Always validate emotions before advice
  - Crisis detection and escalation protocols
- **Privacy Protection Score**: 
  - Zero PII leakage in responses
  - Compliance with data retention policies

**Honest Metrics** 🔍
- **Factual Accuracy**: Verification against medical/parenting databases
  - Pinecone knowledge base accuracy
- **Uncertainty Expression**: Clear communication of limitations
  - "I don't know" rate tracking
  - Confidence calibration scores
- **Consistency Check**: Cross-session response alignment
  - Memory consistency score
  - No contradictory advice tracking

**Rosy-Specific Evaluation Metrics**:
- **Emotional Intelligence Score**: 
  - Correct emotion detection rate: >95%
  - Appropriate empathetic response: >90%
- **Context Retention**: 
  - Multi-turn conversation coherence
  - Long-term memory utilization rate
- **Parent Satisfaction Score**: 
  - User feedback ratings
  - Conversation completion rate
  - Return user percentage

**Evaluation Pipeline**:
1. **Automated Testing**: Unit tests for each agent
2. **Human Evaluation**: Sample conversations reviewed by parenting experts
3. **A/B Testing**: Compare supervisor routing strategies
4. **Production Monitoring**: Real-time metric dashboards