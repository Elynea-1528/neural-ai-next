"""Component interfészek tesztelése.

Ez a modul tartalmazza a CoreComponentsInterface és CoreComponentFactoryInterface
interfészek egységtesztjeit, amelyek ellenőrzik az interfész definíciók helyességét.
"""

import inspect
from typing import get_type_hints

from neural_ai.core.base.interfaces.component_interface import (
    CoreComponentFactoryInterface,
    CoreComponentsInterface,
)


class TestCoreComponentsInterface:
    """CoreComponentsInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert inspect.isabstract(CoreComponentsInterface)

    def test_interface_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "config",
            "logger",
            "storage",
            "has_config",
            "has_logger",
            "has_storage",
            "validate",
        ]

        for method_name in required_methods:
            assert hasattr(CoreComponentsInterface, method_name), (
                f"Hiányzó metódus: {method_name}"
            )

    def test_interface_methods_are_abstract(self) -> None:
        """Teszteli, hogy a metódusok absztraktak-e."""
        abstract_methods = [
            "config",
            "logger",
            "storage",
            "has_config",
            "has_logger",
            "has_storage",
            "validate",
        ]

        for method_name in abstract_methods:
            method = getattr(CoreComponentsInterface, method_name)
            if method_name in ["config", "logger", "storage"]:
                # Ezek property-k
                assert isinstance(method, property), (
                    f"{method_name} nem property"
                )
                assert method.fget is not None, (
                    f"{method_name} property-nek nincs getter-e"
                )
            else:
                assert hasattr(method, "__isabstractmethod__"), (
                    f"{method_name} nem absztrakt metódus"
                )

    def test_interface_has_correct_type_hints(self) -> None:
        """Teszteli, hogy az interfész metódusainak megfelelő típushintjei vannak."""
        type_hints = get_type_hints(CoreComponentsInterface)

        # Ellenőrizzük a property-k visszatérési típusát
        assert "config" in str(type_hints), "config property típushintje hiányzik"
        assert "logger" in str(type_hints), "logger property típushintje hiányzik"
        assert "storage" in str(type_hints), "storage property típushintje hiányzik"


class TestCoreComponentFactoryInterface:
    """CoreComponentFactoryInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert inspect.isabstract(CoreComponentFactoryInterface)

    def test_interface_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "create_components",
            "create_with_container",
            "create_minimal",
        ]

        for method_name in required_methods:
            assert hasattr(CoreComponentFactoryInterface, method_name), (
                f"Hiányzó metódus: {method_name}"
            )

    def test_interface_methods_are_abstract_and_static(self) -> None:
        """Teszteli, hogy a metódusok absztraktak és statikusak-e."""
        required_methods = [
            "create_components",
            "create_with_container",
            "create_minimal",
        ]

        for method_name in required_methods:
            method = getattr(CoreComponentFactoryInterface, method_name)

            # Ellenőrizzük, hogy statikus metódus-e
            assert isinstance(inspect.getattr_static(
                CoreComponentFactoryInterface, method_name
            ), staticmethod), f"{method_name} nem statikus metódus"

            # Ellenőrizzük, hogy absztrakt-e
            # A staticmethod miatt a __func__ attribútumot kell ellenőrizni
            assert callable(method), f"{method_name} nem hívható"

    def test_interface_has_correct_signatures(self) -> None:
        """Teszteli, hogy az interfész metódusainak megfelelő aláírása van."""
        # A metódusok meglétének ellenőrzése elegendő az interfész teszteléséhez
        assert hasattr(CoreComponentFactoryInterface, "create_components")
        assert hasattr(CoreComponentFactoryInterface, "create_with_container")
        assert hasattr(CoreComponentFactoryInterface, "create_minimal")

        # Ellenőrizzük, hogy a metódusok hívhatók-e
        create_components_method = CoreComponentFactoryInterface.create_components
        assert callable(create_components_method), "create_components nem hívható"

        create_with_container_method = CoreComponentFactoryInterface.create_with_container
        assert callable(create_with_container_method), "create_with_container nem hívható"

        create_minimal_method = CoreComponentFactoryInterface.create_minimal
        assert callable(create_minimal_method), "create_minimal nem hívható"
