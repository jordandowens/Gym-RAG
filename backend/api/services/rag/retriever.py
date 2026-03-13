#Reads from Vector Store
from services.vectorstore import collection
from services.rag.embedder import embed

def retrieve(query: str, user_id: int, k: int = 5):
    query_embedding = embed(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        where={"user_id": user_id},
        include=["documents", "metadatas"]
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    return list(zip(docs, metas))
