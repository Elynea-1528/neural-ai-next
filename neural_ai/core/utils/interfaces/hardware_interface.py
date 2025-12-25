"""Hardverinformációk lekérdezéséhez szükséges interfész.

Ez a modul az `HardwareInterface` absztrakt alaposztályt definiálja,
amely a hardver-specifikus képességek (CPU feature-ök) lekérdezését
standardizálja a rendszerben.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class HardwareInterface(ABC):
    """Absztrakt interfész a hardverinformációk lekérdezéséhez.

    Ez az interfész definiálja azokat a metódusokat, amelyeket a
    hardverdetektáló osztályoknak implementálniuk kell. A cél a
    hardver-specifikus képességek (mint az AVX2, SIMD) biztonságos
    és egységes lekérdezése.
    """

    @abstractmethod
    def has_avx2(self) -> bool:
        """Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

        Returns:
            bool: True, ha a CPU támogatja az AVX2-t, False egyébként.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cpu_features(self) -> set[str]:
        """Visszaadja a CPU által támogatott összes feature flag-et.

        Returns:
            set[str]: A CPU által támogatott feature flag-ek halmaza.
        """
        raise NotImplementedError

    @abstractmethod
    def supports_simd(self) -> bool:
        """Ellenőrzi, hogy a CPU támogatja-e az alapvető SIMD utasításokat.

        Returns:
            bool: True, ha a CPU támogatja az alapvető SIMD utasításokat.
        """
        raise NotImplementedError