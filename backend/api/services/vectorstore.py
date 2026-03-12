import chromadb
# Establish vectorstore connection

client = chromadb.HttpClient(host="chromadb", port=8000)

collection = client.get_or_create_collection(
    name="users",
    metadata={"hnsw:space": "cosine"}
)