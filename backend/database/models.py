from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .database import Base

import shortuuid


def generate_id():
    # Returning the str of generated short uuid
    return str(shortuuid.uuid())


class Actor(Base):
    __tablename__ = "actors"

    id = Column(String, primary_key=True, unique=True,
                index=True, default=generate_id)
    name = Column(String, index=True)
    image = Column(String)
    is_active = Column(Boolean, default=True)

    videos = relationship("Video", back_populates="owner")


class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, unique=True,
                index=True, default=generate_id)
    title = Column(String)
    description = Column(String)
    image = Column(String)
    path = Column(String)
    is_active = Column(Boolean, default=True)
    owner_id = Column(String, ForeignKey("actors.id"))

    owner = relationship("Actor", back_populates="videos")
