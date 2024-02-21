from contextlib import asynccontextmanager
from enum import Enum
import os
from typing import List, Union
from fastapi import APIRouter, FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException, ExceptionMiddleware
from pydantic import BaseModel
from mongoengine import *
import motor.motor_asyncio

from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.router import restaurants as restaurants_router, users as users_router
from app.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"])
db = client.get_database("wanteat")
restaurant_collection = db.get_collection("restaurants")
user_collection = db.get_collection("users")


app = FastAPI(
    title="Wanteat API",
)
origins = ['https://localhost:3000', 'https://localhost:8000']

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

app.include_router(restaurants_router.router, prefix="/restaurants")
app.include_router(users_router.router, prefix="/users")

""" @asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
        app.mongodb = app.mongodb_client[settings.DB_NAME]
        yield
    finally:
        app.mongodb_client.close() """
    
if __name__ == '__main__':
    uvicorn.run(
        app,
        host = settings.HOST,
        reload = settings.DEBUG_MODE,
        port = settings.PORT
    )