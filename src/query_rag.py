from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


def query_vector_store(
    query_text: str,
    db_dir: Path,
    collection_name: str = "procurement_contracts",
    model_name: str = "all-MiniLM-L6-v2",
    top_k: int = 2
) -> list[dict]:
    """Embeds a query string, searches ChromaDB, and returns top matching context documents."""
    print(f"Loading embedding model '{model_name}' on CPU...")
    embedding_model = SentenceTransformer(model_name, device="cpu")

    print(f"Generating query embedding for: '{query_text}'")
    query_vector = embedding_model.encode([query_text])[0].tolist()

    print(f"Connecting to ChromaDB at: {db_dir}")
    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_collection(name=collection_name)

    print(f"Querying vector store (top_k={top_k})...\n")
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )

    retrieved_chunks = []
    if results and "documents" in results and results["documents"]:
        for i in range(len(results["ids"][0])):
            chunk_data = {
                "chunk_id": results["ids"][0][i],
                "document_text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i] if "metadatas" in results else {},
                "distance": results["distances"][0][i] if "distances" in results else None
            }
            retrieved_chunks.append(chunk_data)

    return retrieved_chunks


def curate_chunks(chunks: list[dict], max_tokens: int = 2000) -> list[dict]:
    """Prunes retrieved chunks to a real token budget, then reorders survivors
    so the most relevant sit first and last, exploiting the model's
    stronger attention at the start and end of its context window."""
    from ccl import count_tokens, position_aware_order

    selected = []
    used = 0
    for chunk in chunks:
        cost = count_tokens(chunk["document_text"])
        if used + cost > max_tokens:
            break
        selected.append(chunk)
        used += cost

    return position_aware_order(selected)


def format_rag_prompt(query_text: str, retrieved_chunks: list[dict]) -> str:
    """Formats retrieved context and user query into a clean prompt for an LLM."""
    context_blocks = []
    for idx, item in enumerate(retrieved_chunks, 1):
        context_blocks.append(
            f"--- Context Block {idx} (ID: {item['chunk_id']}) ---\n"
            f"{item['document_text']}"
        )

    context_str = "\n\n".join(context_blocks)

    prompt = (
        "You are an AI assistant analyzing procurement contracts.\n"
        "Answer the user's question relying strictly on the context provided below.\n\n"
        f"CONTEXT:\n{context_str}\n\n"
        f"QUESTION: {query_text}\n\n"
        "ANSWER:"
    )
    return prompt


def main():
    base_dir = Path(__file__).resolve().parent.parent
    chroma_db_dir = base_dir / "data" / "chroma_db"

    if not chroma_db_dir.exists():
        print(f"Vector store directory not found: {chroma_db_dir}")
        print("Please run scripts/04_vector_store.py first.")
        return

    user_query = "What is the delivery timeline agreed upon by Supplier Inc?"

    retrieved_chunks = query_vector_store(
        query_text=user_query,
        db_dir=chroma_db_dir,
        top_k=2
    )

    curated_chunks = curate_chunks(retrieved_chunks)

    print(f"=== RETRIEVED {len(retrieved_chunks)} MATCHES, CURATED TO {len(curated_chunks)} ===")
    for idx, match in enumerate(curated_chunks, 1):
        print(f"\nMatch {idx} [Distance: {match['distance']:.4f}]")
        print(f"Source Doc: {match['metadata'].get('file_name', 'N/A')}")
        print(f"Text: {match['document_text']}")

    print("\n" + "=" * 50)
    print("=== CONSTRUCTED RAG PROMPT ===")
    print("=" * 50)
    rag_prompt = format_rag_prompt(user_query, curated_chunks)
    print(rag_prompt)


if __name__ == "__main__":
    main()