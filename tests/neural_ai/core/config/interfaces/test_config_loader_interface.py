"""Unit tesztek az IConfigLoader interfészhez.

Ez a modul tartalmazza az IConfigLoader interface unit tesztjeit:
- Abstract class ellenőrzés
- Metódus definíció validálás
- Interface契約 betartás

Arrange-Act-Assert pattern alapján.
"""

import pytest

from neural_ai.core.config.interfaces.config_loader_interface import IConfigLoader


class TestIConfigLoaderInterface:
    """IConfigLoader interfész tesztek."""

    def test_interface_is_abstract(self) -> None:
        """Teszt: IConfigLoader abstract class.

        ARRANGE: IConfigLoader osztály.
        ACT & ASSERT: Példányosítás TypeError-t dob (abstract methods miatt).
        """
        # ACT & ASSERT
        with pytest.raises(TypeError):
            IConfigLoader()  # type: ignore[abstract]

    def test_interface_has_load_method(self) -> None:
        """Teszt: load() metódus definiálva.

        ARRANGE: IConfigLoader osztály.
        ACT: Metódus lekérés.
        ASSERT: load() metódus létezik és callable.
        """
        # ASSERT
        assert hasattr(IConfigLoader, "load")
        assert callable(getattr(IConfigLoader, "load"))

    def test_interface_has_load_file_method(self) -> None:
        """Teszt: load_file() metódus definiálva.

        ARRANGE: IConfigLoader osztály.
        ACT: Metódus lekérés.
        ASSERT: load_file() metódus létezik és callable.
        """
        # ASSERT
        assert hasattr(IConfigLoader, "load_file")
        assert callable(getattr(IConfigLoader, "load_file"))
