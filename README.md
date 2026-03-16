# Gym-RAG
## Description

Gym‑RAG is a Retrieval‑Augmented Generation system designed to help users optimize their workouts, reach dietary goals, and progress in strength training. It works by allowing users to log their meals and workouts, then interact with the Gym‑RAG personal assistant to receive tailored guidance on how to take the next step in their fitness journey.

## Architecture

Gym‑RAG is powered by a set of modular components that work together to support retrieval‑augmented generation, structured data storage, and a responsive API layer.

### Docker
Docker hosts the primary back‑end services for Gym‑RAG. Containerization ensures each component is isolated, reproducible, and easy to scale or redeploy. This also improves fault tolerance by preventing one service from interfering with another.

### MariaDB Database
MariaDB is included to support future features that require structured relational queries. While the current system relies primarily on semantic similarity search, MariaDB provides a foundation for storing user profiles, logs, or other structured data as the application evolves.

### ChromaDB Vectorstore
ChromaDB stores data as embedding vectors, enabling semantic similarity search rather than traditional keyword or relational lookups. This allows Gym‑RAG to retrieve contextually relevant information based on meaning, not exact matches.

### llama.cpp server
A llama.cpp instance runs inside a Docker container, hosting the local LLM used for inference.
The model currently deployed is:
llama-3.1-8b-instruct-q4_k_m.gguf

In order to run this locally, this gguf file must be downloaded and placed in: 
backend/models/

### FastAPI
FastAPI serves as the Python API layer for Gym‑RAG. It orchestrates the RAG pipeline, validates request and response data using Pydantic models, and exposes HTTP endpoints consumed by the React front‑end.
This container is configured with a bind‑mount to allow live code updates without requiring container rebuilds or restarts.

## Quick Start
To install, follow a few simple instructions:
1. Ensure that the .gguf file for the correct model is placed in backend/models/
2. Navigate to backend/docker/, run the command: docker compose up -d
3. (Optional) Navigate to backend/scripts/, run: python generate_gym_rag_data.py to generate dummy data, followed by both ingestion scripts to populate the MariaDB and ChromaDB databases.
4. Navigate to frontend/ run: npm install followed by npm run dev (Local front-end for testing purposes)