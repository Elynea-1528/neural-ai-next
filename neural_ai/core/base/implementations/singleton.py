"""Singleton metaclass megvalósítása a singleton tervezési minta biztosításához.

Ez a modul egy metaclass-t biztosít, amely garantálja, hogy minden osztályból,
ami ezt a metaclass-t használja, csak egyetlen példány létezzen az alkalmazás
életciklusa során.
"""

from abc import ABCMeta
from typing import TYPE_CHECKING, TypeVar, cast

from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.utils.decorators import trace

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces import LoggerInterface

T = TypeVar("T")


class SingletonMeta(ABCMeta):
    """Singleton minta megvalósítására szolgáló metaclass.

    Ez a metaclass biztosítja, hogy egy osztályból csak egy példány létezzen.
    A létrehozott példányokat egy osztályszintű szótárban tárolja, és minden
    következő példányosításnál ezt adja vissza.

    Attribútumok:
        _instances: Osztályszintű szótár, amely tárolja a singleton példányokat.
            A kulcs az osztály, az érték pedig a létrehozott példány.

    Példa:
        >>> class MyClass(metaclass=SingletonMeta):
        ...     def __init__(self, value: int):
        ...         self.value = value
        ...
        >>> obj1 = MyClass(42)
        >>> obj2 = MyClass(100)
        >>> obj1 is obj2
        True
        >>> obj1.value
        42
    """

    _instances: dict[type, object] = {}
    _logger: "LoggerInterface" = LoggerFactory.get_logger(__name__)
    _instance: object

    @trace
    def __call__(cls: type[T], *args: object, **kwargs: object) -> T:
        """Singleton példány létrehozása vagy visszaadása.

        Ha az osztály még nem szerepel a _instances szótárban, létrehoz egy új
        példányt és eltárolja. Ellenkező esetben a meglévő példányt adja vissza.

        DI Container kompatibilitás érdekében beállítja az _initialized és _instance
        attribútumokat.

        Args:
            cls: Az osztály, amelyből példányt szeretnénk létrehozni.
            *args: Pozicionális argumentumok az osztály konstruktorához.
            **kwargs: Kulcsszavas argumentumok az osztály konstruktorához.

        Returns:
            A létrehozott vagy meglévő singleton példány.

        Példa:
            >>> class Database(metaclass=SingletonMeta):
            ...     def __init__(self, connection_string: str):
            ...         self.connection_string = connection_string
            ...
            >>> db1 = Database("sqlite:///mydb.db")
            >>> db2 = Database("postgresql://localhost/mydb")
            >>> obj1 is obj2
            True
            >>> db1.connection_string
            'sqlite:///mydb.db'
        """
        # Biztosítjuk, hogy a _instances mindig dict legyen (teszt fixture védelem)
        if not hasattr(cls, '_instances') or cls._instances is None:
            cls._instances = {}  # type: ignore[attr-defined]
        
        if cls not in cls._instances:  # type: ignore[attr-defined]
            # Példány létrehozása
            instance = super().__call__(*args, **kwargs)  # type: ignore[misc]

            # 1. DI Container követelmény: _initialized flag
            instance._initialized = True

            # 2. DI Container követelmény: _instance class variable
            # (Bár a dict-ben tároljuk, a DI ellenőrzés ezt is keresi)
            cls._instance = instance  # type: ignore[attr-defined]

            cls._instances[cls] = instance  # type: ignore[attr-defined]

            # Singleton inicializálás logolása
            cls._logger.info(  # type: ignore[attr-defined]
                "Singleton példány inicializálva",
                extra={"class_name": cls.__name__},
            )
        return cast(T, cls._instances[cls])  # type: ignore[attr-defined]

    @classmethod
    def reset_singleton(cls, target_cls: type) -> None:
        """Singleton példány resetelése tesztelés céljából.

        Args:
            target_cls: Az osztály, amelynek singleton példányát resetelni kell.
        """
        if target_cls in cls._instances:
            del cls._instances[target_cls]
        if hasattr(cls, "_instance"):
            cls._instance = None
