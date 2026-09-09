import json
from pathlib import Path
import chromadb


def build_vector_store(embedded_chunks: list[dict], db_dir: Path, collection_name: str = "procurement_contracts"):
    """Stores embedded chunk vectors and metadata into a persistent ChromaDB database."""
    print(f"Initializing ChromaDB client at: {db_dir}")
    client = chromadb.PersistentClient(path=str(db_dir))

    # Get or create the vector collection
    collection = client.get_or_create_collection(name=collection_name)

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for chunk in embedded_chunks:
        ids.append(chunk["chunk_id"])
        embeddings.append(chunk["embedding"])
        documents.append(chunk["text"])
        metadatas.append({
            "doc_id": chunk.get("doc_id", ""),
            "file_name": chunk.get("file_name", ""),
            "chunk_index": chunk.get("chunk_index", 0),
            "model_used": chunk.get("model_used", "")
        })

    print(f"Upserting {len(ids)} record(s) into collection '{collection_name}'...")
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Collection count: {collection.count()} item(s)")
    return collection


def test_query(collection, query_vector: list[float], top_k: int = 1):
    """Executes a sample vector query to verify database retrieval."""
    print(f"\nTesting vector retrieval (top_k={top_k})...")
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )
    
    for i in range(len(results["ids"][0])):
        chunk_id = results["ids"][0][i]
        doc_text = results["documents"][0][i]
        distance = results["distances"][0][i] if "distances" in results else "N/A"
        print(f"Result {i + 1}: ID={chunk_id} | Distance={distance}")
        print(f"Snippet: {doc_text}")


def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    input_file = data_dir / "embedded_contracts.json"
    chroma_db_dir = data_dir / "chroma_db"

    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        print("Please run scripts/03_generate_embeddings.py first.")
        return

    print("Loading embedded contracts...")
    with open(input_file, "r", encoding="utf-8") as f:
        embedded_chunks = json.load(f)

    collection = build_vector_store(embedded_chunks, db_dir=chroma_db_dir)

    # Perform a test search using the first record's vector
    if embedded_chunks:
        test_vector = embedded_chunks[0]["embedding"]
        test_query(collection, query_vector=test_vector)


if __name__ == "__main__":
    main()