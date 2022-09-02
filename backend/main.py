from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .routers import actors, videos, streamer

from .database import models
from .database.database import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Including routes for different api modules
app.include_router(actors.router)
app.include_router(videos.router)
app.include_router(streamer.router)

# Including the build file from react-app
app.mount("/", StaticFiles(directory="./backend/template", html=True), name="react")


@app.get("/")
def home():
    return HTMLResponse("index.html", status_code=200)
