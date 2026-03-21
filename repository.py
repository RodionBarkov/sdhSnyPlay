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