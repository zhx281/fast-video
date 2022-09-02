from typing import List, Union
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session


from ..database import schemas
from ..database.crud import ActorCrud, VideoCrud
from ..database.database import get_db


router = APIRouter(
    prefix="/api/actors",
    tags=["actors"],
    responses={404: {"description": "Not Found"}}
)

actor_crud = ActorCrud()
video_crud = VideoCrud()


@router.get("/", response_model=List[schemas.Actor])
def get_actors(skip: Union[int, None] = None,
               limit: Union[int, None] = None,
               db: Session = Depends(get_db)):
    if skip is None and limit is None:
        return actor_crud.query_all(db, sort_by_name=True)
    elif skip is None and limit is not None:
        return actor_crud.query_all(db, limit=limit)
    elif skip is not None and limit is None:
        return actor_crud.query_all(db, skip=skip)
    else:
        return actor_crud.query_all(db, skip=skip, limit=limit)


@router.get("/{name}", response_model=schemas.Actor)
def get_actors_by_name(name: str, db: Session = Depends(get_db)):
    return actor_crud.query_check(db, name, by_name=True)


@router.get("/id/{_id}", response_model=schemas.Actor)
def get_actor_by_id(_id: str, db: Session = Depends(get_db)):
    return actor_crud.query_check(db, _id)


@router.post("/", response_model=schemas.Actor)
def create_actor(actor: schemas.ActorCreate, db: Session = Depends(get_db)):
    return actor_crud.creat_actor(db, actor)


@router.put("/{name}", response_model=schemas.Actor)
def change_actor_by_name(name: str, actor: schemas.ActorUpdate, db: Session = Depends(get_db)):
    actor_data = actor.dict(exclude_unset=True)
    return actor_crud.update_actor(db, name, actor_data, by_name=True)


@router.put("/id/{_id}", response_model=schemas.Actor)
def change_actor_by_id(_id: str, actor: schemas.ActorUpdate, db: Session = Depends(get_db)):
    actor_data = actor.dict(exclude_unset=True)
    return actor_crud.update_actor(db, _id, actor_data)


@router.delete("/{name}")
def delete_actor_by_name(name: str, with_video: bool = False, db: Session = Depends(get_db)):
    if with_video:
        db_actor = actor_crud.query_check(db, name, by_name=True)
        if video_crud.delete_all_actor_video(db, db_actor.id):
            try:
                actor_crud.delete(db, db_actor)
                return {"detail": f"Successful remove {name} from database with it's videos"}
            except Exception as e:
                actor_crud._500(e)
    return actor_crud.delete_actor(db, name, True)


@router.delete("/id/{_id}")
def delete_actor_by_id(_id: str, with_video: bool = False, db: Session = Depends(get_db)):
    if with_video:
        db_actor = actor_crud.query_check(db, _id)
        if video_crud.delete_all_actor_video(db, db_actor.id):
            try:
                actor_crud.delete(db, db_actor)
                return {"detail": f"Successful remove {_id} from database with it's videos"}
            except Exception as e:
                actor_crud._500(e)
    return actor_crud.delete_actor(db, _id)
