import time
import inspect
import functools
from logging import Logger
from typing import TypeVar, Type, Callable, Any, cast


T = TypeVar("T", bound=Callable[..., Any])
R = TypeVar("R")


def time_checker(
    debug: bool = False, logger: Logger = None
) -> Callable[[Type[T]], Type[T]]:
    """
    Async SQLAlchemy의 Query를 실행하는데 걸리는 시간을 측정합니다.

    :param debug: 디버그 모드를 활성화합니다. debug가 아니면 실행하지 않습니다.
    :param logger: 로거를 지정합니다. 지정하지 않으면 AttributeError가 발생합니다.

    example:

    @time_checker(debug=True, logger=logger)
    class SomeRepository:
        def get(self, db: AsyncSession, id: int) -> SomeModel:
            ...

    temp = SomeRepository()
    temp.get(db, 1)  # SomeRepository.get took 0.01 ms

    """

    if not logger:
        raise AttributeError("you must set logger!")

    def decorator(cls):
        if debug:
            for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
                if name != "__init__" and not name.startswith("_"):
                    setattr(cls, name, check(method))
        return cls

    def check(method: T) -> T:
        @functools.wraps(method)
        async def wrapper(*args: Any, **kwargs: Any) -> R:
            class_name = args[0].__class__.__name__
            start = time.time()
            result = await method(*args, **kwargs)
            end = time.time()
            logger.info(
                f"{class_name}.{method.__name__} took {(end - start) * 1000:.2f} ms"
            )
            return cast(R, result)

        return cast(T, wrapper)

    return decorator
