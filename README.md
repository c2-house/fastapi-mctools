# FastAPI-MCtools

- MC(나)의 FastAPI로 개발할 때 자주 사용하는 코드들을 모아놓은 패키지입니다.
- This is a package that contains frequently used codes when developing with FastAPI by MC(me).
- [블로그](https://chaechae.life/blog/fastapi-my-library) 소개글 참고

## Installation

```bash
pip install fastapi-mctools
```

## Usage

### CLI

### 1. run

- run uvicorn server for development
- this command will find `main.py` and run uvicorn server
- use this command when running in local environment

```bash
mct run dev
```

### 2. startproject

- create a new FastAPI project in ordinary way

```bash
mct startproject
```

### 3. gunicorn

- make gunicorn basic config

```bash
mct gunicorn
```

### 4. types

- check all functions if existing missing type hint
- this command will find all functions in the file or directory and check if there is any missing type hint
- use this if you are very strict about type hinting

```bash
mct types <path: directory or file>
```

## DB Session

- DB, AsyncDB
- when you want to make db session in the fast way, use this

```python
from fastapi_mctools.db import DB, AsyncDB

get_db = DB(db_url)
get_db = AsyncDB(db_url)
```

## Request Logging Middleware

- RequestLoggingMiddleware
- when you simply want to log all requests, use this
- you can use log configuration by dictConfig or fileConfig

```python
# main.py
import logging
from fastapi import FastAPI
from fastapi_mctools.middlewares import RequestLoggingMiddleware

app = FastAPI()

logger = logging.getLogger('request')

app.add_middleware(RequestLoggingMiddleware, logger=logger)
```

### SQLAlchemy ORM

- sync_base, async_base
- these are kind of repositories for frequently used ORM operations, such as CRUD
- if not putting any column name, it will use all columns in the model

```python
from fastapi_mctools.orms import sync_base, async_base

class UserCreate(async_base.ACreateBase):
    ...


class UserRead(async_base.AReadBase):
    ...


class UserUpdate(async_base.AUpdateBase):
    ...

class UserDelete(async_base.ADeleteBase):
    ...

class UserRepository(UserCreate, UserRead, UserUpdate, UserDelete):
    def __init__(self, model: SqlalchemyModel) -> None:
        super().__init__(model=model)


user_repository = UserRepository(model=User)

# AsyncSession from sqlalchemy.ext.asyncio
async def create_user(db: AsyncSession, data: dict) -> User:
    return await user_repository.create(db, **data)

async def read_user(db: AsyncSession, user_id: int) -> User:
    user =  await user_repository.get(db, user_id)
    users = await user_repository.get_all_by_filters(db, age=20)
    users_ages = await user_repository.get_all_by_filters(db, age=20, columns=['age'])
    users_in = await user_repository.get_all_in(db, column='age', values=[20, 21]) # if you want to use not in, make `_not=True`
    users_like = await user_repository.get_all_like(db, column='name', value='mc')
    ...

# update and delete are similar to create and read
```

## TestTools

- db_managers
- when you want to test with db and set up and tear down db in very simple way

```python
# conftest.py
from fastapi_mctools.test_tools.db_managers import TestConfDBManager

db_test_manager = TestConfDBManager(TEST_DB_URL)

@pytest.fixture
async def db():
    # Base is your sqlalchemy base
    async for session in db_test_manager.get_async_db_session(base=Base, is_meta=True):
        yield session


# test_something.py

async def test_something(db):
    # db is your test db session
    ...
```

## dependencies

- Dependency
- this is a class that can be used as a dependency manager that can handle multiple dependencies in an single instance
- so you can only import one instance even if there are many dependencies

```python
async def temp_dep_1():
    return 1

async def temp_dep_2():
    return 2

async def temp_dep_3():
    return 3

temp_dep = Dependency(
    TempDep1=temp_dep_1,
    TempDep2=temp_dep_2,
    TempDep3=temp_dep_3
)

# in your route

@app.get('/temp_1')
async def temp_1(result: temp_dep.TempDep1):
    return result

@app.get('/temp_2')
async def temp_2(result: temp_dep.TempDep2):
    return result

@app.get('/temp_3')
async def temp_3(result: temp_dep.TempDep3):
    return result

```

- create_simple_form_dependency
- this is developed to avoid the tedious task of repeatedly writing out the Form.
- especially when you make api with file upload, you can use this to make it simple

```python
from fastapi_mctools.dependencies import create_simple_form_dependency

simple_form_params ={
    "name": str,
    "age": int,
    "address": str,
    "email": str,
    "status": str,
    "memo": str,
}
form_data = create_simple_form_dependency(simple_form_params)

@app.post("/user")
def create_user(form_data: FastAPIForm = Depends(), file: UploadFile = File()):
    return form_data
```

## Requests

## Responses

## time

## exceptions
