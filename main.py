from fastapi import FastAPI

from db import Base, engine
from routes import user_routes
from routes import story_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
app.include_router(story_routes.router)

@app.get("/")
def root():
    return {"message": "Backend Running"}