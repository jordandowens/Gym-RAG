from fastapi import APIRouter, HTTPException
from services.mariadb import get_connection
from services.vectorstore import collection
from models.workout_create import WorkoutCreate
from models.workout_read import WorkoutRead
import json

router = APIRouter()

@router.post("/", response_model=WorkoutRead)
def create_workout(workout: WorkoutCreate):
    # Insert into MariaDB
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO workouts (user_id, date, workout_text, energy_level, notes, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                workout.user_id,
                workout.date,
                workout.workout_text,
                workout.energy_level,
                workout.notes,
                json.dumps(workout.metadata) if workout.metadata else None
            )
        )
        conn.commit()

        workout_id = cur.lastrowid

        cur.execute("SELECT created_at FROM workouts WHERE id = %s", (workout_id,))
        created_at = cur.fetchone()[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    finally:
        cur.close()
        conn.close()

    # Insert into ChromaDB
    try:
        vector_id = f"workout-{workout_id}"

        # Build a rich document for embeddings
        document = (
            f"Workout on {workout.date}:\n"
            f"{workout.workout_text}\n\n"
            f"Energy level: {workout.energy_level}\n"
            f"Notes: {workout.notes}\n"
            f"Metadata: {workout.metadata}"
        )

        # Clean metadata for Chroma
        raw_movements = workout.metadata.get("movements")

        meta = {
            "workout_id": workout_id,
            "user_id": workout.user_id,
            "date": str(workout.date),
            "energy_level": workout.energy_level,
            "phase": workout.metadata.get("phase"),
            "day_of_week": workout.metadata.get("day_of_week"),
            "is_rest_day": workout.metadata.get("is_rest_day"),
            "quality": workout.metadata.get("quality"),
            "focus": workout.metadata.get("focus"),
            "movements": json.dumps(raw_movements) if raw_movements else None
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

    # Return WorkoutRead model
    return WorkoutRead(
        id=workout_id,
        user_id=workout.user_id,
        date=workout.date,
        workout_text=workout.workout_text,
        energy_level=workout.energy_level,
        notes=workout.notes,
        metadata=workout.metadata,
        created_at=created_at
    )
