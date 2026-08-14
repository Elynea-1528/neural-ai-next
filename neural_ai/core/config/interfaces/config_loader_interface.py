"""Konfiguráció betöltő interfész SOPS támogatással.

Ez a modul definiálja a
[`IConfigLoader`](neural_ai/core/config/interfaces/config_loader_interface.py:11)
interfészt, amely biztosítja a titkosított (SOPS) és titkosítatlan YAML
konfigurációk egységes betöltését.
"""

from abc import ABC, abstractmethod
from typing import Any


class IConfigLoader(ABC):
    """Konfiguráció betöltő interfész SOPS és egyszerű YAML fájlokhoz.

    Ez az interfész biztosítja a titkosított (SOPS) és titkosítatlan YAML
    konfigurációk egységes betöltését.
    """

    @abstractmethod
    def load(self, config_dir: str) -> dict[str, Any]:
        """Betölti az összes config fájlt egy könyvtárból.

        A fájlneveket (kiterjesztés nélkül) használja kulcsként, és a tartalmukat
        az adott kulcs alá tölti be namespace struktúrába.

        Args:
            config_dir: Konfiguráció könyvtár útvonala

        Returns:
            Egyesített konfiguráció dictionary (namespace struktúra)

        Raises:
            ConfigLoadError: Ha a könyvtár nem található
            SOPSDecryptError: Ha a SOPS dekódolás sikertelen
        """

    @abstractmethod
    def load_file(self, file_path: str) -> dict[str, Any]:
        """Betölt egyetlen config fájlt (SOPS vagy plain YAML).

        Automatikusan detektálja a .yaml.sops kiterjesztést és SOPS
        dekódolást alkalmaz szükség esetén.

        Args:
            file_path: Fájl útvonala (.yaml vagy .yaml.sops)

        Returns:
            Fájl tartalma dictionary formában

        Raises:
            ConfigLoadError: Ha fájl nem található
            SOPSDecryptError: Ha SOPS fájl dekódolása sikertelen
        """
