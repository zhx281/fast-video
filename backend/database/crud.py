from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


class Actions:
    '''
    Base Class for most of common CRUD Actions.
    '''

    def __init__(self):
        pass

    def query_check(self, db: Session, info: str, is_register: bool = False, by_name: bool = False):
        db_actor = self.query_one(db, info, by_name=by_name)
        if is_register:
            self.already_registered(db_actor, info)
        else:
            self.not_found(db_actor, info)
        return db_actor

    def query_all(self, db: Session, skip: int = 0, limit: int = 100, sort_by_name: bool = False):
        if sort_by_name:
            return db.query(self.model).order_by(self.name).all()
        return db.query(self.model).offset(skip).limit(limit).all()

    def query_one(self, db: Session, string: str, by_name=False):
        if by_name:
            return db.query(self.model).filter(self.name == string).first()
        return db.query(self.model).filter(self.model.id == string).first()

    def update(self, model, db: Session, update_data: dict):
        for k, v in update_data.items():
            setattr(model, k, v)
        return self.add(db, model)

    def add(self, db: Session, model):
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    def delete(self, db: Session, schema):
        db.delete(schema)
        db.commit()

    def not_found(self, model, name: str):
        if model is None:
            raise HTTPException(
                status_code=404, detail=f"{self.__class__.__name__}: {name} not found")

    def already_registered(self, model, name: str):
        if model:
            raise HTTPException(
                status_code=400, detail=f"{self.__class__.__name__}: {name} already registered")

    def _500(self, e):
        raise HTTPException(
            status_code=500, detail={"message": f"{self.__class__.__name__}: Oops Something Went Wrong",
                                     "error": str(e)})


class ActorCrud(Actions):
    '''
    Specific CRUD actions for Actors.
    '''

    def __init__(self):
        super().__init__()
        self.model = models.Actor
        self.name = self.model.name

    def creat_actor(self, db: Session, actor: schemas.ActorCreate):
        self.query_check(db, actor.name, is_register=True, by_name=True)
        db_actor = models.Actor(**actor.dict())
        return self.add(db, db_actor)

    def update_actor(self, db: Session, info: str, update_data: dict, by_name: bool = False):
        db_actor = self.query_check(db, info, by_name=by_name)
        return self.update(db_actor, db, update_data)

    def delete_actor(self, db: Session, info: str, by_name: bool = False):
        db_actor = self.query_check(db, info, by_name=by_name)
        try:
            self.delete(db, db_actor)
            return {"message": f"Successfully removed {info} from database "}
        except Exception as e:
            self._500(e)


class VideoCrud(Actions):
    '''
    Specific CRUD Actions for Videos.
    '''

    def __init__(self):
        super().__init__()
        self.model = models.Video
        self.name = self.model.title

    def create_video(self, db: Session, actor: schemas.Actor, video: schemas.VideoCreate):
        self.query_check(db, video.title, is_register=True, by_name=True)
        actor_id = actor.id
        db_video = self.model(**video.dict(), owner_id=actor_id)
        return self.add(db, db_video)

    def update_video(self, db: Session, info: str, update_data: dict, by_name: bool = False):
        db_video = self.query_check(db, info, by_name=by_name)
        return self.update(db_video, db, update_data)

    def delete_video(self, db: Session, info: str, by_name: bool = False):
        db_video = self.query_check(db, info, by_name=by_name)
        try:
            self.delete(db, db_video)
            return {"message": f"Successfully removed {info} from database "}
        except Exception as e:
            self._500(e)

    def change_owner(self, db: Session, info: str, actor: schemas.Actor, by_name: bool = False):
        db_video = self.query_check(db, info, by_name=by_name)
        setattr(db_video, "owner_id", actor.id)
        return self.add(db, db_video)

    def query_by_owner_id(self, db: Session, owner_id: str):
        return db.query(self.model).filter(self.model.owner_id == owner_id).all()

    def delete_all_actor_video(self, db: Session, owner_id: str):
        video_list = self.query_by_owner_id(db, owner_id)
        try:
            if video_list:
                for video in video_list:
                    self.delete(db, video)
            return True
        except Exception as e:
            self._500(e)
