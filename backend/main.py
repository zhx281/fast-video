from fastapi import FastAPI
from .routers import actors, videos, streamer

from .database import models
from .database.database import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(actors.router)
app.include_router(videos.router)
app.include_router(streamer.router)


@app.get("/")
def home():
    return {"Hello": "World"}
