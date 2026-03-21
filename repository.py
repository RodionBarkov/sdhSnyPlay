from database import new_session, TrackOrm
from schemas import STracksAdd, STracks
from sqlalchemy import select


class TrackReposutory:
    @classmethod
    async def add_one(cls, data: STracksAdd) -> STracks:
        async with new_session() as session:
            track_dict = data.model_dump()
            track = TrackOrm(**track_dict)
            session.add(track)
            await session.flush()
            await session.commit()
            await session.refresh(track)
            
            
            return STracks(
                id=track.id,
                name=track.name,
                description=track.description,
                cover_url=track.cover_url,
                audio_url=track.audio_url,
                lyrics=track.lyrics
            )

    @classmethod 
    async def find_all(cls) -> list[STracks]:
        async with new_session() as session:
            query = select(TrackOrm)
            result = await session.execute(query)
            track_models = result.scalars().all()
            
            # Преобразуем ORM модели в Pydantic схемы
            track_schemas = []
            for track in track_models:
                track_schema = STracks(
                    id=track.id,
                    name=track.name,
                    description=track.description,
                    cover_url=track.cover_url,
                    audio_url=track.audio_url,
                    lyrics=track.lyrics
                )
                track_schemas.append(track_schema)
            
            return track_schemas
        
    @classmethod 
    async def find_by_id(cls, track_id: int) -> STracks | None:
        async with new_session() as session:
            query = select(TrackOrm).where(TrackOrm.id == track_id)
            result = await session.execute(query)
            track_model = result.scalar_one_or_none()  # Получаем один объект или None
            
            if track_model is None:
                return None
            
            # Преобразуем ORM модель в Pydantic схему
            track_schema = STracks(
                id=track_model.id,
                name=track_model.name,
                description=track_model.description,
                cover_url=track_model.cover_url,
                audio_url=track_model.audio_url,
                lyrics=track_model.lyrics
            )
            
            return track_schema