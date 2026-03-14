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

collection = chroma.get_or_create_collection("user_data")

# -----------------------------
# Load JSON
# -----------------------------
json_path = r"C:\Users\steam\Desktop\Gym-RAG\backend\scripts\data\meals.json"
with open(json_path, "r") as f:
    meals = json.load(f)

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
for m in meals:
    user_id = m["user_id"]
    ensure_user(user_id)

    cursor.execute("""
        INSERT INTO meals (user_id, date, name, description, calories, protein, carbs, fat, notes, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        m["date"],
        m["name"],
        m.get("description"),
        m.get("calories"),
        m.get("protein"),
        m.get("carbs"),
        m.get("fat"),
        m.get("notes"),
        json.dumps(m.get("metadata", {}))
    ))

    meal_id = cursor.lastrowid

    # Build rich document text (matches FastAPI ingestion)
    document = (
        f"Meal on {m['date']}: {m['name']}\n"
        f"Description: {m.get('description', '')}\n\n"
        f"Calories: {m.get('calories')}, Protein: {m.get('protein')}, "
        f"Carbs: {m.get('carbs')}, Fat: {m.get('fat')}\n"
        f"Notes: {m.get('notes')}\n"
        f"Metadata: {m.get('metadata')}"
    )

    vector = embed(document)

    collection.add(
        ids=[f"meal-{meal_id}"],
        documents=[document],
        embeddings=[vector],
        metadatas=[{
            "source_type": "meal",
            "source_id": meal_id,
            "user_id": user_id,
            "date": m["date"],
            "meal_type": m["metadata"]["meal_type"],
            "quality": m["metadata"]["quality"],
            "phase": m["metadata"]["phase"]
        }]
    )

    cursor.execute("""
        INSERT INTO embedding_index (source_type, source_id)
        VALUES ('meal', ?)
    """, (meal_id,))

    print(f"Inserted meal {meal_id}")

print("Meal ingestion complete.")
