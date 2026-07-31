from fastapi import FastAPI

from db import Base, engine
from routes import user_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)


@app.get("/")
def root():
    return {"message": "Backend Running"}