"""Unit tesztek a ConfigLoaderFactory-hoz.

Ez a modul tartalmazza a ConfigLoaderFactory osztály unit tesztjeit:
- Interface visszaadási tesztek
- Custom paraméterek átadása
- Lazy loading működés

Arrange-Act-Assert pattern alapján.
"""

from typing import cast

from neural_ai.core.config.factory import ConfigLoaderFactory
from neural_ai.core.config.implementations.config_loader import ConfigLoader
from neural_ai.core.config.interfaces.config_loader_interface import IConfigLoader


class TestConfigLoaderFactory:
    """ConfigLoaderFactory tesztek."""

    def test_create_loader_returns_interface(self) -> None:
        """Teszt: create_loader() IConfigLoader példányt ad vissza.

        ARRANGE: Factory osztály.
        ACT: create_loader() hívása.
        ASSERT: IConfigLoader interface implementációja visszaadva.
        """
        # ACT
        loader = ConfigLoaderFactory.create_loader()

        # ASSERT
        assert isinstance(loader, IConfigLoader)

    def test_create_loader_with_custom_sops_binary(self) -> None:
        """Teszt: Custom SOPS binary átadása.

        ARRANGE: Factory osztály, custom SOPS binary útvonal.
        ACT: create_loader() hívása custom paraméterrel.
        ASSERT: SOPS binary az átadott érték (cast implementációra).
        """
        # ACT
        loader = ConfigLoaderFactory.create_loader(sops_binary="/custom/sops")

        # ASSERT
        impl = cast(ConfigLoader, loader)
        assert impl._sops_binary == "/custom/sops"

    def test_lazy_loading(self) -> None:
        """Teszt: Lazy loading működik (implementáció betöltése).

        ARRANGE: Factory osztály, _loader_type reset.
        ACT: create_loader() hívása.
        ASSERT: _loader_type betöltődik és IConfigLoader példány jön létre.
        """
        # ARRANGE
        ConfigLoaderFactory._loader_type = None  # pyright: ignore[reportPrivateUsage]

        # ACT
        loader = ConfigLoaderFactory.create_loader()

        # ASSERT
        assert ConfigLoaderFactory._loader_type is not None  # pyright: ignore[reportPrivateUsage]
        assert isinstance(loader, IConfigLoader)
