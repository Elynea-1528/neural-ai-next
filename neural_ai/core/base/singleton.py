"""Singleton metaclass megvalósítása a singleton tervezési minta biztosításához.

Ez a modul egy metaclass-t biztosít, amely garantálja, hogy minden osztályból,
ami ezt a metaclass-t használja, csak egyetlen példány létezzen az alkalmazás
életciklusa során.
"""

from typing import TypeVar, cast

T = TypeVar("T")


class SingletonMeta(type):
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

    def __call__(cls: type[T], *args: object, **kwargs: object) -> T:
        """Singleton példány létrehozása vagy visszaadása.

        Ha az osztály még nem szerepel a _instances szótárban, létrehoz egy új
        példányt és eltárolja. Ellenkező esetben a meglévő példányt adja vissza.

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
        if cls not in cls._instances:  # type: ignore[attr-defined]
            instance = super().__call__(*args, **kwargs)  # type: ignore[misc]
            cls._instances[cls] = instance  # type: ignore[attr-defined]
        return cast(T, cls._instances[cls])  # type: ignore[attr-defined]
