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
    """
    Collects and executes startup/shutdown events for the application.
    """

    def __init__(self) -> None:
        self.events = []

    def add_event(self, event: Event, *args, **kwargs) -> None:
        """
        Add an event (function or coroutine) to the executor.
        """
        self.events.append((event, args, kwargs))

    async def run(self) -> None:
        """
        Run all registered events in order. Await if coroutine, call if sync.
        """
        for event, args, kwargs in self.events:
            if asyncio.iscoroutinefunction(event):
                await event(*args, **kwargs)
            else:
                event(*args, **kwargs)


class Lifespan:
    """
    Context manager and event system for managing application startup and shutdown events.

    Example:
        lifespan = Lifespan()
        lifespan.add_startup(startup_func)
        lifespan.add_shutdown(shutdown_func)
        async with lifespan:
            ...
    """

    def __init__(self, timeout: int | None = None) -> None:
        """
        Initialize the Lifespan manager.
        :param timeout: Optional timeout (seconds) for startup/shutdown events.
        """
        self.startup_events = EventExecutor()
        self.shutdown_runner = EventExecutor()
        self.timeout = timeout
        self.__states = None

    def add_startup(self, event: Event, *args, **kwargs) -> None:
        """
        Register a function/coroutine to run on application startup.
        """
        self.startup_events.add_event(event, *args, **kwargs)

    def add_shutdown(self, event: Event, *args, **kwargs) -> None:
        """
        Register a function/coroutine to run on application shutdown.
        """
        self.shutdown_runner.add_event(event, *args, **kwargs)

    @property
    def states(self) -> State:
        """
        Get the current states dictionary (if set).
        """
        if self.__states is not None and not isinstance(self.__states, dict):
            raise ValueError("States must be a dictionary or None")
        return self.__states

    @states.setter
    def states(self, value: State) -> None:
        """
        Set the states dictionary or a callable returning a dictionary.
        """
        if isinstance(value, Callable):
            self.__states = value()
        else:
            self.__states = value

    async def __aenter__(self) -> "Lifespan":
        """
        Enter the lifespan context, running all startup events.
        """
        if self.timeout:
            async with asyncio.timeout(self.timeout):
                await self.startup_events.run()
        else:
            await self.startup_events.run()
        return self

    async def __aexit__(self, exc_type: _ExceptionType, exc: _Exception, tb: _TracebackType) -> None:
        """
        Exit the lifespan context, running all shutdown events.
        """
        if self.timeout:
            async with asyncio.timeout(self.timeout):
                await self.shutdown_runner.run()
        else:
            await self.shutdown_runner.run()
        return None

    async def lifespan(self, app: ASGIApp) -> AsyncGenerator[Any, Any]:
        """
        ASGI lifespan protocol integration. Use as FastAPI lifespan context.
        """
        await self.__aenter__()
        try:
            yield self.states
        finally:
            await self.__aexit__(None, None, None)
