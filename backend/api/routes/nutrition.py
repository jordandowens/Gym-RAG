from fastapi import APIRouter, HTTPException
from services.mariadb import get_connection
from services.vectorstore import collection
from models.nutrition_create import NutritionCreate
from models.nutrition_read import NutritionRead
import json

router = APIRouter()

@router.post("/", response_model=NutritionRead)
def create_nutrition(entry: NutritionCreate):
    # Insert into MariaDB
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO meals (
                user_id, date, name, description,
                calories, protein, carbs, fat,
                notes, metadata
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                entry.user_id,
                entry.date,
                entry.name,
                entry.description,
                entry.calories,
                entry.protein,
                entry.carbs,
                entry.fat,
                entry.notes,
                json.dumps(entry.metadata) if entry.metadata else None
            )
        )
        conn.commit()

        nutrition_id = cur.lastrowid

        cur.execute("SELECT created_at FROM meals WHERE id = %s", (nutrition_id,))
        created_at = cur.fetchone()[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    finally:
        cur.close()
        conn.close()

    # Insert into ChromaDB
    try:
        vector_id = f"nutrition-{nutrition_id}"

        # Build a rich document for embeddings
        document = (
            f"Meal on {entry.date}: {entry.name}\n"
            f"Description: {entry.description}\n\n"
            f"Calories: {entry.calories}, Protein: {entry.protein}, "
            f"Carbs: {entry.carbs}, Fat: {entry.fat}\n"
            f"Notes: {entry.notes}\n"
            f"Metadata: {entry.metadata}"
        )

        # Clean metadata for Chroma (no None values)
        meta = {
            "nutrition_id": nutrition_id,
            "user_id": entry.user_id,
            "date": str(entry.date),
            "calories": entry.calories,
            "meal_type": entry.metadata.get("meal_type"),
            "phase": entry.metadata.get("phase"),
            "quality": entry.metadata.get("quality"),
            "day_of_week": entry.metadata.get("day_of_week")
        }

        # Remove None values
        meta = {k: v for k, v in meta.items() if v is not None}

        collection.add(
            ids=[vector_id],
            documents=[document],
            metadatas=[meta]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vectorstore error: {e}")

    # Return NutritionRead
    return NutritionRead(
        id=nutrition_id,
        user_id=entry.user_id,
        date=entry.date,
        name=entry.name,
        description=entry.description,
        calories=entry.calories,
        protein=entry.protein,
        carbs=entry.carbs,
        fat=entry.fat,
        notes=entry.notes,
        metadata=entry.metadata,
        created_at=created_at
    )
