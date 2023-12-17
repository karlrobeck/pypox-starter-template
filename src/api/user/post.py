from fastapi import HTTPException, status
from src.database.SQLITE import SampleDb
from pypox.database import asyncDbSession, AsyncSession
from src.api.user.schemas import User
from uuid import uuid1
from sqlalchemy.exc import IntegrityError


async def endpoint(body: User):
    db: AsyncSession = await asyncDbSession(SampleDb)

    try:
        await db.begin()
        db.add(SampleDb.User(id=str(uuid1()), **body.model_dump()))
        await db.commit()
        return {"message": "Successfully added to database!"}
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    finally:
        await db.close()
