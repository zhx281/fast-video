from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image = Column(String)
    is_active = Column(Boolean, default=True)

    videos = relationship("Video", back_populates="owner")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    image = Column(String)
    is_active = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("actors.id"))

    owner = relationship("Actor", back_populates="videos")
