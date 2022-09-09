from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .routers import actors, videos, streamer

from .database import models
from .database.database import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

hosts = ["http://localhost:3000", "http://localhost:8000"]

# CORS in order for react to fetch from api within localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=hosts,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Including routes for different api modules
app.include_router(actors.router)
app.include_router(videos.router)
app.include_router(streamer.router)

# Including the build file from react-app
# Using the html=True so the static file serve as html files
app.mount("/", StaticFiles(directory="./backend/template", html=True), name="react")


@app.get("/")
def home():
    # Sending the response as a HTML Response
    return HTMLResponse("index.html", status_code=200)
