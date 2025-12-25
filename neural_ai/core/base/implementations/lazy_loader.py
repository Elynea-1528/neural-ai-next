"""Lustatöltés (lazy loading) segédeszközök.

Ez a modul a lustatöltés mechanizmust valósítja meg, amely lehetővé teszi,
hogy a drága erőforrások csak akkor töltődjenek be, amikor valóban szükség van rájuk.
Ez jelentősen javítja az alkalmazás indítási idejét és a memóriahasználatot.
"""

import threading
from collections.abc import Callable
from typing import TypeVar, cast

T = TypeVar("T")

__all__ = ["LazyLoader", "lazy_property"]


class LazyLoader[T]:
    """Drága erőforrások lustatöltője.

    Ez az osztály lehetővé teszi, hogy a drága erőforrások (pl. konfigurációk,
    adatbázis kapcsolatok, nagy adathalmazok) csak akkor töltődjenek be,
    amikor valóban szükség van rájuk.

    A lustatöltés szálbiztos, így többszálú környezetben is biztonságosan
    használható.
    """

    def __init__(self, loader_func: Callable[[], T]) -> None:
        """Inicializálja a lustatöltőt.

        Args:
            loader_func: A függvény, amely betölti az erőforrást.
                Ennek a függvénynek vissza kell térnie a betöltött erőforrással.
        """
        self._loader_func = loader_func
        self._loaded: bool = False
        self._value: T | None = None
        self._lock = threading.RLock()

    def _load(self) -> T:
        """Betölti az erőforrást, ha még nincs betöltve.

        Returns:
            A betöltött erőforrás.

        Note:
            Ez egy belső metódus, általában nem kell közvetlenül használni.
            Ehelyett használd a __call__ metódust.
        """
        with self._lock:
            if not self._loaded:
                self._value = self._loader_func()
                self._loaded = True
                assert self._value is not None, "A betöltő függvény None értéket adott vissza"
        return cast(T, self._value)

    def __call__(self) -> T:
        """Visszaadja a betöltött erőforrást.

        Ha az erőforrás még nincs betöltve, először meghívja a betöltő függvényt.

        Returns:
            A betöltött erőforrás.
        """
        return self._load()

    @property
    def is_loaded(self) -> bool:
        """Ellenőrzi, hogy az erőforrás betöltve van-e.

        Returns:
            True, ha az erőforrás betöltve van, egyébként False.
        """
        return self._loaded

    def reset(self) -> None:
        """Visszaállítja a betöltőt az alaphelyzetbe.

        Ez kiüríti a betöltött erőforrást, lehetővé téve az újratöltést.
        Hasznos lehet tesztelés során vagy ha újra szeretnénk tölteni
        az erőforrást.
        """
        with self._lock:
            self._loaded = False
            self._value = None


def lazy_property[T](func: Callable[..., T]) -> property:
    """Dekorátor lustatöltésű property-k létrehozásához.

    Ez a dekorátor egy olyan property-t hoz létre, amelynek értéke csak
    az első hozzáféréskor számolódik ki, majd gyorsítótárba kerül.
    A későbbi hozzáférések már a gyorsítótárazott értéket adják vissza.

    Args:
        func: A függvény, amely kiszámolja a property értékét.

    Returns:
        Egy property objektum lustatöltéssel.

    Példa:
        >>> class DataProcessor:
        ...     def __init__(self, data):
        ...         self._data = data
        ...     @lazy_property
        ...     def processed_data(self):
        ...         # Ez a kód csak egyszer fut le
        ...         return [x * 2 for x in self._data]
        >>> processor = DataProcessor([1, 2, 3])
        >>> # A processed_data még nincs kiszámolva
        >>> result = processor.processed_data  # Most fut le először
        >>> result2 = processor.processed_data  # Már gyorsítótárból jön
    """
    attr_name = f"_lazy_{func.__name__}"

    def wrapper(instance: object) -> T:
        if not hasattr(instance, attr_name):
            value = func(instance)
            setattr(instance, attr_name, value)
        return cast(T, getattr(instance, attr_name))

    return property(wrapper)
