# FastAPI-MCtools

- MC(나)의 FastAPI로 개발할 때 자주 사용하는 코드들을 모아놓은 패키지입니다.
- This is a package that contains frequently used codes when developing with FastAPI by MC(me).
- This is kind of an utility package
- [블로그](https://chaechae.life/blog/fastapi-my-library) 소개글 참고

## Installation

```bash
pip install fastapi-mctools
```

## Usage

### CLI

### 1-1. run dev

- run uvicorn server for development, this command wraps uvicorn command.
- this command will find `main.py` and run uvicorn server
- use this command when running in local environment and use --port and --host for setting port and host. default is 8000 and 127.0.0.1

```bash
mct run dev
```

### 1-2. run prod

- run gunicorn server for production, this command wraps gunicorn command.
- this command will find `gunicorn.config.py` and run gunicorn server
- if not existing `gunicorn.config.py`, it will make basic gunicorn config file

```bash
mct run prod
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

### 5. shell

- simple ipython shell
- need to install ipython

```bash
mct shell
```

```python
# in ipython shell
# need to import session that made by generator or async generator

# sync session
from app.session import get_db
db = next(get_db())

# async session
from app.session import get_db
db = await anxet(get_db())

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
- can use filterbackend for filtering data

```python
from fastapi_mctools.orms.sqlalchemy import sync_base, async_base
from fastapi_mctools.orms.filters import FilterBackend

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
    user =  await user_repository.get_by_id(db, user_id)
    users = await user_repository.get_by_filters(db, age=20) # This will return data for users whose age is 20.
    ...

async def read_user_with_filterbackend(db: AsyncSession, user_id: int) -> User:
    filter_backend = FilterBackend()
    filter_backend.set_model(User)
    filter_backend.add_filter({"age": 20})
    filter_backend.add_filter({"name": "%test%"})
    users = await user_repository.get_by_filters(db, filter_backend=filter_backend) # This will return data for users whose age is 20 and name contains "test"
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
async def temp_1(result: temp_dep.TempDep1): # temp_dep[0] is possible
    return result

@app.get('/temp_2')
async def temp_2(result: temp_dep.TempDep2): # temp_dep[1] is possible
    return result

@app.get('/temp_3')
async def temp_3(result: temp_dep.TempDep3): # temp_dep[2] is possible
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

- APIClient
- this is a class that can be used to make requests to external APIs only asynchronously
- you can keep the session alive and reuse it
- I normally use this in the lifespan of the app

```python
from fastapi_mctools.utils.requests import APIClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        api_client = APIClient()
        await api_client.start()
        states["api_client"] = api_client
        logger.info(f"Start App: states {states}, Debug: {app_settings.DEBUG}")
        yield
        await api_client.close()
    except Exception as e:
        raise e
```

## Responses

- ResponseInterFace
- this is an interface that can unify the response format ex) {"results" : data, "message": message, "status": status}
- it's not compatible with `response_model` in router.

```python
from fastapi_mctools.utils.responses import ResponseInterFace


async def get_user(user_id: int) -> ResponseInterFace:
    user = await user_repository.get(user_id)
    if user:
        return ResponseInterFace(result=user, message="Success", temp_response_1="temp1", temp_response_2="temp2", status=200)
    return ResponseInterFace(result=None, message="Not Found", temp_response_1="temp1", temp_response_2="temp2", status=404)


from pydantic import BaseModel

class UserResponse(BaseModel)
    # Let's assume that the model is defined
    ...

@router.get("/user/{user_id}")
async def get_user(user_id: int):
    ...
    response = ResponseInterFace(result=user, message="Success", temp_response_1="temp1", temp_response_2="temp2", status=200)
    return UserResponse(**response)
```

## time

- time_checker
- this is a decorator that can be used to check orm query time

```python

from fastapi_mctools.utils.time import time_checker

@time_checker(debug=True, logger=logger)
class SomeRepository:
    def get(self, db: AsyncSession, id: int) -> SomeModel:
        ...

temp = SomeRepository()
temp.get(db, 1)  # SomeRepository.get took 0.01 ms
```

## exceptions

- HTTPException, handle_http_exception, handle_500_exception
- HTTPException is a class that can be used instead of FastAPI's HTTPException, you can add more information to the exception response
- handle_http_exception is exception handler that can be used to handle HTTPException, if you want to add more information with HTTPException, add this handler to app
- handle_500_exception is exception handler that can be used to handle 500 error, it converts Exception to HTTPException and returns it

```python
from fastapi_mctools.exceptions import HTTPException, handle_http_exception, handle_500_exception

async def temp_api():
    raise HTTPException(status_code=400, detail="Bad Request", more_info="more info", code="TEMP_ERROR")

app.add_exception_handler(HTTPException, handle_http_exception)
```

## Lifespan

- Lifespan is the class that can be used to manage the startup and shutdown of the app
- Just make lifespan simple by using class

```python
from fastapi_mctools.lifespan import Lifespan
from fastapi import FastAPI

async def async_hello(name):
    print(f"Hello async world, {name}")

def get_states():
    return {
        "state_1": "state_1",
        "state_2": "state_2"
    }

lifespan = Lifespan()
lifespan.add_startup(print, "Hello world")
lifespan.add_startup(async_hello, name="mingke")
lifespan.add_shutdown(print, "Goodbye world")
lifespan.states = get_states

app = FastAPI(lifespan = lifespan.lifespan)

```
