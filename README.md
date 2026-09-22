# Procurement RAG Analyst

**Open towards Team Collaborations & Contract Opportunities.**

An intelligent procurement assistant that uses local vector embeddings to perform semantic search over legal contracts and leverages a locally-hosted Ollama model to deliver strict, context-bound answers for contract queries.

## Features
* **Local Dense Retrieval:** Uses `sentence-transformers` (`all-MiniLM-L6-v2`) and cosine similarity for document vector search.
* **Context Curation:** Retrieved chunks are pruned to a real token budget and position-ordered before reaching the model, via [CCL](https://github.com/Cre8tiveStuff/Context-Curation-Ledger) — countering the "lost in the middle" effect confirmed for this model family.
* **Local LLM Generation:** Runs entirely on device via Ollama, no API keys required.
* **Safe Re-indexing:** `refresh_index.py` uses [ARC](https://github.com/Cre8tiveStuff/ARC-Agentic-Reasoning-Chain)'s `@idempotent` decorator, so re-indexing an already-processed file is a safe no-op rather than duplicate work.
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
|   |-- query_rag.py       # Now curates chunks via CCL before prompt-building
|   |-- refresh_index.py   # Idempotent re-indexing via ARC
|   |-- generate_answer.py
|   `-- api_server.py
|-- .gitignore
|-- requirements.txt
`-- README.md
```

## Part of a larger system

This repo is one of five connected projects, orchestrated together by [O2A](https://github.com/Cre8tiveStuff/O2A-Observability-Orchestration-Agent), an agent that calls this pipeline's retrieval and re-indexing capabilities as genuine, callable tools — verified end-to-end with a real, passing multi-tool reasoning test.