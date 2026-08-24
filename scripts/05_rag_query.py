import os
import sys
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from google import genai

def retrieve_chunks(query, top_k=2):
    embeddings = np.load("data/embeddings/embeddings.npy")
    df = pd.read_csv("data/embeddings/metadata.csv")
    
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    query_embedding = model.encode([query])
    
    norm_query = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
    norm_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    
    scores = np.dot(norm_query, norm_embeddings.T)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]
    
    retrieved_texts = []
    for idx in top_indices:
        retrieved_texts.append(f"[{df.iloc[idx]['chunk_id']}]: {df.iloc[idx]['content']}")
        
    return "\n".join(retrieved_texts)

def run_rag(query):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        return

    print("Retrieving context from vector store...")
    context = retrieve_chunks(query)
    
    prompt = f"""You are a Procurement Analyst AI. Answer the question using ONLY the provided contract context. If the answer is not in the context, say "Data not found in contracts."

Retrieved Context:
{context}

Question: {query}
Answer:"""

    client = genai.Client(api_key=api_key)
    
    chat = client.chats.create(model="gemini-3.6-flash")
    response = chat.send_message(prompt)
    
    print("\n--- Generated RAG Answer ---")
    print(response.text)

if __name__ == "__main__":
    user_query = sys.argv[1] if len(sys.argv) > 1 else "What are the escalation caps across contracts?"
    run_rag(user_query)
