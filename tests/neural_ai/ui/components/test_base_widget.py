"""Unit tesztek a BaseWidget osztályhoz."""

from neural_ai.ui.components.base_widget import BaseWidget


class TestBaseWidget:
    """Tesztek a BaseWidget osztályhoz."""

    def test_initialization_without_config(self) -> None:
        """Teszteli a BaseWidget inicializálását konfiguráció nélkül."""
        widget = BaseWidget()

        assert widget._config == {}
        assert widget._visible is True

    def test_initialization_with_config(self) -> None:
        """Teszteli a BaseWidget inicializálását konfigurációval."""
        config: dict[str, object] = {"key": "value", "number": 42}
        widget = BaseWidget(config=config)

        assert widget._config == config
        assert widget._visible is True

    def test_initialization_with_none_config(self) -> None:
        """Teszteli a BaseWidget inicializálását None konfigurációval."""
        widget = BaseWidget(config=None)

        assert widget._config == {}
        assert widget._visible is True

    def test_render_returns_string(self) -> None:
        """Teszteli, hogy a render metódus string-et ad vissza."""
        widget = BaseWidget()

        result = widget.render()

        assert isinstance(result, str)
        assert result == "Base Widget"

    def test_show_sets_visible_to_true(self) -> None:
        """Teszteli, hogy a show metódus láthatóvá teszi a widget-et."""
        widget = BaseWidget()
        widget._visible = False

        widget.show()

        assert widget._visible is True

    def test_hide_sets_visible_to_false(self) -> None:
        """Teszteli, hogy a hide metódus elrejti a widget-et."""
        widget = BaseWidget()

        widget.hide()

        assert widget._visible is False

    def test_is_visible_property_returns_true_initially(self) -> None:
        """Teszteli, hogy az is_visible property kezdetben True-t ad vissza."""
        widget = BaseWidget()

        assert widget.is_visible is True

    def test_is_visible_property_after_hide(self) -> None:
        """Teszteli az is_visible property-t hide után."""
        widget = BaseWidget()

        widget.hide()

        assert widget.is_visible is False

    def test_is_visible_property_after_show(self) -> None:
        """Teszteli az is_visible property-t show után."""
        widget = BaseWidget()
        widget.hide()

        widget.show()

        assert widget.is_visible is True

    def test_show_hide_toggle(self) -> None:
        """Teszteli a show és hide metódusok váltakozó használatát."""
        widget = BaseWidget()

        assert widget.is_visible is True

        widget.hide()
        assert widget.is_visible is False

        widget.show()
        assert widget.is_visible is True

        widget.hide()
        assert widget.is_visible is False
