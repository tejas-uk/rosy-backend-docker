import os
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME") or None
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL") or None
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY") or None

if not INDEX_NAME:
    raise NotImplementedError("PINECONE_INDEX_NAME, EMBEDDING_MODEL, or PINECONE_API_KEY is not set")

if not EMBEDDING_MODEL:
    raise NotImplementedError("EMBEDDING_MODEL is not set")

if not PINECONE_API_KEY:
    raise NotImplementedError("PINECONE_API_KEY is not set")


vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=OpenAIEmbeddings(model=EMBEDDING_MODEL),
    pinecone_api_key=PINECONE_API_KEY,
)

vectorstore_retriever = vectorstore.as_retriever(search_type="similarity")

@tool
def search_pinecone(query: str, k: int = 5) -> str:
    """Search the Pinecone index for the most relevant documents."""
    try:
        docs = vectorstore_retriever.invoke(query, search_kwargs={"k": k})
        return "\n\n".join(doc.page_content for doc in docs) if docs else "No books found"
    except Exception as e:
        return f"Retrieval Error: {str(e)}"
