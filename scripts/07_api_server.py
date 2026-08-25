import importlib.util
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama

# Dynamically import 05_query_rag.py for retrieval logic
script_path = Path(__file__).resolve().parent / "05_query_rag.py"
spec = importlib.util.spec_from_file_location("query_rag", script_path)
query_rag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query_rag)

query_vector_store = query_rag.query_vector_store
format_rag_prompt = query_rag.format_rag_prompt

app = FastAPI(
    title="Procurement RAG API",
    description="Lightweight API service for querying procurement contracts locally via ChromaDB and Ollama.",
    version="1.0.0"
)

base_dir = Path(__file__).resolve().parent.parent
chroma_db_dir = base_dir / "data" / "chroma_db"

class QueryRequest(BaseModel):
    query: str
    top_k: int = 2
    model_name: str = "llama3.2"

class QueryResponse(BaseModel):
    query: str
    answer: str
    retrieved_chunks: list

@app.get("/")
def health_check():
    """Health check endpoint to verify API state."""
    return {"status": "ok", "message": "Procurement RAG API is running"}

@app.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    """Retrieves relevant contract context and returns a grounded answer from Ollama."""
    if not chroma_db_dir.exists():
        raise HTTPException(
            status_code=500, 
            detail=f"Vector store not found at {chroma_db_dir}. Run script 04 first."
        )

    # 1. Retrieve context
    retrieved_chunks = query_vector_store(
        query_text=request.query,
        db_dir=chroma_db_dir,
        top_k=request.top_k
    )

    if not retrieved_chunks:
        raise HTTPException(status_code=404, detail="No relevant context found in vector store.")

    # 2. Build prompt
    rag_prompt = format_rag_prompt(request.query, retrieved_chunks)

    # 3. Generate answer locally via Ollama
    try:
        response = ollama.generate(
            model=request.model_name,
            prompt=rag_prompt
        )
        answer = response.get("response", "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama inference error: {str(e)}")

    return QueryResponse(
        query=request.query,
        answer=answer,
        retrieved_chunks=retrieved_chunks
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)