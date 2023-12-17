from fastapi import FastAPI
from src.database.SQLITE import SampleDb
from pypox.database import createAsyncEngine, init_database_async, getAsyncEngine

createAsyncEngine(SampleDb, "aiosqlite")


async def __call__(app: FastAPI):
    await init_database_async(getAsyncEngine(SampleDb), SampleDb)
