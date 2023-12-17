from sqlalchemy import Row
from src.database.SQLITE import SampleDb
from pypox.database import asyncDbSession, AsyncSession
from src.api.user.schemas import User
from sqlmodel import select
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from sqlalchemy.engine.result import Result


async def endpoint() -> dict[str, list[SampleDb.User]]:
    db: AsyncSession = await asyncDbSession(SampleDb)
    await db.begin()
    try:
        statement = select(SampleDb.User)
        result = (await db.execute(statement)).all()
        if not result:
            raise NoResultFound("No user found!")
        return {"data": [x[0] for x in result]}
    except NoResultFound as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )
    finally:
        await db.close()
