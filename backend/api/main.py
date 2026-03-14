from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Routers
from routes.users import router as users_router
from routes.workout import router as workouts_router
from routes.nutrition import router as meals_router

# RAG pipeline
from services.rag.rag_pipeline import run_rag

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(workouts_router, prefix="/workouts", tags=["Workouts"])
app.include_router(meals_router, prefix="/meals", tags=["Meals"])

# --- RAG Request Model ---
class RAGRequest(BaseModel):
    query: str
    user_id: int

# --- Production RAG Endpoint ---
@app.post("/rag")
def rag_endpoint(payload: RAGRequest):
    """
    Runs the full RAG pipeline for a specific user.
    """
    try:
        result = run_rag(
            query=payload.query,
            user_id=payload.user_id
        )
        return result
    except Exception as e:
        return {"error": str(e)}

