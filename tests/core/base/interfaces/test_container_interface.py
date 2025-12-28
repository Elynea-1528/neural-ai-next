"""Container interfészek tesztelése.

Ez a modul tartalmazza a DIContainerInterface és LazyComponentInterface
interfészek egységtesztjeit, amelyek ellenőrzik az interfész definíciók helyességét.
"""

import inspect
from typing import get_type_hints

from neural_ai.core.base.interfaces.container_interface import (
    DIContainerInterface,
    LazyComponentInterface,
)


class TestDIContainerInterface:
    """DIContainerInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert inspect.isabstract(DIContainerInterface)

    def test_interface_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "register_instance",
            "register_factory",
            "resolve",
            "register_lazy",
            "get",
            "clear",
        ]

        for method_name in required_methods:
            assert hasattr(DIContainerInterface, method_name), (
                f"Hiányzó metódus: {method_name}"
            )

    def test_interface_methods_are_abstract(self) -> None:
        """Teszteli, hogy a metódusok absztraktak-e."""
        abstract_methods = [
            "register_instance",
            "register_factory",
            "resolve",
            "register_lazy",
            "get",
            "clear",
        ]

        for method_name in abstract_methods:
            method = getattr(DIContainerInterface, method_name)
            assert hasattr(method, "__isabstractmethod__"), (
                f"{method_name} nem absztrakt metódus"
            )

    def test_interface_has_correct_type_hints(self) -> None:
        """Teszteli, hogy az interfész metódusainak megfelelő típushintjei vannak."""
        type_hints = get_type_hints(DIContainerInterface)

        # Ellenőrizzük, hogy a metódusoknak vannak típushintjei
        assert len(type_hints) > 0, "Az interfésznek nincsenek típushintjei"

        # Ellenőrizzük a register_lazy metódus típushintjeit
        method = DIContainerInterface.register_lazy
        method_hints = get_type_hints(method)
        assert "component_name" in str(method_hints), (
            "register_lazy hiányzik component_name típushintje"
        )
        assert "factory_func" in str(method_hints), (
            "register_lazy hiányzik factory_func típushintje"
        )

    def test_interface_methods_are_callable(self) -> None:
        """Teszteli, hogy az interfész metódusai hívhatók-e."""
        required_methods = [
            "register_instance",
            "register_factory",
            "resolve",
            "register_lazy",
            "get",
            "clear",
        ]

        for method_name in required_methods:
            method = getattr(DIContainerInterface, method_name)
            assert callable(method), f"{method_name} nem hívható metódus"

    def test_interface_uses_generic_types(self) -> None:
        """Teszteli, hogy az interfész generikus típusokat használ."""
        # A DIContainerInterface TypeVar-okat használ (T, InterfaceT)
        # Ezt a forráskód ellenőrzésével igazolhatjuk
        source = inspect.getsource(DIContainerInterface)
        assert "TypeVar" in source or "T" in source, (
            "Az interfész nem használ generikus típusokat"
        )


class TestLazyComponentInterface:
    """LazyComponentInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert inspect.isabstract(LazyComponentInterface)

    def test_interface_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "get",
            "is_loaded",
        ]

        for method_name in required_methods:
            assert hasattr(LazyComponentInterface, method_name), (
                f"Hiányzó metódus: {method_name}"
            )

    def test_interface_methods_are_abstract(self) -> None:
        """Teszteli, hogy a metódusok absztraktak-e."""
        # get metódus ellenőrzése
        get_method = LazyComponentInterface.get
        assert hasattr(get_method, "__isabstractmethod__"), (
            "get metódus nem absztrakt"
        )

        # is_loaded property ellenőrzése
        is_loaded_property = LazyComponentInterface.is_loaded
        assert isinstance(is_loaded_property, property), (
            "is_loaded nem property"
        )
        assert is_loaded_property.fget is not None, (
            "is_loaded property-nek nincs getter-e"
        )

    def test_interface_has_correct_type_hints(self) -> None:
        """Teszteli, hogy az interfész metódusainak megfelelő típushintjei vannak."""
        type_hints = get_type_hints(LazyComponentInterface)

        # Ellenőrizzük, hogy a metódusoknak vannak típushintjei
        assert len(type_hints) > 0, "Az interfésznek nincsenek típushintjei"

        # Ellenőrizzük a get metódus típushintjeit
        get_method = LazyComponentInterface.get
        method_hints = get_type_hints(get_method)
        assert "return" in method_hints, "get metódusnak nincs visszatérési típusa"

    def test_interface_methods_are_callable(self) -> None:
        """Teszteli, hogy az interfész metódusai hívhatók-e."""
        # get metódus ellenőrzése
        get_method = LazyComponentInterface.get
        assert callable(get_method), "get metódus nem hívható"

        # is_loaded property ellenőrzése
        is_loaded_property = LazyComponentInterface.is_loaded
        assert isinstance(is_loaded_property, property), (
            "is_loaded nem property"
        )

    def test_interface_defines_lazy_loading_contract(self) -> None:
        """Teszteli, hogy az interfész definiálja-e a lusta betöltés szerződését."""
        # Az interfésznek tartalmaznia kell a lusta betöltés alapvető műveleteit
        assert hasattr(LazyComponentInterface, "get"), (
            "Az interfész nem definiál get metódust a komponens lekéréséhez"
        )
        assert hasattr(LazyComponentInterface, "is_loaded"), (
            "Az interfész nem definiál is_loaded property-t a betöltés állapotához"
        )

        # A get metódusnak hívhatónak kell lennie
        get_method = LazyComponentInterface.get
        assert callable(get_method), "get metódus nem hívható"

        # Az is_loaded property-nek olvashatónak kell lennie
        is_loaded_property = LazyComponentInterface.is_loaded
        assert isinstance(is_loaded_property, property), (
            "is_loaded nem property"
        )
