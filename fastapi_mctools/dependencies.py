from typing import Annotated, Callable
from fastapi import Depends


class Dependency:
    """
    FastAPI Depenedency를 관리하는 클래스입니다.
    Endpoint에서 필요한 Dependency 여러개 임포트하기 귀찮아서 만들었습니다.

    사용법:
    async def get_user(db: DB) -> User:
        ...
        return user

    async def get_some_things_of_user(db: DB) -> Some:
        ...
        return some

    user_dependency = Dependency(
        GetUser=get_user,
        GetSomeThingsOfUser=get_some_things_of_user,
    )

    @router.get("/users/{user_id}")
    async def run_something_about_user(user: user_dependency.GetUser, some: user_dependency.GetSomeThingsOfUser):
        ...
        return

    """

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if not isinstance(value, Callable):
                raise TypeError(f"{value}가 Callable하지 않습니다.")

            if not value.__annotations__.get("return"):
                raise AttributeError(f"{value}에 반환값 annotation이 없습니다.")

            return_type = value.__annotations__.get("return")
            value = Annotated[return_type, Depends(value)]
            setattr(self, key, value)
