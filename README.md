# Procurement RAG Analyst


**Open towards Team Collaborations & Contract Opportunities.**

An intelligent procurement assistant that uses local vector embeddings to perform semantic search over legal contracts and leverages a locally-hosted Ollama model to deliver strict, context-bound answers for contract queries.

## Features
* **Local Dense Retrieval:** Uses `sentence-transformers` (`all-MiniLM-L6-v2`) and cosine similarity for document vector search.
* **Local LLM Generation:** Runs entirely on device via Ollama no API keys required.
* **Procurement Analyst Guardrails:** Prompts are structured to reject answers not supported by contract data.

## Project Structure
```text
procurement-rag/
|-- data/                  # Contract data and metadata
|-- src/
|   |-- ingest.py
|   |-- chunk.py
|   |-- embed.py
|   |-- vector_store.py
|   |-- query_rag.py
|   |-- generate_answer.py
|   `-- api_server.py
|-- .gitignore
|-- requirements.txt
`-- README.md
