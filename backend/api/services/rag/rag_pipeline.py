#Runs retrieval + LLM Call
from services.rag.retriever import retrieve
from services.rag.prompt_builder import build_prompt
from services.llama_client import generate

def run_rag(query: str, user_id: int):
    # 1. Retrieve relevant docs
    retrieved_docs = retrieve(query, user_id)

    # 2. Build prompt
    prompt = build_prompt(query, retrieved_docs)

    # 3. Generate answer
    answer = generate(prompt)

    return {
        "answer": answer,
        "sources": retrieved_docs
    }
