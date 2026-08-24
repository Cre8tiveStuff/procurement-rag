import json
from pathlib import Path


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Splits text into chunks by word count with specified overlap."""
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_str = " ".join(chunk_words)
        chunks.append(chunk_str)
        
        # Advance position by chunk size minus overlap
        start += chunk_size - overlap
        
        # Prevent infinite loops if parameters are misconfigured
        if chunk_size <= overlap:
            break

    return chunks


def process_chunks(ingested_docs: list[dict], chunk_size: int, overlap: int) -> list[dict]:
    """Iterates over documents and creates structured chunk records."""
    all_chunks = []

    for doc in ingested_docs:
        doc_id = doc.get("doc_id", "unknown")
        file_name = doc.get("file_name", "unknown")
        raw_text = doc.get("text", "")

        text_chunks = chunk_text(raw_text, chunk_size=chunk_size, overlap=overlap)

        for idx, chunk_content in enumerate(text_chunks):
            all_chunks.append({
                "chunk_id": f"{doc_id}_chunk_{idx + 1}",
                "doc_id": doc_id,
                "file_name": file_name,
                "chunk_index": idx + 1,
                "text": chunk_content
            })

    return all_chunks


def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    input_file = data_dir / "ingested_contracts.json"
    output_file = data_dir / "chunked_contracts.json"

    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        print("Please run scripts/01_ingest_data.py first.")
        return

    print("Loading ingested contracts...")
    with open(input_file, "r", encoding="utf-8") as f:
        ingested_docs = json.load(f)

    print(f"Processing {len(ingested_docs)} document(s)...")
    chunks = process_chunks(ingested_docs, chunk_size=100, overlap=20)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"Successfully generated {len(chunks)} total chunk(s) -> {output_file}")


if __name__ == "__main__":
    main()