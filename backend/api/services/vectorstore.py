import chromadb
# Establish vectorstore connection

client = chromadb.HttpClient(host="chromadb", port=8000)

collection = client.get_or_create_collection(
    name="workouts",
    metadata={"hnsw:space": "cosine"}
)