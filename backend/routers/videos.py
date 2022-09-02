from typing import List, Union
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import schemas
from ..database.crud import ActorCrud, VideoCrud
from ..database.database import get_db


router = APIRouter(
    prefix="/api/videos",
    tags=["videos"],
    responses={404: {"description": "Not Found"}}
)

actor_crud = ActorCrud()
video_crud = VideoCrud()


@router.get("/", response_model=List[schemas.Video])
def get_videos(skip: Union[int, None] = None,
               limit: Union[int, None] = None,
               db: Session = Depends(get_db)):
    if skip is None and limit is None:
        return video_crud.query_all(db, sort_by_name=True)
    elif skip is None and limit is not None:
        return video_crud.query_all(db, limit=limit)
    elif skip is not None and limit is None:
        return video_crud.query_all(db, skip=skip)
    else:
        return video_crud.query_all(db, skip=skip, limit=limit)


@router.get("/{title}", response_model=schemas.Video)
def get_videos_by_title(title: str, db: Session = Depends(get_db)):
    return video_crud.query_check(db, title, by_name=True)


@router.get("/id/{_id}", response_model=schemas.Video)
def get_video_by_id(_id: str, db: Session = Depends(get_db)):
    return video_crud.query_check(db, _id)


@router.post("/{actor_name}", response_model=schemas.Video)
def create_video(actor_name: str, video: schemas.VideoCreate, db: Session = Depends(get_db)):
    db_actor = actor_crud.query_check(db, actor_name, by_name=True)
    return video_crud.create_video(db, db_actor, video)


@router.put("/{title}", response_model=schemas.Video)
def change_video_by_title(title: str, video: schemas.VideoUpdate, db: Session = Depends(get_db)):
    video_data = video.dict(exclude_unset=True)
    return video_crud.update_video(db, title, video_data, by_name=True)


@router.put("/id/{_id}", response_model=schemas.Video)
def change_video_by_id(_id: str, video: schemas.VideoUpdate, db: Session = Depends(get_db)):
    video_data = video.dict(exclude_unset=True)
    return video_crud.update_video(db, _id, video_data)


@router.put("/change-actor/{title}/{actor_name}", response_model=schemas.Video)
def change_video_actor_by_title(title: str, actor_name, db: Session = Depends(get_db)):
    db_actor = actor_crud.query_check(db, actor_name, by_name=True)
    return video_crud.change_owner(db, title, db_actor, by_name=True)


@router.delete("/{title}")
def delete_video_by_title(title: str, db: Session = Depends(get_db)):
    return video_crud.delete_video(db, title, True)


@router.delete("/id/{_id}")
def delete_video_by_id(_id: str, db: Session = Depends(get_db)):
    return video_crud.delete_video(db, _id)


@router.get("/actors/{name}", response_model=List[schemas.Video])
def get_all_actors_video_by_name(name: str, db: Session = Depends(get_db)):
    db_actor = actor_crud.query_check(db, name, by_name=True)
    return video_crud.query_by_owner_id(db, db_actor.id)


@router.get("/actors/{_id}", response_model=List[schemas.Video])
def get_all_actors_video_by_id(_id: str, db: Session = Depends(get_db)):
    return video_crud.query_by_owner_id(db, _id)
