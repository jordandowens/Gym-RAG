import json
import mariadb
import chromadb
from chromadb.config import Settings
from embedding import embed
from dotenv import load_dotenv
import os

load_dotenv()

# -----------------------------
# MariaDB connection
# -----------------------------
conn = mariadb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    autocommit=True
)
cursor = conn.cursor()

# -----------------------------
# ChromaDB connection
# -----------------------------
chroma = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST"),
    port=int(os.getenv("CHROMA_PORT")),
    settings=Settings(allow_reset=False)
)

collection = chroma.get_or_create_collection("workouts")

# -----------------------------
# Load JSON
# -----------------------------
json_path = r"C:\Users\steam\Desktop\Gym-RAG\backend\scripts\data\workouts.json"
with open(json_path, "r") as f:
    workouts = json.load(f)

# -----------------------------
# Ensure user exists
# -----------------------------
def ensure_user(user_id):
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if cursor.fetchone():
        return
    cursor.execute("INSERT INTO users (id, username) VALUES (?, ?)", (user_id, f"user_{user_id}"))
    print(f"Created missing user {user_id}")

# -----------------------------
# Insert loop
# -----------------------------
for w in workouts:
    user_id = w["user_id"]
    ensure_user(user_id)

    cursor.execute("""
        INSERT INTO workouts (user_id, date, workout_text, energy_level, notes, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        w["date"],
        w["workout_text"],
        w.get("energy_level"),
        w.get("notes"),
        json.dumps(w.get("metadata", {}))
    ))

    workout_id = cursor.lastrowid

    vector = embed(w["workout_text"])

    collection.add(
        ids=[f"workout-{workout_id}"],
        documents=[w["workout_text"]],
        embeddings=[vector],
        metadatas=[{
            "source_type": "workout",
            "source_id": workout_id,
            "user_id": user_id
        }]
    )

    cursor.execute("""
        INSERT INTO embedding_index (source_type, source_id)
        VALUES ('workout', ?)
    """, (workout_id,))

    print(f"Inserted workout {workout_id}")

print("Workout ingestion complete.")
