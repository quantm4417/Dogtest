from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.routers import auth, dogs, health, equipment, care, tags, training, walks, activity, reminders
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing dogs, health, training, and walks.",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Ensure media directory exists
os.makedirs("/app/media", exist_ok=True)

# Mount static files for media
app.mount("/media", StaticFiles(directory="/app/media"), name="media")

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <--- CHANGE THIS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(dogs.router, prefix=f"{settings.API_V1_STR}/dogs", tags=["dogs"])
app.include_router(health.router, prefix=f"{settings.API_V1_STR}/health", tags=["health"])
app.include_router(equipment.router, prefix=f"{settings.API_V1_STR}/equipment", tags=["equipment"])
app.include_router(care.router, prefix=f"{settings.API_V1_STR}/care", tags=["care"])
app.include_router(tags.router, prefix=f"{settings.API_V1_STR}/tags", tags=["tags"])
app.include_router(training.router, prefix=f"{settings.API_V1_STR}/training", tags=["training"])
app.include_router(walks.router, prefix=f"{settings.API_V1_STR}/walks", tags=["walks"])
app.include_router(activity.router, prefix=f"{settings.API_V1_STR}/activity", tags=["activity"])
app.include_router(reminders.router, prefix=f"{settings.API_V1_STR}/reminders", tags=["reminders"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Dog Management API"}

