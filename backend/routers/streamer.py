import os
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from ..database.crud import VideoCrud
from ..database.database import get_db
from ..stream.stream import range_requests_response

media_path = os.getcwd()
print(media_path)

router = APIRouter(
    prefix="/stream/video",
    tags=["stream"],
    responses={404: {"description": "Not Found"}}
)

video_crud = VideoCrud()


@router.get("/")
async def video_stream(req: Request, video: str, db: Session = Depends(get_db)):
    db_video = video_crud.query_check(db, video, by_name=True)
    path = os.path.join(media_path, db_video.path)
    return range_requests_response(req, path, "video/mp4")
