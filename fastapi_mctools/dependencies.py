from typing import Annotated, Callable
from fastapi import Depends, Form  # noqa F401


class Dependency:
    """
    A class for managing FastAPI dependencies.
    Created to avoid the hassle of importing multiple dependencies in the endpoint.

    Usage:
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

    def __getitem__(self, index: int) -> Annotated:
        try:
            values = list(self.__dict__.values())[index]
            return values
        except IndexError:
            raise IndexError(f"{self.__class__.__name__} has only {len(self.__dict__)} dependency.")


def create_simple_form_dependency(input_dict: dict) -> type:
    """
    Creates a class for using FastAPI's Form.
    Developed to avoid the tedious task of repeatedly writing out the Form.
    It can be used as a class dependency.

    사용법:
        * input : type 형식으로 입력합니다.
        input = {
            "username": str,
            "password": str,
            "age": int,
        }
        FastAPIForm = create_fastapi_form_class(input)

        @app.post("/user")
        def create_user(form_data: FastAPIForm = Depends()):
            return form_data
    """

    init_params_str = ", ".join(f"{name}: {_type.__name__} = Form(...)" for name, _type in input_dict.items())
    init_body_str = "\n        ".join(f"self.{name} = {name}" for name in input_dict.keys())
    init_method_str = f"def __init__(self, {init_params_str}):\n        {init_body_str}"

    class_def_str = f"class FastAPIForm:\n    {init_method_str}"

    namespace = {}
    exec(class_def_str, globals(), namespace)
    return namespace["FastAPIForm"]
