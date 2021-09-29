import sys
from _typeshed import Self
from types import TracebackType
from typing import (
    IO,
    Any,
    AsyncContextManager,
    AsyncIterator,
    Awaitable,
    Callable,
    ContextManager,
    Iterator,
    Optional,
    Type,
    TypeVar,
    overload,
)
from typing_extensions import ParamSpec, Protocol

AbstractContextManager = ContextManager
if sys.version_info >= (3, 7):
    AbstractAsyncContextManager = AsyncContextManager

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_T_io = TypeVar("_T_io", bound=Optional[IO[str]])
_P = ParamSpec("_P")

_ExitFunc = Callable[[Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]], bool]
_CM_EF = TypeVar("_CM_EF", ContextManager[Any], _ExitFunc)

class _GeneratorContextManager(ContextManager[_T_co]):
    def __call__(self, func: Callable[_P, Any]) -> Callable[_P, Any]: ...  # type: ignore

# type ignore to deal with incomplete ParamSpec support in mypy
def contextmanager(func: Callable[_P, Iterator[_T]]) -> Callable[_P, _GeneratorContextManager[_T]]: ...  # type: ignore

if sys.version_info >= (3, 7):
    def asynccontextmanager(func: Callable[_P, AsyncIterator[_T]]) -> Callable[_P, AsyncContextManager[_T]]: ...  # type: ignore

class _SupportsClose(Protocol):
    def close(self) -> object: ...

_SupportsCloseT = TypeVar("_SupportsCloseT", bound=_SupportsClose)

class closing(ContextManager[_SupportsCloseT]):
    def __init__(self, thing: _SupportsCloseT) -> None: ...

if sys.version_info >= (3, 10):
    class _SupportsAclose(Protocol):
        def aclose(self) -> Awaitable[object]: ...
    _SupportsAcloseT = TypeVar("_SupportsAcloseT", bound=_SupportsAclose)
    class aclosing(AsyncContextManager[_SupportsAcloseT]):
        def __init__(self, thing: _SupportsAcloseT) -> None: ...
    class AsyncContextDecorator:
        def __call__(self, func: Callable[_P, Awaitable[Any]]) -> Callable[_P, Awaitable[Any]]: ...  # type: ignore

class suppress(ContextManager[None]):
    def __init__(self, *exceptions: Type[BaseException]) -> None: ...
    def __exit__(
        self, exctype: Type[BaseException] | None, excinst: BaseException | None, exctb: TracebackType | None
    ) -> bool: ...

class redirect_stdout(ContextManager[_T_io]):
    def __init__(self, new_target: _T_io) -> None: ...

class redirect_stderr(ContextManager[_T_io]):
    def __init__(self, new_target: _T_io) -> None: ...

class ContextDecorator:
    def __call__(self, func: Callable[_P, Any]) -> Callable[_P, Any]: ...  # type: ignore

class ExitStack(ContextManager[ExitStack]):
    def __init__(self) -> None: ...
    def enter_context(self, cm: ContextManager[_T]) -> _T: ...
    def push(self, exit: _CM_EF) -> _CM_EF: ...
    def callback(self, callback: Callable[_P, Any], *args: Any, **kwds: Any) -> Callable[_P, Any]: ...  # type: ignore
    def pop_all(self: Self) -> Self: ...
    def close(self) -> None: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(
        self, __exc_type: Type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None
    ) -> bool: ...

if sys.version_info >= (3, 7):
    _ExitCoroFunc = Callable[[Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]], Awaitable[bool]]
    _CallbackCoroFunc = Callable[_P, Awaitable[Any]]  # type: ignore
    _ACM_EF = TypeVar("_ACM_EF", AsyncContextManager[Any], _ExitCoroFunc)
    class AsyncExitStack(AsyncContextManager[AsyncExitStack]):
        def __init__(self) -> None: ...
        def enter_context(self, cm: ContextManager[_T]) -> _T: ...
        def enter_async_context(self, cm: AsyncContextManager[_T]) -> Awaitable[_T]: ...
        def push(self, exit: _CM_EF) -> _CM_EF: ...
        def push_async_exit(self, exit: _ACM_EF) -> _ACM_EF: ...
        def callback(self, callback: Callable[_P, Any], *args: Any, **kwds: Any) -> Callable[_P, Any]: ...  # type: ignore
        def push_async_callback(self, callback: _CallbackCoroFunc, *args: Any, **kwds: Any) -> _CallbackCoroFunc: ...
        def pop_all(self: Self) -> Self: ...
        def aclose(self) -> Awaitable[None]: ...
        def __aenter__(self: Self) -> Awaitable[Self]: ...
        def __aexit__(
            self, __exc_type: Type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None
        ) -> Awaitable[bool]: ...

if sys.version_info >= (3, 10):
    class nullcontext(AbstractContextManager[_T], AbstractAsyncContextManager[_T]):
        enter_result: _T
        @overload
        def __init__(self: nullcontext[None], enter_result: None = ...) -> None: ...
        @overload
        def __init__(self: nullcontext[_T], enter_result: _T) -> None: ...
        def __enter__(self) -> _T: ...
        def __exit__(self, *exctype: Any) -> None: ...
        async def __aenter__(self) -> _T: ...
        async def __aexit__(self, *exctype: Any) -> None: ...

elif sys.version_info >= (3, 7):
    class nullcontext(AbstractContextManager[_T]):
        enter_result: _T
        @overload
        def __init__(self: nullcontext[None], enter_result: None = ...) -> None: ...
        @overload
        def __init__(self: nullcontext[_T], enter_result: _T) -> None: ...
        def __enter__(self) -> _T: ...
        def __exit__(self, *exctype: Any) -> None: ...
