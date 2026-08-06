from fastapi import FastAPI

from db import Base, engine
from routes import user_routes
from routes import story_routes
from fastapi.staticfiles import StaticFiles
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
app.include_router(story_routes.router)

@app.get("/")
def root():
    return {"message": "Backend Running"}

# Create folder if it doesn't exist
os.makedirs("generated_images", exist_ok=True)

# Serve generated images
app.mount(
    "/generated_images",
    StaticFiles(directory="generated_images"),
    name="generated_images"
)