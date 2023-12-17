import pytest
import httpx
from fastapi.testclient import TestClient
from fastapi import status
from faker import Faker
from src.main import app  # import your FastAPI instance

fake = Faker()

SIZE = 100
users = {}  # Dictionary to store the created users


@pytest.mark.asyncio
async def test_read_main():
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as async_client:
        response = await async_client.get("/api/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_read_users():
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as async_client:
        response = await async_client.get("/api/user/")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)


@pytest.mark.asyncio
async def test_create_user():
    for _ in range(SIZE):
        user_data = {
            "name": fake.name(),
            "fullname": fake.name(),
        }
        async with httpx.AsyncClient(
            app=app, base_url="http://testserver"
        ) as async_client:
            response = await async_client.post("/api/user/", json=user_data)
            assert (
                response.status_code == status.HTTP_200_OK
                or response.status_code == status.HTTP_409_CONFLICT
            )

        users[user_data["name"]] = user_data  # Store the created user in the dictionary


@pytest.mark.asyncio
async def test_read_user():
    for name, user in users.items():
        async with httpx.AsyncClient(
            app=app, base_url="http://testserver"
        ) as async_client:
            response = await async_client.get(f"/api/user/{name}/")
            assert response.status_code == status.HTTP_200_OK
            assert set(response.json().keys()) == {"fullname", "id", "name"}
