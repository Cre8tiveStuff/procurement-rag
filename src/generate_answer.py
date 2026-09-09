import importlib.util
from pathlib import Path
import ollama

# Dynamically import 05_query_rag.py (bypasses module name syntax errors)
script_path = Path(__file__).resolve().parent / "05_query_rag.py"
spec = importlib.util.spec_from_file_location("query_rag", script_path)
query_rag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query_rag)

query_vector_store = query_rag.query_vector_store
format_rag_prompt = query_rag.format_rag_prompt


def generate_answer(prompt: str, model_name: str = "llama3.2") -> str:
    """Sends the formatted RAG prompt to a local Ollama model and returns the answer."""
    print(f"Sending prompt to local Ollama model ('{model_name}')...\n")
    
    response = ollama.generate(
        model=model_name,
        prompt=prompt
    )
    
    return response.get("response", "")


def main():
    base_dir = Path(__file__).resolve().parent.parent
    chroma_db_dir = base_dir / "data" / "chroma_db"

    if not chroma_db_dir.exists():
        print(f"Vector store directory not found: {chroma_db_dir}")
        print("Please run scripts/04_vector_store.py first.")
        return

    user_query = "What is the delivery timeline agreed upon by Supplier Inc?"

    # 1. Retrieve context
    retrieved_chunks = query_vector_store(
        query_text=user_query,
        db_dir=chroma_db_dir,
        top_k=2
    )

    if not retrieved_chunks:
        print("No relevant context found in the vector store.")
        return

    # 2. Build prompt
    rag_prompt = format_rag_prompt(user_query, retrieved_chunks)

    # 3. Generate answer via local Ollama instance
    try:
        answer = generate_answer(rag_prompt, model_name="llama3.2")
        
        print("=" * 50)
        print("=== FINAL GENERATED ANSWER ===")
        print("=" * 50)
        print(answer)
        
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        print("Ensure the Ollama service is running and the model is pulled (`ollama pull llama3.2`).")


if __name__ == "__main__":
    main()