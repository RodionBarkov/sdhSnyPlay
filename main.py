from fastapi import FastAPI, Depends, APIRouter
from typing import Annotated
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from repository import TrackReposutory
from routers import router as tracks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
#     await delete_tables()
#     print("База очищена")
#     await create_tables()
    print("База готова")
    yield
    print("Выключение")



app = FastAPI(lifespan=lifespan)
app.include_router(tracks_router)


class STracksAdd(BaseModel):
        name: str
        description: str | None = None


class STracks(BaseModel):
        id: int
        name: str
        description: str | None = None
