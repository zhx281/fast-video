from sqlalchemy.orm import Session

from . import models, schemas


def get_actor(db: Session, actor_id: int):
    return db.query(models.Actor).filter(models.Actor.id == actor_id).first()


def get_actor_by_name(db: Session, name: str):
    return db.query(models.Actor).filter(models.Actor.name == name).first()


def get_actors(db: Session):
    return db.query(models.Actor).order_by(models.Actor.name).all()


def create_actor(db: Session, actor: schemas.ActorCreate):
    db_actor = models.Actor(name=actor.name, image=actor.image)
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor


def update_actor(db: Session, actor: schemas.Actor):
    db.add(actor)
    db.commit()
    db.refresh(actor)
    return actor


def delete_actor(db: Session, actor: schemas.Actor):
    db.delete(actor)
    db.commit()


def get_videos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Video).offset(skip).limit(limit).all()


def get_video_by_id(db: Session, video_id):
    return db.query(models.Video).filter(models.Video.id == video_id).first()


def update_video(db: Session, video: schemas.Video):
    db.add(video)
    db.commit()
    db.refresh(video)
    return video


def create_actor_video(db: Session, video: schemas.VideoCreate, actor_id: int):
    db_video = models.Video(**video.dict(), owner_id=actor_id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def delete_video(db: Session, video: schemas.Video):
    db.delete(video)
    db.commit()
