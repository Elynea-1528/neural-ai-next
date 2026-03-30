"""Unit tesztek a neural_ai.core.config.interfaces.types modulhoz.

Ez a modul teszteli a Pydantic config típusokat és validációt.
"""

import pytest
from pydantic import ValidationError


class TestPydanticConfigTypesExist:
    """Tesztek a Pydantic config típusok létezéséhez."""

    def test_system_config_exists(self) -> None:
        """Ellenőrzi, hogy a SystemConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import SystemConfig

        # Then
        assert SystemConfig is not None

    def test_storage_config_exists(self) -> None:
        """Ellenőrzi, hogy a StorageConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import StorageConfig

        # Then
        assert StorageConfig is not None

    def test_processors_config_exists(self) -> None:
        """Ellenőrzi, hogy a ProcessorsConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import ProcessorsConfig

        # Then
        assert ProcessorsConfig is not None

    def test_logging_config_exists(self) -> None:
        """Ellenőrzi, hogy a LoggingConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import LoggingConfig

        # Then
        assert LoggingConfig is not None

    def test_database_config_exists(self) -> None:
        """Ellenőrzi, hogy a DatabaseConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import DatabaseConfig

        # Then
        assert DatabaseConfig is not None

    def test_events_config_exists(self) -> None:
        """Ellenőrzi, hogy az EventsConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import EventsConfig

        # Then
        assert EventsConfig is not None

    def test_collectors_config_exists(self) -> None:
        """Ellenőrzi, hogy a CollectorsConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import CollectorsConfig

        # Then
        assert CollectorsConfig is not None

    def test_config_schema_exists(self) -> None:
        """Ellenőrzi, hogy a ConfigSchema létezik."""
        # When
        from neural_ai.core.config.interfaces.types import ConfigSchema

        # Then
        assert ConfigSchema is not None


class TestPydanticBaseModelInheritance:
    """Tesztek a Pydantic BaseModel örökléshez."""

    def test_system_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a SystemConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces.types import SystemConfig

        # Then
        assert issubclass(SystemConfig, BaseModel)

    def test_storage_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a StorageConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces.types import StorageConfig

        # Then
        assert issubclass(StorageConfig, BaseModel)

    def test_processors_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a ProcessorsConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces.types import ProcessorsConfig

        # Then
        assert issubclass(ProcessorsConfig, BaseModel)

    def test_logging_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a LoggingConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces.types import LoggingConfig

        # Then
        assert issubclass(LoggingConfig, BaseModel)

    def test_database_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a DatabaseConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces.types import DatabaseConfig

        # Then
        assert issubclass(DatabaseConfig, BaseModel)

    def test_events_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy az EventsConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces.types import EventsConfig

        # Then
        assert issubclass(EventsConfig, BaseModel)

    def test_collectors_config_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a CollectorsConfig Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces.types import CollectorsConfig

        # Then
        assert issubclass(CollectorsConfig, BaseModel)

    def test_config_schema_is_pydantic_model(self) -> None:
        """Ellenőrzi, hogy a ConfigSchema Pydantic BaseModel."""
        # When
        from pydantic import BaseModel

        from neural_ai.core.config.interfaces.types import ConfigSchema

        # Then
        assert issubclass(ConfigSchema, BaseModel)


class TestPydanticValidation:
    """Tesztek a Pydantic validációhoz."""

    def test_handler_config_validates_level_pattern(self) -> None:
        """Ellenőrzi, hogy a HandlerConfig validálja a level pattern-t."""
        # When
        from neural_ai.core.config.interfaces.types import HandlerConfig

        # Then - invalid level should raise ValidationError
        with pytest.raises(ValidationError):
            HandlerConfig(level="INVALID_LEVEL")  # pyright: ignore[reportCallIssue]

    def test_paths_config_validates_min_length(self) -> None:
        """Ellenőrzi, hogy a PathsConfig validálja a min_length-et."""
        # When
        from neural_ai.core.config.interfaces.types import PathsConfig

        # Then - empty string should raise ValidationError
        with pytest.raises(ValidationError):
            PathsConfig(data="")  # pyright: ignore[reportCallIssue]

    def test_handler_config_validates_max_bytes_positive(self) -> None:
        """Ellenőrzi, hogy a HandlerConfig validálja a max_bytes pozitív értékét."""
        # When
        from neural_ai.core.config.interfaces.types import HandlerConfig

        # Then - negative value should raise ValidationError
        with pytest.raises(ValidationError):
            HandlerConfig(max_bytes=-1)  # pyright: ignore[reportCallIssue]

    def test_handler_config_validates_backup_count_non_negative(self) -> None:
        """Ellenőrzi, hogy a HandlerConfig validálja a backup_count nem-negatív értékét."""
        # When
        from neural_ai.core.config.interfaces.types import HandlerConfig

        # Then - negative value should raise ValidationError
        with pytest.raises(ValidationError):
            HandlerConfig(backup_count=-1)  # pyright: ignore[reportCallIssue]


class TestPydanticModelConfig:
    """Tesztek a Pydantic model config-hoz."""

    def test_system_config_forbids_extra_fields(self) -> None:
        """Ellenőrzi, hogy a SystemConfig tiltja az extra mezőket."""
        # When
        from neural_ai.core.config.interfaces.types import SystemConfig

        # Then - extra field should raise ValidationError
        with pytest.raises(ValidationError):
            SystemConfig(invalid_field="value")  # type: ignore[call-arg]

    def test_storage_config_forbids_extra_fields(self) -> None:
        """Ellenőrzi, hogy a StorageConfig tiltja az extra mezőket."""
        # When
        from neural_ai.core.config.interfaces.types import StorageConfig

        # Then - extra field should raise ValidationError
        with pytest.raises(ValidationError):
            StorageConfig(invalid_field="value")  # type: ignore[call-arg]

    def test_config_schema_forbids_extra_fields(self) -> None:
        """Ellenőrzi, hogy a ConfigSchema tiltja az extra mezőket."""
        # When
        from neural_ai.core.config.interfaces.types import ConfigSchema

        # Then - extra field should raise ValidationError
        with pytest.raises(ValidationError):
            ConfigSchema(invalid_field="value")  # type: ignore[call-arg]


class TestAdditionalConfigTypes:
    """Tesztek további config típusokhoz."""

    def test_paths_config_exists(self) -> None:
        """Ellenőrzi, hogy a PathsConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import PathsConfig

        # Then
        assert PathsConfig is not None

    def test_handler_config_exists(self) -> None:
        """Ellenőrzi, hogy a HandlerConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import HandlerConfig

        # Then
        assert HandlerConfig is not None

    def test_logger_config_exists(self) -> None:
        """Ellenőrzi, hogy a LoggerConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import LoggerConfig

        # Then
        assert LoggerConfig is not None

    def test_ingestion_config_exists(self) -> None:
        """Ellenőrzi, hogy az IngestionConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import IngestionConfig

        # Then
        assert IngestionConfig is not None

    def test_ui_config_exists(self) -> None:
        """Ellenőrzi, hogy a UIConfig létezik."""
        # When
        from neural_ai.core.config.interfaces.types import UIConfig

        # Then
        assert UIConfig is not None
