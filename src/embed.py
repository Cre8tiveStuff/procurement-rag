import json
from pathlib import Path
from sentence_transformers import SentenceTransformer


def generate_embeddings(chunks: list[dict], model_name: str = "all-MiniLM-L6-v2") -> list[dict]:
    """Generates dense vector embeddings for text chunks using SentenceTransformer on CPU."""
    print(f"Loading embedding model '{model_name}' on CPU...")
    # Explicitly force device='cpu' to prevent CUDA compatibility errors
    model = SentenceTransformer(model_name, device="cpu")

    texts = [chunk.get("text", "") for chunk in chunks]
    
    if not texts:
        print("No text content found to embed.")
        return []

    print(f"Generating embeddings for {len(texts)} chunk(s)...")
    embeddings = model.encode(texts, show_progress_bar=True)

    embedded_chunks = []
    for idx, chunk in enumerate(chunks):
        # Convert numpy array to standard Python list for JSON serialization
        vector_list = embeddings[idx].tolist()
        
        chunk_record = chunk.copy()
        chunk_record["embedding"] = vector_list
        chunk_record["embedding_dimension"] = len(vector_list)
        chunk_record["model_used"] = model_name
        embedded_chunks.append(chunk_record)

    return embedded_chunks


def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    input_file = data_dir / "chunked_contracts.json"
    output_file = data_dir / "embedded_contracts.json"

    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        print("Please run scripts/02_chunk_documents.py first.")
        return

    print("Loading chunked contracts...")
    with open(input_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embedded_chunks = generate_embeddings(chunks)

    if embedded_chunks:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(embedded_chunks, f, indent=2)

        sample_dim = embedded_chunks[0]["embedding_dimension"]
        print(f"\nSuccessfully generated vectors (Dimension: {sample_dim}) -> {output_file}")


if __name__ == "__main__":
    main()