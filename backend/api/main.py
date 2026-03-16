from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from routes.users import router as users_router
from routes.workout import router as workouts_router
from routes.nutrition import router as meals_router

# RAG pipeline
from models.rag_request import RAGRequest
from services.rag.rag_pipeline import run_rag

app = FastAPI()

#CORS - middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Routers
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(workouts_router, prefix="/workouts", tags=["Workouts"])
app.include_router(meals_router, prefix="/meals", tags=["Meals"])


#Production RAG Endpoint
@app.post("/rag")
def rag_endpoint(payload: RAGRequest):
    try:
        result = run_rag(
            query=payload.query,
            user_id=payload.user_id
        )
        return result
    except Exception as e:
        return {"error": str(e)}

