import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import sys

def search_contracts(query, top_k=2):
    embeddings_path = "data/embeddings/embeddings.npy"
    metadata_path = "data/embeddings/metadata.csv"

    if not os.path.exists(embeddings_path) or not os.path.exists(metadata_path):
        print("Error: Embeddings or metadata not found. Run 03_embed.py first.")
        return

    embeddings = np.load(embeddings_path)
    df = pd.read_csv(metadata_path)

    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

    # Generate vector embedding for the search query
    query_embedding = model.encode([query])

    # Compute Cosine Similarity between query vector and chunk vectors
    norm_query = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
    norm_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    scores = np.dot(norm_query, norm_embeddings.T)[0]

    # Rank indices by highest similarity score
    top_indices = np.argsort(scores)[::-1][:top_k]

    print(f"\n--- Top Results for Query: '{query}' ---")
    for idx in top_indices:
        print(f"Score: {scores[idx]:.4f} | Chunk ID: {df.iloc[idx]['chunk_id']}")
        print(f"Content: {df.iloc[idx]['content']}\n")

if __name__ == "__main__":
    user_query = sys.argv[1] if len(sys.argv) > 1 else "What are the escalation caps?"
    search_contracts(user_query)