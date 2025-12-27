"""Tesztek a DynamicConfigManager osztályhoz."""

import asyncio
from datetime import datetime, timezone
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from neural_ai.core.config.exceptions import ConfigError
from neural_ai.core.config.implementations.dynamic_config_manager import (
    DynamicConfigManager,
)
from neural_ai.core.db.implementations.models import DynamicConfig


@pytest.fixture
def mock_session() -> AsyncMock:
    """Mock AsyncSession létrehozása."""
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.fixture
def mock_logger() -> MagicMock:
    """Mock Logger létrehozása."""
    return MagicMock()


@pytest.fixture
def config_manager(mock_session: AsyncMock) -> DynamicConfigManager:
    """DynamicConfigManager létrehozása mock sessionnel."""
    return DynamicConfigManager(session=mock_session)


@pytest.fixture
def config_manager_with_logger(
    mock_session: AsyncMock, mock_logger: MagicMock
) -> DynamicConfigManager:
    """DynamicConfigManager létrehozása loggerrel."""
    return DynamicConfigManager(session=mock_session, logger=mock_logger)


class TestDynamicConfigManagerInit:
    """DynamicConfigManager inicializálásának tesztjei."""

    def test_init_without_session_raises_value_error(self) -> None:
        """Teszt: ValueError-t dob, ha nincs session megadva."""
        with pytest.raises(ValueError, match="Az adatbázis session megadása kötelező"):
            DynamicConfigManager(session=None)

    def test_init_with_session_success(self, mock_session: AsyncMock) -> None:
        """Teszt: Sikeres inicializálás sessionnel."""
        manager = DynamicConfigManager(session=mock_session)
        assert manager.session == mock_session
        assert manager._logger is None
        assert manager._cache == {}
        assert manager._listeners == []
        assert manager._last_update is None
        assert manager._hot_reload_task is None

    def test_init_with_session_and_logger_success(
        self, mock_session: AsyncMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Sikeres inicializálás sessionnel és loggerrel."""
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        assert manager.session == mock_session
        assert manager._logger == mock_logger


class TestDynamicConfigManagerGet:
    """DynamicConfigManager get metódusának tesztjei."""

    async def test_get_with_multiple_keys_raises_value_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: ValueError-t dob, ha több kulcsot adnak meg."""
        with pytest.raises(ValueError, match="csak egyetlen kulcsot támogat"):
            await config_manager.get("key1", "key2")

    async def test_get_from_cache(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Érték lekérése a cache-ből."""
        config_manager._cache["test_key"] = "cached_value"
        result = await config_manager.get("test_key", default="default_value")
        assert result == "cached_value"

    async def test_get_from_database_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Érték lekérése az adatbázisból."""
        # Mock konfiguráció létrehozása
        mock_config = DynamicConfig(
            key="test_key",
            value="test_value",
            value_type="str",
            category="system",
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = mock_result

        result = await config_manager.get("test_key", default="default_value")

        assert result == "test_value"
        assert config_manager._cache["test_key"] == "test_value"
        mock_session.execute.assert_awaited_once()

    async def test_get_from_database_not_found_returns_default(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Alapértelmezett érték visszaadása, ha a kulcs nem található."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await config_manager.get("nonexistent_key", default="default_value")

        assert result == "default_value"

    async def test_get_database_error_raises_config_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: ConfigError-t dob adatbázis hiba esetén."""
        mock_session.execute.side_effect = Exception("Database error")

        with pytest.raises(ConfigError, match="Konfiguráció lekérdezése sikertelen"):
            await config_manager.get("test_key")


class TestDynamicConfigManagerSet:
    """DynamicConfigManager set metódusának tesztjei."""

    async def test_set_with_multiple_keys_raises_value_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: ValueError-t dob, ha több kulcsot adnak meg."""
        with pytest.raises(ValueError, match="csak egyetlen kulcsot támogat"):
            await config_manager.set("key1", "key2", value="value")

    async def test_set_new_config_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Új konfiguráció létrehozása."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        await config_manager.set("new_key", value="new_value")

        # Ellenőrizzük, hogy a konfiguráció hozzá lett-e adva
        assert mock_session.add.called
        mock_session.commit.assert_awaited_once()
        assert config_manager._cache["new_key"] == "new_value"

    async def test_set_existing_config_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Meglévő konfiguráció frissítése."""
        mock_config = DynamicConfig(
            key="existing_key",
            value="old_value",
            value_type="str",
            category="system",
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = mock_result

        await config_manager.set("existing_key", value="updated_value")

        assert mock_config.value == "updated_value"
        mock_session.commit.assert_awaited_once()
        assert config_manager._cache["existing_key"] == "updated_value"

    async def test_set_database_error_raises_config_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: ConfigError-t dob adatbázis hiba esetén."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        mock_session.commit.side_effect = Exception("Database error")

        with pytest.raises(ConfigError, match="Konfiguráció beállítása sikertelen"):
            await config_manager.set("test_key", value="test_value")

        mock_session.rollback.assert_awaited_once()


class TestDynamicConfigManagerGetSection:
    """DynamicConfigManager get_section metódusának tesztjei."""

    async def test_get_section_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Konfigurációs szekció lekérdezése."""
        mock_configs = [
            DynamicConfig(key="key1", value="value1", value_type="str", category="risk"),
            DynamicConfig(key="key2", value="value2", value_type="int", category="risk"),
        ]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_configs
        mock_session.execute.return_value = mock_result

        result = await config_manager.get_section("risk")

        assert result == {"key1": "value1", "key2": "value2"}

    async def test_get_section_not_found_raises_key_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: KeyError-t dob, ha a szekció nem található."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        with pytest.raises(KeyError, match="Konfigurációs kategória nem található"):
            await config_manager.get_section("nonexistent_category")

    async def test_get_section_database_error_raises_config_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: ConfigError-t dob adatbázis hiba esetén."""
        mock_session.execute.side_effect = Exception("Database error")

        with pytest.raises(ConfigError, match="Konfigurációs szekció lekérdezése sikertelen"):
            await config_manager.get_section("risk")


class TestDynamicConfigManagerNotImplementedMethods:
    """Nem implementált metódusok tesztjei."""

    async def test_save_raises_not_implemented_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: save metódus NotImplementedError-t dob."""
        with pytest.raises(NotImplementedError):
            await config_manager.save()

    async def test_load_raises_not_implemented_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: load metódus NotImplementedError-t dob."""
        with pytest.raises(NotImplementedError):
            await config_manager.load("filename")

    async def test_load_directory_raises_not_implemented_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: load_directory metódus NotImplementedError-t dob."""
        with pytest.raises(NotImplementedError):
            await config_manager.load_directory("path")


class TestDynamicConfigManagerValidate:
    """DynamicConfigManager validate metódusának tesztjei."""

    async def test_validate_success(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Sikeres validáció."""
        config_manager._cache = {
            "key1": "value1",
            "key2": 123,
            "key3": 3.14,
        }
        schema = {
            "key1": str,
            "key2": int,
            "key3": float,
        }

        is_valid, errors = await config_manager.validate(schema)

        assert is_valid is True
        assert errors is None

    async def test_validate_missing_required_field(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Validáció hiba, ha kötelező mező hiányzik."""
        config_manager._cache = {"key1": "value1"}
        schema = {
            "key1": str,
            "missing_key": int,
        }

        is_valid, errors = await config_manager.validate(schema)

        assert is_valid is False
        assert "missing_key" in errors
        assert errors["missing_key"] == "Kötelező mező hiányzik"

    async def test_validate_invalid_type(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Validáció hiba, ha az érték típusa nem megfelelő."""
        config_manager._cache = {"key1": "value1"}
        schema = {"key1": int}

        is_valid, errors = await config_manager.validate(schema)

        assert is_valid is False
        assert "key1" in errors
        assert "Érvénytelen típus" in errors["key1"]


class TestDynamicConfigManagerListeners:
    """Listener metódusok tesztjei."""

    def test_add_listener_success(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Listener hozzáadása."""
        async def dummy_listener(key: str, value: Any) -> None:
            pass

        config_manager.add_listener(dummy_listener)

        assert len(config_manager._listeners) == 1
        assert config_manager._listeners[0] == dummy_listener

    def test_remove_listener_success(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Listener eltávolítása."""
        async def dummy_listener(key: str, value: Any) -> None:
            pass

        config_manager.add_listener(dummy_listener)
        config_manager.remove_listener(dummy_listener)

        assert len(config_manager._listeners) == 0

    def test_remove_nonexistent_listener_no_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Nem létező listener eltávolítása nem okoz hibát."""
        async def dummy_listener(key: str, value: Any) -> None:
            pass

        # Nem okoz hibát, ha a listener nem létezik
        config_manager.remove_listener(dummy_listener)


class TestDynamicConfigManagerHotReload:
    """Hot reload metódusok tesztjei."""

    async def test_start_hot_reload_success(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Hot reload indítása."""
        await config_manager.start_hot_reload(interval=1.0)

        assert config_manager._hot_reload_task is not None
        assert not config_manager._hot_reload_task.done()

        # Hot reload leállítása
        await config_manager.stop_hot_reload()

    async def test_start_hot_reload_when_already_running_raises_runtime_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: RuntimeError-t dob, ha a hot reload már fut."""
        await config_manager.start_hot_reload(interval=1.0)

        with pytest.raises(RuntimeError, match="A hot reload már fut"):
            await config_manager.start_hot_reload(interval=1.0)

        await config_manager.stop_hot_reload()

    async def test_stop_hot_reload_success(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Hot reload leállítása."""
        await config_manager.start_hot_reload(interval=1.0)
        await config_manager.stop_hot_reload()

        assert config_manager._hot_reload_task is None
        assert config_manager._stop_hot_reload.is_set()

    async def test_stop_hot_reload_when_not_running_no_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Hot reload leállítása nem okoz hibát, ha nem fut."""
        # Nem okoz hibát, ha a hot reload nem fut
        await config_manager.stop_hot_reload()


class TestDynamicConfigManagerGetAll:
    """DynamicConfigManager get_all metódusának tesztjei."""

    async def test_get_all_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Összes konfiguráció lekérdezése."""
        mock_configs = [
            DynamicConfig(key="key1", value="value1", value_type="str", category="system"),
            DynamicConfig(key="key2", value="value2", value_type="int", category="risk"),
        ]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_configs
        mock_session.execute.return_value = mock_result

        result = await config_manager.get_all()

        assert result == {"key1": "value1", "key2": "value2"}

    async def test_get_all_with_category_filter(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Konfigurációk lekérdezése kategória szerint."""
        mock_configs = [
            DynamicConfig(key="key1", value="value1", value_type="str", category="risk"),
        ]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_configs
        mock_session.execute.return_value = mock_result

        result = await config_manager.get_all(category="risk")

        assert result == {"key1": "value1"}

    async def test_get_all_database_error_raises_config_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: ConfigError-t dob adatbázis hiba esetén."""
        mock_session.execute.side_effect = Exception("Database error")

        with pytest.raises(ConfigError, match="Összes konfiguráció lekérdezése sikertelen"):
            await config_manager.get_all()


class TestDynamicConfigManagerSetWithMetadata:
    """DynamicConfigManager set_with_metadata metódusának tesztjei."""

    async def test_set_with_metadata_new_config_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Új konfiguráció létrehozása metaadatokkal."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        await config_manager.set_with_metadata(
            key="test_key",
            value="test_value",
            category="risk",
            description="Test description",
            is_active=True,
        )

        assert mock_session.add.called
        mock_session.commit.assert_awaited_once()
        assert config_manager._cache["test_key"] == "test_value"

    async def test_set_with_metadata_existing_config_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Meglévő konfiguráció frissítése metaadatokkal."""
        mock_config = DynamicConfig(
            key="existing_key",
            value="old_value",
            value_type="str",
            category="system",
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = mock_result

        await config_manager.set_with_metadata(
            key="existing_key",
            value="updated_value",
            category="risk",
            description="Updated description",
            is_active=False,
        )

        assert mock_config.value == "updated_value"
        assert mock_config.category == "risk"
        assert mock_config.description == "Updated description"
        assert mock_config.is_active is False
        mock_session.commit.assert_awaited_once()


class TestDynamicConfigManagerDelete:
    """DynamicConfigManager delete metódusának tesztjei."""

    async def test_delete_existing_config_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Konfiguráció törlése (soft delete)."""
        mock_config = DynamicConfig(
            key="test_key",
            value="test_value",
            value_type="str",
            category="system",
            is_active=True,
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = mock_result

        result = await config_manager.delete("test_key")

        assert result is True
        assert mock_config.is_active is False
        mock_session.commit.assert_awaited_once()
        assert "test_key" not in config_manager._cache

    async def test_delete_nonexistent_config_returns_false(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: False visszaadása, ha a konfiguráció nem található."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await config_manager.delete("nonexistent_key")

        assert result is False

    async def test_delete_database_error_raises_config_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: ConfigError-t dob adatbázis hiba esetén."""
        mock_config = DynamicConfig(
            key="test_key",
            value="test_value",
            value_type="str",
            category="system",
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = mock_result
        mock_session.commit.side_effect = Exception("Database error")

        with pytest.raises(ConfigError, match="Konfiguráció törlése sikertelen"):
            await config_manager.delete("test_key")


class TestDynamicConfigManagerDetermineValueType:
    """_determine_value_type metódus tesztjei."""

    def test_determine_value_type_bool(self) -> None:
        """Teszt: Boolean típus felismerése."""
        assert DynamicConfigManager._determine_value_type(True) == "bool"
        assert DynamicConfigManager._determine_value_type(False) == "bool"

    def test_determine_value_type_int(self) -> None:
        """Teszt: Integer típus felismerése."""
        assert DynamicConfigManager._determine_value_type(42) == "int"
        assert DynamicConfigManager._determine_value_type(0) == "int"
        assert DynamicConfigManager._determine_value_type(-123) == "int"

    def test_determine_value_type_float(self) -> None:
        """Teszt: Float típus felismerése."""
        assert DynamicConfigManager._determine_value_type(3.14) == "float"
        assert DynamicConfigManager._determine_value_type(0.0) == "float"
        assert DynamicConfigManager._determine_value_type(-2.5) == "float"

    def test_determine_value_type_str(self) -> None:
        """Teszt: String típus felismerése."""
        assert DynamicConfigManager._determine_value_type("hello") == "str"
        assert DynamicConfigManager._determine_value_type("") == "str"

    def test_determine_value_type_list(self) -> None:
        """Teszt: List típus felismerése."""
        assert DynamicConfigManager._determine_value_type([1, 2, 3]) == "list"
        assert DynamicConfigManager._determine_value_type([]) == "list"

    def test_determine_value_type_dict(self) -> None:
        """Teszt: Dict típus felismerése."""
        assert DynamicConfigManager._determine_value_type({"key": "value"}) == "dict"
        assert DynamicConfigManager._determine_value_type({}) == "dict"

    def test_determine_value_type_unknown_defaults_to_str(self) -> None:
        """Teszt: Ismeretlen típus esetén str visszaadása."""
        # Példa ismeretlen típusra
        class CustomType:
            pass

        assert DynamicConfigManager._determine_value_type(CustomType()) == "str"


class TestDynamicConfigManagerNotifyListeners:
    """_notify_listeners metódus tesztjei."""

    async def test_notify_listeners_success(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Listener-ek értesítése."""
        listener_called = False
        listener_key = None
        listener_value = None

        async def test_listener(key: str, value: Any) -> None:
            nonlocal listener_called, listener_key, listener_value
            listener_called = True
            listener_key = key
            listener_value = value

        config_manager.add_listener(test_listener)
        await config_manager._notify_listeners("test_key", "test_value")

        assert listener_called is True
        assert listener_key == "test_key"
        assert listener_value == "test_value"

    async def test_notify_listeners_with_exception_in_listener(
        self, config_manager: DynamicConfigManager, mock_logger: MagicMock
    ) -> None:
        """Teszt: Listener hiba esetén a többi listener még mindig hívódik."""
        config_manager._logger = mock_logger

        error_listener_called = False
        good_listener_called = False

        async def error_listener(key: str, value: Any) -> None:
            nonlocal error_listener_called
            error_listener_called = True
            raise Exception("Listener error")

        async def good_listener(key: str, value: Any) -> None:
            nonlocal good_listener_called
            good_listener_called = True

        config_manager.add_listener(error_listener)
        config_manager.add_listener(good_listener)

        # A hiba nem szabad, hogy megállítsa a többi listener hívását
        await config_manager._notify_listeners("test_key", "test_value")

        assert error_listener_called is True
        assert good_listener_called is True
        # Ellenőrizzük, hogy a hibát naplózták-e
        mock_logger.error.assert_called()


class TestDynamicConfigManagerCheckForUpdates:
    """_check_for_updates metódus tesztjei."""

    async def test_check_for_updates_first_time_loads_all(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Első alkalommal betölti az összes konfigurációt."""
        config_manager._last_update = None

        mock_configs = [
            DynamicConfig(key="key1", value="value1", value_type="str", category="system"),
        ]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_configs
        mock_session.execute.return_value = mock_result

        await config_manager._check_for_updates()

        assert config_manager._cache == {"key1": "value1"}
        assert config_manager._last_update is not None

    async def test_check_for_updates_with_changes(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Változások észlelése és cache frissítése."""
        # Először beállítjuk az utolsó frissítés időpontját
        config_manager._last_update = datetime.now(timezone.utc)

        # Mock konfiguráció, ami megváltozott
        updated_config = DynamicConfig(
            key="updated_key",
            value="new_value",
            value_type="str",
            category="system",
        )
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [updated_config]
        mock_session.execute.return_value = mock_result

        # Listener hozzáadása a változás észleléséhez
        listener_called = False
        async def test_listener(key: str, value: Any) -> None:
            nonlocal listener_called
            listener_called = True

        config_manager.add_listener(test_listener)

        await config_manager._check_for_updates()

        assert config_manager._cache["updated_key"] == "new_value"
        assert listener_called is True

    async def test_check_for_updates_database_error_logged(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Adatbázis hiba esetén a hiba naplózásra kerül."""
        config_manager._logger = mock_logger
        config_manager._last_update = datetime.now(timezone.utc)
        mock_session.execute.side_effect = Exception("Database error")

        # A hiba nem szabad, hogy kivételt dobjon, csak naplózásra kerüljön
        await config_manager._check_for_updates()

        mock_logger.error.assert_called()