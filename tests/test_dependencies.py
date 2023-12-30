from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_mctools.dependencies import Dependency, create_simple_form_dependency
from pydantic import BaseModel
import pytest


class DB(BaseModel):
    test: str


class User(BaseModel):
    id: int
    name: str


class Some(BaseModel):
    id: int
    data: str


async def get_user(db: DB) -> User:
    return User(id=1, name="John")


async def get_some_things_of_user(db: DB) -> Some:
    return Some(id=1, data="something")


@pytest.fixture
def dependency():
    return Dependency(
        GetUser=get_user,
        GetSomeThingsOfUser=get_some_things_of_user,
    )


@pytest.fixture
def client(dependency):
    app = FastAPI()

    @app.post("/users/{user_id}")
    async def run_something_about_user(
        user: dependency.GetUser, some: dependency.GetSomeThingsOfUser
    ):
        user = user.id == 1
        some = some.id == 1
        return {"user": user, "some": some}

    return TestClient(app)


def test_dependency_instance(dependency):
    assert isinstance(dependency, Dependency)


def test_run_something_about_user(client):
    response = client.post("/users/1", json={"test": "test"})
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "some" in data
    assert data["user"] is True
    assert data["some"] is True


def test_create_simple_form_dependency():
    input = {
        "username": str,
        "password": str,
        "age": int,
    }
    FastAPIForm = create_simple_form_dependency(input)
    assert "FastAPIForm" in locals()
