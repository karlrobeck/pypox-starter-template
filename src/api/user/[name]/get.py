from src.database.SQLITE import SampleDb
from pypox.database import asyncDbSession, AsyncSession
from src.api.user.schemas import User
from sqlmodel import select
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status


async def endpoint(name: str) -> SampleDb.User:
    db: AsyncSession = await asyncDbSession(SampleDb)
    await db.begin()
    try:
        statement = select(SampleDb.User).where(SampleDb.User.name == name)
        result = (await db.execute(statement)).scalar()
        if not result:
            raise NoResultFound("No user found!")
        return result
    except NoResultFound as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e,
        )
    finally:
        await db.close()
