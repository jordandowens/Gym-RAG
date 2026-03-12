#FastAPI Entrypoint
from fastapi import FastAPI
from routes.users import router as users_router
from routes.workout import router as workout_router
from routes.nutrition import router as nutrition_router

app = FastAPI()

app.include_router(users_router, prefix="/api")
app.include_router(workout_router, prefix="/api")
app.include_router(nutrition_router, prefix="/api")
