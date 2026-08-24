# Procurement RAG Analyst

An intelligent procurement assistant that uses local vector embeddings to perform semantic search over legal contracts and leverages the Google Gemini API to deliver strict, context-bound answers for contract queries.

## Features
* **Local Dense Retrieval:** Uses `sentence-transformers` (`all-MiniLM-L6-v2`) and cosine similarity for document vector search.
* **Context-Bound LLM Generation:** Integrates with Google's Gemini models via the `google-genai` SDK to answer queries strictly using retrieved contract context.
* **Procurement Analyst Guardrails:** Prompts are structured to reject answers not supported by contract data.

## Project Structure
```text
procurement-rag/
├── data/                  # Contract data and metadata
├── scripts/
│   ├── 01_ingest_data.py
│   ├── 02_chunk_documents.py
│   ├── 03_generate_embeddings.py
│   ├── 04_vector_store.py
│   └── 05_rag_query.py    # Main execution script
├── .gitignore
├── requirements.txt
└── README.md