import os
from fastapi import APIRouter, Request

from ..stream.stream import range_requests_response

media_path = os.path.join(os.getcwd(), "mp4")
print(media_path)

router = APIRouter(
    prefix="/stream/video",
    tags=["video"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/")
async def video_stream(req: Request, actor: str, video: str):
    if ".mp4" not in video:
        video = video + ".mp4"
    path = os.path.join(media_path, actor + "/" + video)
    return range_requests_response(req, path, "video/mp4")
