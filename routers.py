from fastapi import FastAPI, Depends, APIRouter, HTTPException
from repository import TrackReposutory
from typing import Annotated
from schemas import STracksAdd, STracks, STracksUpdate

router = APIRouter(
       prefix="/tracks",
       tags=["Треки"]
)

@router.post("", response_model=STracks)  # CREATE - создание
async def add_tracks(
    track: Annotated[STracksAdd, Depends()],
):
    """Добавление нового трека"""
    try:
        created_track = await TrackReposutory.add_one(track)
        return created_track
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=list[STracks])  # READ - чтение всех
async def get_tracks():
    """Получение списка всех треков"""
    try:
        tracks = await TrackReposutory.find_all()
        return tracks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{track_id}", response_model=STracks)  # READ - чтение одного
async def get_track_by_id(track_id: int):
    """Получение трека по ID"""
    try:
        track = await TrackReposutory.find_by_id(track_id)
        if track is None:
            raise HTTPException(status_code=404, detail=f"Track {track_id} not found")
        return track
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{track_id}", response_model=STracks)  # UPDATE - полное обновление
async def update_track(track_id: int, track_data: STracksUpdate):
    """Обновление существующего трека (можно обновить любое поле)"""
    try:
        updated_track = await TrackReposutory.update_one(track_id, track_data)
        if updated_track is None:
            raise HTTPException(status_code=404, detail=f"Track {track_id} not found")
        return updated_track
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{track_id}")  # DELETE - удаление
async def delete_track(track_id: int):
    """Удаление трека по ID"""
    try:
        deleted = await TrackReposutory.delete_one(track_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Track {track_id} not found")
        return {"message": f"Track {track_id} successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))