"""Unit tesztek a neural_ai.core.config.interfaces __init__ modulhoz.

Ez a modul teszteli a config interfaces modul publikus API-ját és exportált interfészeit.
"""


class TestConfigInterfacesModuleExports:
    """Tesztek a config interfaces modul exportálásához."""

    def test_interfaces_module_exports_config_manager_interface(self) -> None:
        """Ellenőrzi, hogy az interfaces modul exportálja a ConfigManagerInterface-t."""
        # When
        from neural_ai.core.config.interfaces import ConfigManagerInterface

        # Then
        assert ConfigManagerInterface is not None

    def test_interfaces_module_exports_factory_interface(self) -> None:
        """Ellenőrzi, hogy az interfaces modul exportálja a ConfigManagerFactoryInterface-t."""
        # When
        from neural_ai.core.config.interfaces import ConfigManagerFactoryInterface

        # Then
        assert ConfigManagerFactoryInterface is not None

    def test_interfaces_module_exports_pydantic_types(self) -> None:
        """Ellenőrzi, hogy az interfaces modul exportálja a Pydantic típusokat."""
        # When
        from neural_ai.core.config.interfaces import (
            CollectorsConfig,
            ConfigSchema,
            DatabaseConfig,
            EventsConfig,
            LoggingConfig,
            ProcessorsConfig,
            StorageConfig,
            SystemConfig,
        )

        # Then
        assert SystemConfig is not None
        assert StorageConfig is not None
        assert ProcessorsConfig is not None
        assert LoggingConfig is not None
        assert DatabaseConfig is not None
        assert EventsConfig is not None
        assert CollectorsConfig is not None
        assert ConfigSchema is not None

    def test_interfaces_module_all_exports(self) -> None:
        """Ellenőrzi, hogy a __all__ lista tartalmazza az összes exportált elemet."""
        # When
        from neural_ai.core.config.interfaces import __all__

        # Then
        expected_exports = [
            "ConfigManagerInterface",
            "ConfigManagerFactoryInterface",
            "SystemConfig",
            "StorageConfig",
            "ProcessorsConfig",
            "LoggingConfig",
            "DatabaseConfig",
            "EventsConfig",
            "CollectorsConfig",
            "ConfigSchema",
        ]
        assert set(__all__) == set(expected_exports)


class TestConfigManagerInterfaceMethods:
    """Tesztek a ConfigManagerInterface metódusaihoz."""

    def test_config_manager_interface_has_get_method(self) -> None:
        """Ellenőrzi, hogy a ConfigManagerInterface tartalmazza a get metódust."""
        # When
        from neural_ai.core.config.interfaces import ConfigManagerInterface

        # Then
        assert hasattr(ConfigManagerInterface, "get")

    def test_config_manager_interface_has_get_section_method(self) -> None:
        """Ellenőrzi, hogy a ConfigManagerInterface tartalmazza a get_section metódust."""
        # When
        from neural_ai.core.config.interfaces import ConfigManagerInterface

        # Then
        assert hasattr(ConfigManagerInterface, "get_section")


    def test_config_manager_interface_has_validate_method(self) -> None:
        """Ellenőrzi, hogy a ConfigManagerInterface tartalmazza a validate metódust."""
        # When
        from neural_ai.core.config.interfaces import ConfigManagerInterface

        # Then
        assert hasattr(ConfigManagerInterface, "validate")


class TestConfigManagerFactoryInterfaceMethods:
    """Tesztek a ConfigManagerFactoryInterface metódusaihoz."""

    def test_factory_interface_has_create_manager_method(self) -> None:
        """Ellenőrzi, hogy a ConfigManagerFactoryInterface tartalmazza a create_manager metódust."""
        # When
        from neural_ai.core.config.interfaces import ConfigManagerFactoryInterface

        # Then
        assert hasattr(ConfigManagerFactoryInterface, "create_manager")


class TestPydanticConfigModels:
    """Tesztek a Pydantic config modellekhez."""

    def test_system_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a SystemConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces import SystemConfig

        # Then
        assert issubclass(SystemConfig, BaseModel)

    def test_storage_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a StorageConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces import StorageConfig

        # Then
        assert issubclass(StorageConfig, BaseModel)

    def test_processors_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a ProcessorsConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces import ProcessorsConfig

        # Then
        assert issubclass(ProcessorsConfig, BaseModel)

    def test_logging_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a LoggingConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces import LoggingConfig

        # Then
        assert issubclass(LoggingConfig, BaseModel)

    def test_database_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a DatabaseConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces import DatabaseConfig

        # Then
        assert issubclass(DatabaseConfig, BaseModel)

    def test_events_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy az EventsConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces import EventsConfig

        # Then
        assert issubclass(EventsConfig, BaseModel)

    def test_collectors_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a CollectorsConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces import CollectorsConfig

        # Then
        assert issubclass(CollectorsConfig, BaseModel)

    def test_config_schema_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a ConfigSchema Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces import ConfigSchema

        # Then
        assert issubclass(ConfigSchema, BaseModel)
