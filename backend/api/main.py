from fastapi import FastAPI

# Import your existing routers
from routes.users import router as users_router
from routes.workout import router as workout_router
from routes.nutrition import router as nutrition_router

# Create ONE FastAPI app
app = FastAPI(
    title="Gym-RAG API",
    version="1.0.0"
)

# Register your existing routers
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(workout_router, prefix="/workouts", tags=["Workouts"])
app.include_router(nutrition_router, prefix="/nutrition", tags=["Nutrition"])

# -----------------------------
# RAG TEST ENDPOINT (lazy import)
# -----------------------------
@app.post("/rag/test", tags=["RAG"])
def test_rag(payload: dict):
    # Lazy import prevents blocking during startup
    from services.rag.rag_pipeline import run_rag

    query = payload["query"]
    user_id = payload.get("user_id", 1)
    return run_rag(query, user_id)


@app.get("/health")
def health():
    return {"status": "ok"}
