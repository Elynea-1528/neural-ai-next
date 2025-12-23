"""Logger interfész definíció a naplózási rendszer számára."""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import TYPE_CHECKING, AnyStr, Optional

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


class LoggerInterface(ABC):
    """Logger interfész a naplózási műveletek absztrakt definíciójához.

    Ez az interfész definiálja azokat a metódusokat, amelyeket minden logger
    implementációnak implementálnia kell a konzisztens naplózási viselkedés
    érdekében.
    """

    @abstractmethod
    def __init__(
        self,
        name: str,
        config: Optional["ConfigManagerInterface"] = None,
        **kwargs: Mapping[str, AnyStr],
    ) -> None:
        """Logger inicializálása.

        Args:
            name: A logger egyedi azonosítója.
            config: Opcionális konfigurációs interfész a logger beállításaihoz.
            **kwargs: További opcionális paraméterek (pl. file_path, level).
        """
        pass

    @abstractmethod
    def debug(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        """Debug szintű üzenet naplózása.

        Részletes hibakeresési információk naplózására szolgál, amelyek általában
        csak fejlesztés közben relevánsak.

        Args:
            message: A naplózandó üzenet szövege.
            **kwargs: További kontextusparaméterek (pl. extra, exc_info).
        """
        pass

    @abstractmethod
    def info(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        """Információs szintű üzenet naplózása.

        Általános információk naplózására szolgál, amelyek a rendszer normál
        működéséről adnak tájékoztatást.

        Args:
            message: A naplózandó üzenet szövege.
            **kwargs: További kontextusparaméterek (pl. extra, exc_info).
        """
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        """Figyelmeztető szintű üzenet naplózása.

        Olyan helyzetek naplózására szolgál, amelyek nem kritikusak, de
        figyelmet igényelnek.

        Args:
            message: A naplózandó üzenet szövege.
            **kwargs: További kontextusparaméterek (pl. extra, exc_info).
        """
        pass

    @abstractmethod
    def error(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        """Hiba szintű üzenet naplózása.

        Hibák naplózására szolgál, amelyek befolyásolják a rendszer működését,
        de nem okoznak alkalmazásleállást.

        Args:
            message: A naplózandó üzenet szövege.
            **kwargs: További kontextusparaméterek (pl. extra, exc_info).
        """
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        """Kritikus szintű üzenet naplózása.

        Súlyos hibák naplózására szolgál, amelyek alkalmazásleállást okozhatnak.

        Args:
            message: A naplózandó üzenet szövege.
            **kwargs: További kontextusparaméterek (pl. extra, exc_info).
        """
        pass

    @abstractmethod
    def set_level(self, level: int) -> None:
        """Logger naplózási szintjének beállítása.

        Beállítja a minimális naplózási szintet. A szintnél alacsonyabb
        prioritású üzenetek nem lesznek naplózva.

        Args:
            level: Az új naplózási szint (0-50 közötti egész szám).
        """
        pass

    @abstractmethod
    def get_level(self) -> int:
        """Aktuális naplózási szint lekérdezése.

        Returns:
            int: A jelenleg beállított naplózási szint értéke.
        """
        pass
