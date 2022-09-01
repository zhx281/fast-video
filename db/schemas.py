from typing import List, Union, Optional

from pydantic import BaseModel


class VideoBase(BaseModel):
    title: str
    description: Union[str, None] = None
    image: Union[str, None] = None


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int
    is_active: bool
    owner_id: int

    class Config:
        orm_mode = True


class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: Optional[bool] = None


class ActorBase(BaseModel):
    name: str
    image: Union[str, None] = None


class ActorCreate(ActorBase):
    pass


class Actor(ActorBase):
    id: int
    is_active: bool
    videos: List[Video] = []

    class Config:
        orm_mode = True


class ActorUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    is_active: Optional[bool] = None
