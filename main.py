import os

from fastapi import FastAPI, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from repository import TrackReposutory
from routers import router as tracks_router
from fastapi.middleware.cors import CORSMiddleware


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
app.mount("/data", StaticFiles(directory="data"), name="data")
if os.path.isdir("frontend_dist"):
    app.mount("/", StaticFiles(directory="frontend_dist", html=True), name="frontend")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5130",
        "http://127.0.0.1:5130",
        "http://localhost:5173",  # если используете другой порт
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # разрешаем все HTTP методы
    allow_headers=["*"],  # разрешаем все заголовки
)


class STracksAdd(BaseModel):
        name: str
        description: str | None = None


class STracks(BaseModel):
        id: int
        name: str
        description: str | None = None
