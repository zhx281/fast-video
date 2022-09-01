from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from db import sqlite

app = FastAPI()
app.include_router(sqlite.router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home():
    return RedirectResponse("/db/actors/")


@app.get("/videos/{actor}/{video}", response_class=HTMLResponse)
def play_video(req: Request, actor: str, video: str):
    return templates.TemplateResponse("PlayVideo.html",
                                      {"request": req,
                                       "actor": actor,
                                       "video": video})
