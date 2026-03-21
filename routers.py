from fastapi import FastAPI, Depends, APIRouter, HTTPException
from repository import TrackReposutory
from typing import Annotated
from schemas import STracksAdd, STracks


router = APIRouter(
       prefix="/tracks",
       tags=["Треки"]
)

@router.post("", response_model=STracks)  # Возвращаем полный объект с id
async def add_tracks(
    track: Annotated[STracksAdd, Depends()],
):
    try:
        created_track = await TrackReposutory.add_one(track)
        return created_track
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=list[STracks])
async def get_tracks():
    try:
        tracks = await TrackReposutory.find_all()
        return tracks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{track_id}", response_model=STracks)
async def get_track_by_id(track_id: int):
    try:
        track = await TrackReposutory.find_by_id(track_id)
        if track is None:
            raise HTTPException(status_code=404, detail=f"Track {track_id} not found")
        return track
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))