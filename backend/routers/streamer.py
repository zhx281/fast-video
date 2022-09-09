import os
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from ..database.crud import VideoCrud
from ..database.database import get_db
from ..stream.stream import range_requests_response

# Media path change to you local hard drive or media server
media_path = os.getcwd()

# Setup for fastapi router
router = APIRouter(
    prefix="/stream/video",
    tags=["stream"],
    responses={404: {"description": "Not Found"}}
)

# Initalize the video crud object
video_crud = VideoCrud()


@router.get("/")
async def video_stream(req: Request, video: str, db: Session = Depends(get_db)):
    # req = getting the request header
    # video = title of video
    # db = database local session

    # Checkin if the video path is in database
    db_video = video_crud.query_check(db, video, by_name=True)
    # Create a complete path for the video
    path = os.path.join(media_path, db_video.path)
    # Returning stream data in chunks as the video play
    # with the request header information as the timestamp
    return range_requests_response(req, path, "video/mp4")
