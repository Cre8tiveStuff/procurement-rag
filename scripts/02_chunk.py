import os
import glob
import pandas as pd

def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)
        if end >= len(words):
            break
        start += (chunk_size - overlap)
    return chunks

def process_chunks():
    processed_dir = "data/processed"
    chunks_dir = "data/chunks"
    os.makedirs(chunks_dir, exist_ok=True)
    
    txt_files = glob.glob(os.path.join(processed_dir, "*.txt"))
    all_chunks = []
    
    for txt_path in txt_files:
        doc_id = os.path.basename(txt_path).replace(".txt", "")
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        chunks = chunk_text(text)
        
        for idx, chunk_content in enumerate(chunks):
            chunk_id = f"{doc_id}_chunk_{idx+1}"
            all_chunks.append({
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "chunk_index": idx + 1,
                "content": chunk_content
            })
            
    df = pd.DataFrame(all_chunks)
    df.to_csv("data/chunks/chunks_manifest.csv", index=False)
    print(f"Created {len(all_chunks)} chunks from {len(txt_files)} documents.")

if __name__ == "__main__":
    process_chunks()