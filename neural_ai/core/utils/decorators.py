"""Funkcionális dekorátorok a Neural AI Next rendszerhez.

Ez a modul a rendszer által használt dekorátorokat tartalmazza, beleértve
a `@trace` dekorátort, amely funkcióhívások nyomon követését és logolását
teszi lehetővé structlog segítségével.
"""

import time
import uuid
from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING, ParamSpec, TypeVar, cast

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

# Típusváltozók a generikus típusokhoz
P = ParamSpec("P")
R = TypeVar("R")


# Logger inicializálása - késleltetett import elkerülése érdekében
def _get_trace_logger() -> "LoggerInterface":
    from neural_ai.core.logger.factory import LoggerFactory

    return LoggerFactory.get_logger("neural_ai.trace")


_trace_logger: "LoggerInterface | None" = None


def _ensure_trace_logger() -> "LoggerInterface":
    global _trace_logger
    if _trace_logger is None:
        _trace_logger = _get_trace_logger()
    return _trace_logger


# Biztonságos típusok halmaza
_SAFE_TYPES = (str, int, float, bool, type(None))


def _serialize_arg(arg: object) -> str:
    """Egy argumentum biztonságos szöveges reprezentációját adja vissza.

    Csak biztonságos típusokat (str, int, float, bool, None) konvertál
    közvetlenül, minden egyéb típus esetén "UNSAFE_ARG" értéket ad vissza.

    Args:
        arg: A konvertálandó argumentum.

    Returns:
        Az argumentum szöveges reprezentációja, vagy "UNSAFE_ARG" ha a
        típus nem biztonságos.
    """
    if isinstance(arg, _SAFE_TYPES):
        return str(arg)
    return "UNSAFE_ARG"


def trace(func: Callable[P, R]) -> Callable[P, R]:  # noqa: UP047
    """Dekorátor a funkcióhívások nyomon követéséhez és logolásához.

    A dekorátor minden függvényhíváskor logolja a következő információkat:
    - call_id: Egyedi azonosító (UUID4)
    - function: A hívott függvény neve
    - args: A függvény argumentumainak biztonságos reprezentációja
    - duration_ms: A függvény futási ideje milliszekundumban

    A logolás DEBUG szinten történik a "neural_ai.trace" loggeren keresztül.

    Args:
        func: A dekorálandó függvény.

    Returns:
        A dekorált függvény, amely automatikusan logolja a hívásokat.

    Examples:
        >>> @trace
        ... def add(a: int, b: int) -> int:
        ...     return a + b
        ...
        >>> result = add(5, 3)
        # Log output:
        # call_id=... function=add args=['5', '3'] duration_ms=0.123
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        """A dekorált függvényt becsomagoló wrapper függvény.

        Args:
            *args: Pozicionális argumentumok.
            **kwargs: Kulcsszavas argumentumok.

        Returns:
            A dekorált függvény visszatérési értéke.
        """
        # Egyedi hívásazonosító generálása
        call_id = str(uuid.uuid4())

        # Argumentumok biztonságos szerializálása
        safe_args: list[str] = [_serialize_arg(arg) for arg in args]
        safe_kwargs: dict[str, str] = {key: _serialize_arg(value) for key, value in kwargs.items()}

        # Időmérés indítása
        start_time = time.perf_counter()

        try:
            # Függvényhívás végrehajtása
            result = func(*args, **kwargs)

            # Futási idő kiszámítása
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Logolás a LoggerFactory-val
            _ensure_trace_logger().debug(
                "function_call",
                call_id=call_id,
                function=func.__name__,
                call_args=safe_args,
                call_kwargs=safe_kwargs,
                duration_ms=round(duration_ms, 3),
            )

            return result

        except Exception as e:
            # Hiba esetén is logoljuk az információkat
            duration_ms = (time.perf_counter() - start_time) * 1000

            _ensure_trace_logger().debug(
                "function_call_error",
                call_id=call_id,
                function=func.__name__,
                call_args=safe_args,
                call_kwargs=safe_kwargs,
                duration_ms=round(duration_ms, 3),
                error=str(e),
            )

            # A hiba továbbdobása
            raise

    return cast(Callable[P, R], wrapper)
