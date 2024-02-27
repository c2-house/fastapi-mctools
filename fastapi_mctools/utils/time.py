import time
import inspect
import functools
from logging import Logger
from typing import TypeVar, Type, Callable, Any, cast


T = TypeVar("T", bound=Callable[..., Any])
R = TypeVar("R")


def time_checker(debug: bool = False, logger: Logger = None) -> Callable[[Type[T]], Type[T]]:
    """
    time checker decorator

    Measures the time taken to execute a query in Async SQLAlchemy.

    :param debug: Activates debug mode. If not in debug, it does not execute.
    :param logger: Specifies a logger. If not specified, an AttributeError occurs.


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
            logger.info(f"{class_name}.{method.__name__} took {(end - start) * 1000:.2f} ms")
            return cast(R, result)

        return cast(T, wrapper)

    return decorator
