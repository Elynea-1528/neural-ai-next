"""CoreComponents tesztelése.

Ez a modul tartalmazza a CoreComponents osztály egységtesztjeit,
beleértve a komponens lekérdezést, beállítást és validálást.
"""

from unittest.mock import MagicMock

from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.base.implementations.di_container import DIContainer


class TestCoreComponents:
    """CoreComponents osztály tesztjei."""

    def test_init_with_container(self) -> None:
        """Teszteli a komponensek inicializálását meglévő konténerrel."""
        container: DIContainer = DIContainer()
        components: CoreComponents = CoreComponents(container)

        # A konténer átadás megtörtént, ezt a has_logger-en keresztül ellenőrizzük
        assert components.logger is None  # Üres konténer

    def test_init_without_container(self) -> None:
        """Teszteli a komponensek inicializálását új konténerrel."""
        components: CoreComponents = CoreComponents()

        # Alapértelmezetten üres a konténer
        assert not components.has_logger()
        assert not components.has_config()

    def test_config_property_none(self) -> None:
        """Teszteli a config property-t ha nincs config komponens."""
        components: CoreComponents = CoreComponents()

        assert components.config is None

    def test_config_property_with_instance(self) -> None:
        """Teszteli a config property-t ha van config komponens."""
        components: CoreComponents = CoreComponents()
        mock_config: MagicMock = MagicMock()
        components.set_config(mock_config)

        assert components.config is mock_config

    def test_logger_property_none(self) -> None:
        """Teszteli a logger property-t ha nincs logger komponens."""
        components: CoreComponents = CoreComponents()

        assert components.logger is None

    def test_logger_property_with_instance(self) -> None:
        """Teszteli a logger property-t ha van logger komponens."""
        components: CoreComponents = CoreComponents()
        mock_logger: MagicMock = MagicMock()
        components.set_logger(mock_logger)

        assert components.logger is mock_logger

    def test_storage_property_none(self) -> None:
        """Teszteli a storage property-t ha nincs storage komponens."""
        components: CoreComponents = CoreComponents()

        assert components.storage is None

    def test_storage_property_with_instance(self) -> None:
        """Teszteli a storage property-t ha van storage komponens."""
        components: CoreComponents = CoreComponents()
        mock_storage: MagicMock = MagicMock()
        components.set_storage(mock_storage)

        assert components.storage is mock_storage

    def test_database_property_none(self) -> None:
        """Teszteli a database property-t ha nincs database komponens."""
        components: CoreComponents = CoreComponents()

        assert components.database is None

    def test_database_property_with_instance(self) -> None:
        """Teszteli a database property-t ha van database komponens."""
        components: CoreComponents = CoreComponents()
        mock_database: MagicMock = MagicMock()
        components.set_database(mock_database)

        assert components.database is mock_database

    def test_event_bus_property_none(self) -> None:
        """Teszteli a event_bus property-t ha nincs event_bus komponens."""
        components: CoreComponents = CoreComponents()

        assert components.event_bus is None

    def test_event_bus_property_with_instance(self) -> None:
        """Teszteli a event_bus property-t ha van event_bus komponens."""
        components: CoreComponents = CoreComponents()
        mock_event_bus: MagicMock = MagicMock()
        components.set_event_bus(mock_event_bus)

        assert components.event_bus is mock_event_bus

    def test_hardware_property_none(self) -> None:
        """Teszteli a hardware property-t ha nincs hardware komponens."""
        components: CoreComponents = CoreComponents()

        assert components.hardware is None

    def test_hardware_property_with_instance(self) -> None:
        """Teszteli a hardware property-t ha van hardware komponens."""
        components: CoreComponents = CoreComponents()
        mock_hardware: MagicMock = MagicMock()
        components.set_hardware(mock_hardware)

        assert components.hardware is mock_hardware

    def test_has_config_false(self) -> None:
        """Teszteli a has_config metódust ha nincs config."""
        components: CoreComponents = CoreComponents()

        assert not components.has_config()

    def test_has_config_true(self) -> None:
        """Teszteli a has_config metódust ha van config."""
        components: CoreComponents = CoreComponents()
        mock_config: MagicMock = MagicMock()
        components.set_config(mock_config)

        assert components.has_config()

    def test_has_logger_false(self) -> None:
        """Teszteli a has_logger metódust ha nincs logger."""
        components: CoreComponents = CoreComponents()

        assert not components.has_logger()

    def test_has_logger_true(self) -> None:
        """Teszteli a has_logger metódust ha van logger."""
        components: CoreComponents = CoreComponents()
        mock_logger: MagicMock = MagicMock()
        components.set_logger(mock_logger)

        assert components.has_logger()

    def test_has_storage_false(self) -> None:
        """Teszteli a has_storage metódust ha nincs storage."""
        components: CoreComponents = CoreComponents()

        assert not components.has_storage()

    def test_has_storage_true(self) -> None:
        """Teszteli a has_storage metódust ha van storage."""
        components: CoreComponents = CoreComponents()
        mock_storage: MagicMock = MagicMock()
        components.set_storage(mock_storage)

        assert components.has_storage()

    def test_has_database_false(self) -> None:
        """Teszteli a has_database metódust ha nincs database."""
        components: CoreComponents = CoreComponents()

        assert not components.has_database()

    def test_has_database_true(self) -> None:
        """Teszteli a has_database metódust ha van database."""
        components: CoreComponents = CoreComponents()
        mock_database: MagicMock = MagicMock()
        components.set_database(mock_database)

        assert components.has_database()

    def test_has_event_bus_false(self) -> None:
        """Teszteli a has_event_bus metódust ha nincs event_bus."""
        components: CoreComponents = CoreComponents()

        assert not components.has_event_bus()

    def test_has_event_bus_true(self) -> None:
        """Teszteli a has_event_bus metódust ha van event_bus."""
        components: CoreComponents = CoreComponents()
        mock_event_bus: MagicMock = MagicMock()
        components.set_event_bus(mock_event_bus)

        assert components.has_event_bus()

    def test_has_hardware_false(self) -> None:
        """Teszteli a has_hardware metódust ha nincs hardware."""
        components: CoreComponents = CoreComponents()

        assert not components.has_hardware()

    def test_has_hardware_true(self) -> None:
        """Teszteli a has_hardware metódust ha van hardware."""
        components: CoreComponents = CoreComponents()
        mock_hardware: MagicMock = MagicMock()
        components.set_hardware(mock_hardware)

        assert components.has_hardware()

    def test_validate_false_when_empty(self) -> None:
        """Teszteli a validate metódust üres komponensekkel."""
        components: CoreComponents = CoreComponents()

        assert not components.validate()

    def test_validate_true_when_all_present(self) -> None:
        """Teszteli a validate metódust minden komponenssel."""
        components: CoreComponents = CoreComponents()
        components.set_config(MagicMock())
        components.set_logger(MagicMock())
        components.set_storage(MagicMock())
        components.set_database(MagicMock())
        components.set_event_bus(MagicMock())
        components.set_hardware(MagicMock())
        components.set_health_monitor(MagicMock())

        assert components.validate()

    def test_validate_false_when_some_missing(self) -> None:
        """Teszteli a validate metódust néhány hiányzó komponenssel."""
        components: CoreComponents = CoreComponents()
        components.set_config(MagicMock())
        components.set_logger(MagicMock())
        # storage, database, event_bus, hardware hiányzik

        assert not components.validate()

    def test_persister_property_none(self) -> None:
        """Teszteli a persister property-t ha nincs persister komponens."""
        components: CoreComponents = CoreComponents()

        assert components.persister is None

    def test_persister_property_with_instance(self) -> None:
        """Teszteli a persister property-t ha van persister komponens."""
        components: CoreComponents = CoreComponents()
        mock_persister: MagicMock = MagicMock()
        components.set_persister(mock_persister)

        assert components.persister is mock_persister

    def test_live_feed_property_none(self) -> None:
        """Teszteli a live_feed property-t ha nincs live_feed komponens."""
        components: CoreComponents = CoreComponents()

        assert components.live_feed is None

    def test_live_feed_property_with_instance(self) -> None:
        """Teszteli a live_feed property-t ha van live_feed komponens."""
        components: CoreComponents = CoreComponents()
        mock_live_feed: MagicMock = MagicMock()
        components.set_live_feed(mock_live_feed)

        assert components.live_feed is mock_live_feed

    def test_set_persister(self) -> None:
        """Teszteli a set_persister metódust."""
        components: CoreComponents = CoreComponents()
        mock_persister: MagicMock = MagicMock()
        components.set_persister(mock_persister)

        assert components.persister is mock_persister

    def test_set_live_feed(self) -> None:
        """Teszteli a set_live_feed metódust."""
        components: CoreComponents = CoreComponents()
        mock_live_feed: MagicMock = MagicMock()
        components.set_live_feed(mock_live_feed)

        assert components.live_feed is mock_live_feed

    def test_has_persister_false(self) -> None:
        """Teszteli a has_persister metódust ha nincs persister."""
        components: CoreComponents = CoreComponents()

        assert not components.has_persister()

    def test_has_persister_true(self) -> None:
        """Teszteli a has_persister metódust ha van persister."""
        components: CoreComponents = CoreComponents()
        mock_persister: MagicMock = MagicMock()
        components.set_persister(mock_persister)

        assert components.has_persister()

    def test_has_live_feed_false(self) -> None:
        """Teszteli a has_live_feed metódust ha nincs live_feed."""
        components: CoreComponents = CoreComponents()

        assert not components.has_live_feed()

    def test_has_live_feed_true(self) -> None:
        """Teszteli a has_live_feed metódust ha van live_feed."""
        components: CoreComponents = CoreComponents()
        mock_live_feed: MagicMock = MagicMock()
        components.set_live_feed(mock_live_feed)

        assert components.has_live_feed()
