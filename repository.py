from database import new_session, TrackOrm
from schemas import STracksAdd, STracks, STracksUpdate
from sqlalchemy import select, update, delete

class TrackReposutory:
    @classmethod
    async def add_one(cls, data: STracksAdd) -> STracks:
        """Добавление нового трека"""
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
        """Получение всех треков"""
        async with new_session() as session:
            query = select(TrackOrm)
            result = await session.execute(query)
            track_models = result.scalars().all()
            
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
        """Получение трека по ID"""
        async with new_session() as session:
            query = select(TrackOrm).where(TrackOrm.id == track_id)
            result = await session.execute(query)
            track_model = result.scalar_one_or_none()
            
            if track_model is None:
                return None
            
            track_schema = STracks(
                id=track_model.id,
                name=track_model.name,
                description=track_model.description,
                cover_url=track_model.cover_url,
                audio_url=track_model.audio_url,
                lyrics=track_model.lyrics
            )
            
            return track_schema
    
    @classmethod
    async def update_one(cls, track_id: int, data: STracksUpdate) -> STracks | None:
        """Обновление существующего трека"""
        async with new_session() as session:
            # Сначала проверяем, существует ли трек
            query = select(TrackOrm).where(TrackOrm.id == track_id)
            result = await session.execute(query)
            track_model = result.scalar_one_or_none()
            
            if track_model is None:
                return None
            
            # Обновляем только те поля, которые были переданы
            update_data = data.model_dump(exclude_unset=True)  # exclude_unset исключает None значения
            
            if update_data:
                # Применяем обновления
                update_query = update(TrackOrm).where(TrackOrm.id == track_id).values(**update_data)
                await session.execute(update_query)
                await session.commit()
                
                # Получаем обновленный трек
                return await cls.find_by_id(track_id)
            
            # Если нет данных для обновления, возвращаем текущий трек
            return await cls.find_by_id(track_id)
    
    @classmethod
    async def delete_one(cls, track_id: int) -> bool:
        """Удаление трека по ID"""
        async with new_session() as session:
            # Проверяем, существует ли трек
            query = select(TrackOrm).where(TrackOrm.id == track_id)
            result = await session.execute(query)
            track_model = result.scalar_one_or_none()
            
            if track_model is None:
                return False
            
            # Удаляем трек
            delete_query = delete(TrackOrm).where(TrackOrm.id == track_id)
            await session.execute(delete_query)
            await session.commit()
            
            return True