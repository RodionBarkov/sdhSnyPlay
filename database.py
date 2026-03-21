from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

engine = create_async_engine(
    "sqlite+aiosqlite:///music.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class TrackOrm(Model):
    __tablename__ = "Track"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False) 
    description: Mapped[Optional[str]] = mapped_column(nullable=True) 
    cover_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    audio_url: Mapped[str] = mapped_column(nullable=False)
    lyrics: Mapped[Optional[str]] = mapped_column(nullable=True)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
        

        


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)