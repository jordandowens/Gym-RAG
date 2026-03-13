from api.services.mariadb import get_connection
from api.services.vectorstore import collection
from api.services.rag.embedder import embed
import json

def fetch_all_workouts():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM workouts")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def fetch_all_nutrition():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM nutrition")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def rebuild():
    print("Clearing vectorstore...")
    collection.delete(where={})

    print("Rebuilding workouts...")
    for w in fetch_all_workouts():
        doc = (
            f"Workout on {w['date']}:\n"
            f"{w['workout_text']}\n\n"
            f"Energy level: {w['energy_level']}\n"
            f"Notes: {w['notes']}\n"
            f"Metadata: {w['metadata']}"
        )
        embedding = embed(doc)
        collection.add(
            ids=[f"workout-{w['id']}"],
            embeddings=[embedding],
            documents=[doc],
            metadatas=[{
                "workout_id": w["id"],
                "user_id": w["user_id"],
                "date": str(w["date"]),
                "type": "workout"
            }]
        )

    print("Rebuilding nutrition...")
    for n in fetch_all_nutrition():
        doc = (
            f"Meal on {n['date']}: {n['name']}\n"
            f"{n['description']}\n\n"
            f"Calories: {n['calories']}, Protein: {n['protein']}, "
            f"Carbs: {n['carbs']}, Fat: {n['fat']}\n"
            f"Notes: {n['notes']}\n"
            f"Metadata: {n['metadata']}"
        )
        embedding = embed(doc)
        collection.add(
            ids=[f"nutrition-{n['id']}"],
            embeddings=[embedding],
            documents=[doc],
            metadatas=[{
                "nutrition_id": n["id"],
                "user_id": n["user_id"],
                "date": str(n["date"]),
                "type": "nutrition"
            }]
        )

    print("Vectorstore rebuild complete.")

if __name__ == "__main__":
    rebuild()
