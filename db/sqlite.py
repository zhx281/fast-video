from typing import List, Union

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/db",
                   tags=["db"],
                   responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory="./templates")


# Helper functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def query_actor(info: Union[int, str], db: Session = Depends(get_db)):
    if isinstance(info, int):
        db_actor = crud.get_actor(db, actor_id=info)
    else:
        db_actor = crud.get_actor_by_name(db, name=info)
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return db_actor


# GET Route
@router.get("/actors/", response_model=List[schemas.Actor], response_class=HTMLResponse)
def read_actors(req: Request, db: Session = Depends(get_db)):
    actors = crud.get_actors(db)
    return templates.TemplateResponse("index.html", {"request": req, "actors": actors})


@router.get("/actors/{name}", response_model=schemas.Actor, response_class=HTMLResponse)
def read_actor(req: Request, name: str, db: Session = Depends(get_db)):
    db_actor = crud.get_actor_by_name(db, name=name)
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return templates.TemplateResponse("ActorDetail.html", {"request": req, "actor": db_actor})


# POST Route
@router.post("/actors/", response_model=schemas.Actor)
def create_actor(actor: schemas.ActorCreate, db: Session = Depends(get_db)):
    db_actor = crud.get_actor_by_name(db, name=actor.name)
    if db_actor:
        raise HTTPException(
            status_code=400, detail="Acotr already registered")
    return crud.create_actor(db=db, actor=actor)


@router.post("/actors/{actor_info}/videos/", response_model=schemas.Video)
def create_video_for_user(actor_info: Union[int, str],
                          video: schemas.VideoCreate,
                          db: Session = Depends(get_db)):
    db_actor = query_actor(actor_info, db)
    _id = db_actor.id
    return crud.create_actor_video(db=db, video=video, actor_id=_id)


# Delete Route
@router.delete("/actors/{actor_info}")
def delete_actor(actor_info: Union[int, str], db: Session = Depends(get_db)):
    db_actor = query_actor(actor_info, db)
    name = db_actor.name
    for video in db_actor.videos:
        crud.delete_video(db, video)
    crud.delete_actor(db, db_actor)
    return {"message": f"{name} has been deleted from Database successfully"}


@router.delete("/videos/{video_id}")
def delete_video(video_id: int, db: Session = Depends(get_db)):
    db_video = crud.get_video_by_id(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    name = db_video.name
    crud.delete_video(db, video=db_video)
    return {"message": f"{name} has been deleted from Database successfully"}


# Put Route
@router.put("/actors/{actor_info}", response_model=schemas.Actor)
def update_actor(actor_info: Union[int, str],
                 actor_request: schemas.ActorUpdate,
                 db: Session = Depends(get_db)):
    db_actor = query_actor(actor_info, db)
    actor_data = actor_request.dict(exclude_unset=True)
    for k, v in actor_data.items():
        setattr(db_actor, k, v)
    return crud.update_actor(db, db_actor)


@router.put("/videos/{video_id}", response_model=schemas.Video)
def update_video(video_id: int,
                 video_request: schemas.VideoUpdate,
                 db: Session = Depends(get_db)):
    db_video = crud.get_video_by_id(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    video_data = video_request.dict(exclude_unset=True)
    for k, v in video_data.items():
        setattr(db_video, k, v)
    return crud.update_video(db, db_video)
