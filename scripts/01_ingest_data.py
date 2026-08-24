import json
import os
from pathlib import Path


def load_txt_files(data_dir: Path) -> list[dict]:
    """Reads all raw text files from the data directory."""
    documents = []
    
    if not data_dir.exists():
        print(f"Directory {data_dir} does not exist.")
        return documents

    for filepath in data_dir.glob("*.txt"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    documents.append({
                        "doc_id": filepath.stem,
                        "file_name": filepath.name,
                        "text": content
                    })
                    print(f"Loaded: {filepath.name}")
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")

    return documents


def save_ingested_data(documents: list[dict], output_path: Path) -> None:
    """Saves loaded documents into a clean JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2)
    print(f"\nSuccessfully ingested {len(documents)} document(s) -> {output_path}")


def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    output_file = data_dir / "ingested_contracts.json"

    print("Starting data ingestion...")
    docs = load_txt_files(data_dir)
    
    if docs:
        save_ingested_data(docs, output_file)
    else:
        print("No .txt contract files found in data/ directory. Add sample files and rerun.")


if __name__ == "__main__":
    main()