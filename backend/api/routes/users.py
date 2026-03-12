from fastapi import APIRouter, HTTPException
from services.mariadb import get_connection
from services.vectorstore import collection
from models.user_create import UserCreate
from models.user_read import UserRead

router = APIRouter()

@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate):
    #Insert into MariaDB
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (username) VALUES (%s)",
            (user.username,)
        )
        conn.commit()

        user_id = cur.lastrowid

        cur.execute("SELECT created_at FROM users WHERE id = %s", (user_id,))
        created_at = cur.fetchone()[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    finally:
        cur.close()
        conn.close()

    #Insert into ChromaDB
    try:
        vector_id = f"user-{user_id}"

        collection.add(
            ids=[vector_id],
            documents=[f"User profile for {user.username}"],
            metadatas=[{"user_id": user_id, "username": user.username}]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vectorstore error: {e}")

    #Return UserRead model
    return UserRead(
        id=user_id,
        username=user.username,
        created_at=created_at
    )
