import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os

def generate_embeddings():
    chunks_path = "data/chunks/chunks_manifest.csv"
    output_dir = "data/embeddings"
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(chunks_path):
        print("Error: chunks_manifest.csv not found.")
        return

    df = pd.read_csv(chunks_path)
    
    print("Loading local embedding model (all-MiniLM-L6-v2) on CPU...")
    # Force device='cpu' to prevent PyTorch CUDA driver errors
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    
    print(f"Generating embeddings for {len(df)} chunks...")
    embeddings = model.encode(df["content"].tolist(), show_progress_bar=True)
    
    # Save vector embeddings matrix and metadata
    np.save(os.path.join(output_dir, "embeddings.npy"), embeddings)
    df.to_csv(os.path.join(output_dir, "metadata.csv"), index=False)
    
    print(f"Successfully generated embeddings matrix of shape: {embeddings.shape}")

if __name__ == "__main__":
    generate_embeddings()