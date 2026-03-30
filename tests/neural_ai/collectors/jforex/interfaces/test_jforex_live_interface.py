"""Unit tesztek a JForex Live Interface-hez."""

import pytest

from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed


class ConcreteLiveFeed(ILiveFeed):
    """Teszt implementáció az ILiveFeed interfészhez."""

    def __init__(self) -> None:
        """Inicializálja a teszt live feed-et."""
        self._running = False

    async def start(self) -> None:
        """Teszt implementáció."""
        self._running = True

    async def stop(self) -> None:
        """Teszt implementáció."""
        self._running = False

    def is_running(self) -> bool:
        """Teszt implementáció."""
        return self._running


class TestILiveFeed:
    """Tesztek az ILiveFeed interfészhez."""

    def test_interface_is_abstract(self) -> None:
        """Ellenőrzi, hogy az interfész absztrakt osztály."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            ILiveFeed()  # type: ignore[abstract]

    def test_concrete_implementation_can_be_instantiated(self) -> None:
        """Ellenőrzi, hogy konkrét implementáció példányosítható."""
        # Arrange & Act
        feed = ConcreteLiveFeed()

        # Assert
        assert isinstance(feed, ILiveFeed)

    @pytest.mark.asyncio
    async def test_start_signature(self) -> None:
        """Ellenőrzi a start metódus szignatúráját."""
        # Arrange
        feed = ConcreteLiveFeed()

        # Act
        await feed.start()

        # Assert
        assert feed.is_running()

    @pytest.mark.asyncio
    async def test_stop_signature(self) -> None:
        """Ellenőrzi a stop metódus szignatúráját."""
        # Arrange
        feed = ConcreteLiveFeed()
        await feed.start()

        # Act
        await feed.stop()

        # Assert
        assert not feed.is_running()

    def test_is_running_signature(self) -> None:
        """Ellenőrzi az is_running metódus szignatúráját."""
        # Arrange
        feed = ConcreteLiveFeed()

        # Act
        result = feed.is_running()

        # Assert
        assert isinstance(result, bool)
        assert not result

    def test_interface_has_all_required_methods(self) -> None:
        """Ellenőrzi, hogy az interfész tartalmazza az összes szükséges metódust."""
        # Arrange
        required_methods = ["start", "stop", "is_running"]

        # Act & Assert
        for method_name in required_methods:
            assert hasattr(ILiveFeed, method_name)
            assert callable(getattr(ILiveFeed, method_name))

    @pytest.mark.asyncio
    async def test_lifecycle(self) -> None:
        """Ellenőrzi a teljes életciklust: start -> running -> stop."""
        # Arrange
        feed = ConcreteLiveFeed()

        # Act & Assert - Kezdeti állapot
        assert not feed.is_running()

        # Act & Assert - Start után
        await feed.start()
        assert feed.is_running()

        # Act & Assert - Stop után
        await feed.stop()
        assert not feed.is_running()
