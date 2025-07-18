from fastapi import FastAPI
import os
from contextlib import asynccontextmanager
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from api.db import init_db
from api.chat.routing import router as chat_router
from api.auth.routing import router as auth_router
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before the app starts
    init_db()
    # After the app starts
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(chat_router)
app.include_router(auth_router)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_index():
    return {"message": "Hello, Tej!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}



async def run_agent():
    from ai.graph import get_agent
    from langchain_core.messages import HumanMessage, AIMessage
    

    agent = await get_agent()
    # agent = get_supervisor_agent()
    config = {"configurable": {"thread_id": 2}, "user_id": 2}
    while True:
        query = input("⛄️ You: ")

        if query.lower() == "exit":
            break

        inputs = [HumanMessage(content=query)]
        response = await agent.ainvoke({"messages": inputs}, config)
        # response = agent.invoke({"messages": inputs}, config)
        # Get the last message from the result
        # print("-"*60)
        # print(response)
        # print("-"*60)
        last_message = next((m for m in reversed(response["messages"])
                            if isinstance(m, AIMessage)), None)
    
        if last_message:
            print(f"🧚‍♂️ Rosy: {last_message.content}")
        else:
            print("🧚‍♂️ Rosy: No response from the agent.")


if __name__ == "__main__":
    asyncio.run(run_agent())