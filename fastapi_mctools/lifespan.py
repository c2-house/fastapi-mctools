import asyncio
from typing import Callable, Coroutine, Union, Any, Optional, Type, AsyncGenerator
from types import TracebackType
from starlette.types import ASGIApp


Event = Union[Callable, Coroutine[Any, Any, Any]]
State = Union[dict, Callable]
_ExceptionType = Optional[Type[BaseException]]
_Exception = Optional[BaseException]
_TracebackType = Optional[TracebackType]


class EventExecutor:
    def __init__(self) -> None:
        self.events = []

    def add_event(self, event: Event, *args, **kwargs) -> None:
        self.events.append((event, args, kwargs))

    async def run(self) -> None:
        for event, args, kwargs in self.events:
            if asyncio.iscoroutinefunction(event):
                await event(*args, **kwargs)
            else:
                event(*args, **kwargs)


class Lifespan:
    def __init__(self, timeout: int | None = None) -> None:
        self.startup_events = EventExecutor()
        self.shutdown_runner = EventExecutor()
        self.timeout = timeout
        self.__states = None

    def add_startup(self, event: Event, *args, **kwargs) -> None:
        self.startup_events.add_event(event, *args, **kwargs)

    def add_shutdown(self, event: Event, *args, **kwargs) -> None:
        self.shutdown_runner.add_event(event, *args, **kwargs)

    @property
    def states(self) -> State:
        if self.__states is not None and not isinstance(self.__states, dict):
            raise ValueError("States must be a dictionary or None")
        return self.__states

    @states.setter
    def states(self, value: State) -> None:
        if isinstance(value, Callable):
            self.__states = value()
        else:
            self.__states = value

    async def __aenter__(self) -> "Lifespan":
        if self.timeout:
            async with asyncio.timeout(self.timeout):
                await self.startup_events.run()
        else:
            await self.startup_events.run()
        return self

    async def __aexit__(self, exc_type: _ExceptionType, exc: _Exception, tb: _TracebackType) -> None:
        if self.timeout:
            async with asyncio.timeout(self.timeout):
                await self.shutdown_runner.run()
        else:
            await self.shutdown_runner.run()
        return None

    async def lifespan(self, app: ASGIApp) -> AsyncGenerator[Any, Any]:
        await self.__aenter__()
        try:
            yield self.states
        finally:
            await self.__aexit__(None, None, None)
