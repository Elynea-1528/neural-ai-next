"""Tesztek a DynamicConfigManager osztályhoz."""

import asyncio
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from neural_ai.core.config.exceptions import ConfigError
from neural_ai.core.config.implementations.dynamic_config_manager import (
    DynamicConfigManager,
)
from neural_ai.core.db.implementations.models import DynamicConfig


@pytest.fixture(scope="function")
def mock_session() -> AsyncMock:
    """Mock AsyncSession létrehozása."""
    session: AsyncMock = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.fixture(scope="function")
def mock_logger() -> MagicMock:
    """Mock Logger létrehozása."""
    logger: MagicMock = MagicMock()
    return logger


@pytest.fixture(scope="function")
def config_manager(mock_session: AsyncMock) -> DynamicConfigManager:
    """DynamicConfigManager létrehozása mock sessionnel."""
    return DynamicConfigManager(session=mock_session)


@pytest.fixture(scope="function")
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
        assert manager._logger is None  # pyright: ignore[reportPrivateUsage]
        assert manager._cache == {}  # pyright: ignore[reportPrivateUsage]
        assert manager._listeners == []  # pyright: ignore[reportPrivateUsage]
        assert manager._last_update is None  # pyright: ignore[reportPrivateUsage]
        assert manager._hot_reload_task is None  # pyright: ignore[reportPrivateUsage]

    def test_init_with_session_and_logger_success(
        self, mock_session: AsyncMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Sikeres inicializálás sessionnel és loggerrel."""
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        assert manager.session == mock_session
        assert manager._logger == mock_logger  # pyright: ignore[reportPrivateUsage]


class TestDynamicConfigManagerGet:
    """DynamicConfigManager get metódusának tesztjei."""

    @pytest.mark.asyncio
    async def test_get_with_multiple_keys_raises_value_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: ValueError-t dob, ha több kulcsot adnak meg."""
        with pytest.raises(ValueError, match="csak egyetlen kulcsot támogat"):
            await config_manager.get("key1", "key2")

    @pytest.mark.asyncio
    async def test_get_from_cache(self, config_manager: DynamicConfigManager) -> None:
        """Teszt: Érték lekérése a cache-ből."""
        config_manager._cache["test_key"] = "cached_value"  # pyright: ignore[reportPrivateUsage]
        result = await config_manager.get("test_key", default="default_value")
        assert result == "cached_value"

    @pytest.mark.asyncio
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
        mock_result: MagicMock = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = mock_result

        result = await config_manager.get("test_key", default="default_value")

        assert result == "test_value"
        assert config_manager._cache["test_key"] == "test_value"  # pyright: ignore[reportPrivateUsage]
        mock_session.execute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_from_database_not_found_returns_default(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Alapértelmezett érték visszaadása, ha a kulcs nem található."""
        mock_result: MagicMock = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await config_manager.get("nonexistent_key", default="default_value")

        assert result == "default_value"

    @pytest.mark.asyncio
    async def test_get_database_error_raises_config_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: ConfigError-t dob adatbázis hiba esetén."""
        mock_session.execute.side_effect = Exception("Database error")

        with pytest.raises(ConfigError, match="Konfiguráció lekérdezése sikertelen"):
            await config_manager.get("test_key")


class TestDynamicConfigManagerSet:
    """DynamicConfigManager set metódusának tesztjei."""

    @pytest.mark.asyncio
    async def test_set_with_multiple_keys_raises_value_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: ValueError-t dob, ha több kulcsot adnak meg."""
        with pytest.raises(ValueError, match="csak egyetlen kulcsot támogat"):
            await config_manager.set("key1", "key2", value="value")

    @pytest.mark.asyncio
    async def test_set_new_config_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Új konfiguráció létrehozása."""
        mock_result: MagicMock = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        await config_manager.set("new_key", value="new_value")

        # Ellenőrizzük, hogy a konfiguráció hozzá lett-e adva
        assert mock_session.add.called
        mock_session.commit.assert_awaited_once()
        assert config_manager._cache["new_key"] == "new_value"  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
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
        mock_result: MagicMock = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = mock_result

        await config_manager.set("existing_key", value="updated_value")

        assert mock_config.value == "updated_value"
        mock_session.commit.assert_awaited_once()
        assert config_manager._cache["existing_key"] == "updated_value"  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
    async def test_set_database_error_raises_config_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: ConfigError-t dob adatbázis hiba esetén."""
        mock_result: MagicMock = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        mock_session.commit.side_effect = Exception("Database error")

        with pytest.raises(ConfigError, match="Konfiguráció beállítása sikertelen"):
            await config_manager.set("test_key", value="test_value")

        mock_session.rollback.assert_awaited_once()


class TestDynamicConfigManagerGetSection:
    """DynamicConfigManager get_section metódusának tesztjei."""

    @pytest.mark.asyncio
    async def test_get_section_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Konfigurációs szekció lekérdezése."""
        mock_configs = [
            DynamicConfig(key="key1", value="value1", value_type="str", category="risk"),
            DynamicConfig(key="key2", value="value2", value_type="int", category="risk"),
        ]
        mock_result: MagicMock = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_configs
        mock_session.execute.return_value = mock_result

        result = await config_manager.get_section("risk")

        assert result == {"key1": "value1", "key2": "value2"}

    @pytest.mark.asyncio
    async def test_get_section_not_found_raises_key_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: KeyError-t dob, ha a szekció nem található."""
        mock_result: MagicMock = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        with pytest.raises(KeyError, match="Konfigurációs kategória nem található"):
            await config_manager.get_section("nonexistent_category")

    @pytest.mark.asyncio
    async def test_get_section_database_error_raises_config_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: ConfigError-t dob adatbázis hiba esetén."""
        mock_session.execute.side_effect = Exception("Database error")

        with pytest.raises(ConfigError, match="Konfigurációs szekció lekérdezése sikertelen"):
            await config_manager.get_section("risk")


class TestDynamicConfigManagerNotImplementedMethods:
    """Nem implementált metódusok tesztjei."""

    @pytest.mark.asyncio
    async def test_save_raises_not_implemented_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: save metódus NotImplementedError-t dob."""
        with pytest.raises(NotImplementedError):
            await config_manager.save()

    @pytest.mark.asyncio
    async def test_load_raises_not_implemented_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: load metódus NotImplementedError-t dob."""
        with pytest.raises(NotImplementedError):
            await config_manager.load("filename")

    @pytest.mark.asyncio
    async def test_load_directory_raises_not_implemented_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: load_directory metódus NotImplementedError-t dob."""
        with pytest.raises(NotImplementedError):
            await config_manager.load_directory("path")


class TestDynamicConfigManagerValidate:
    """DynamicConfigManager validate metódusának tesztjei."""

    @pytest.mark.asyncio
    async def test_validate_success(self, config_manager: DynamicConfigManager) -> None:
        """Teszt: Sikeres validáció."""
        config_manager._cache = {  # pyright: ignore[reportPrivateUsage]
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

    @pytest.mark.asyncio
    async def test_validate_missing_required_field(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Validáció hiba, ha kötelező mező hiányzik."""
        config_manager._cache = {"key1": "value1"}  # pyright: ignore[reportPrivateUsage]
        schema = {
            "key1": str,
            "missing_key": int,
        }

        is_valid, errors = await config_manager.validate(schema)

        assert is_valid is False
        assert "missing_key" in errors  # type: ignore[operator]
        assert errors["missing_key"] == "Kötelező mező hiányzik"  # type: ignore[index]

    @pytest.mark.asyncio
    async def test_validate_invalid_type(self, config_manager: DynamicConfigManager) -> None:
        """Teszt: Validáció hiba, ha az érték típusa nem megfelelő."""
        config_manager._cache = {"key1": "value1"}  # pyright: ignore[reportPrivateUsage]
        schema = {"key1": int}

        is_valid, errors = await config_manager.validate(schema)

        assert is_valid is False
        assert "key1" in errors  # type: ignore[operator]
        assert "Érvénytelen típus" in errors["key1"]  # type: ignore[index]


class TestDynamicConfigManagerListeners:
    """Listener metódusok tesztjei."""

    def test_add_listener_success(self, config_manager: DynamicConfigManager) -> None:
        """Teszt: Listener hozzáadása."""

        async def dummy_listener(key: str, value: Any) -> None:
            pass

        config_manager.add_listener(dummy_listener)

        assert len(config_manager._listeners) == 1  # pyright: ignore[reportPrivateUsage]
        assert config_manager._listeners[0] == dummy_listener  # pyright: ignore[reportPrivateUsage]

    def test_remove_listener_success(self, config_manager: DynamicConfigManager) -> None:
        """Teszt: Listener eltávolítása."""

        async def dummy_listener(key: str, value: Any) -> None:
            pass

        config_manager.add_listener(dummy_listener)
        config_manager.remove_listener(dummy_listener)

        assert len(config_manager._listeners) == 0  # pyright: ignore[reportPrivateUsage]

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

    @pytest.mark.asyncio
    async def test_start_hot_reload_success(self, config_manager: DynamicConfigManager) -> None:
        """Teszt: Hot reload indítása."""
        await config_manager.start_hot_reload(interval=1.0)

        assert config_manager._hot_reload_task is not None  # pyright: ignore[reportPrivateUsage]
        assert not config_manager._hot_reload_task.done()  # pyright: ignore[reportPrivateUsage]

        # Hot reload leállítása
        await config_manager.stop_hot_reload()

    @pytest.mark.asyncio
    async def test_start_hot_reload_when_already_running_raises_runtime_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: RuntimeError-t dob, ha a hot reload már fut."""
        await config_manager.start_hot_reload(interval=1.0)

        with pytest.raises(RuntimeError, match="A hot reload már fut"):
            await config_manager.start_hot_reload(interval=1.0)

        await config_manager.stop_hot_reload()

    @pytest.mark.asyncio
    async def test_stop_hot_reload_success(self, config_manager: DynamicConfigManager) -> None:
        """Teszt: Hot reload leállítása."""
        await config_manager.start_hot_reload(interval=1.0)
        await config_manager.stop_hot_reload()

        assert config_manager._hot_reload_task is None  # pyright: ignore[reportPrivateUsage]
        assert config_manager._stop_hot_reload.is_set()  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
    async def test_stop_hot_reload_when_not_running_no_error(
        self, config_manager: DynamicConfigManager
    ) -> None:
        """Teszt: Hot reload leállítása nem okoz hibát, ha nem fut."""
        # Nem okoz hibát, ha a hot reload nem fut
        await config_manager.stop_hot_reload()


class TestDynamicConfigManagerGetAll:
    """DynamicConfigManager get_all metódusának tesztjei."""

    @pytest.mark.asyncio
    async def test_get_all_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Összes konfiguráció lekérdezése."""
        mock_configs = [
            DynamicConfig(key="key1", value="value1", value_type="str", category="system"),
            DynamicConfig(key="key2", value="value2", value_type="int", category="risk"),
        ]
        mock_result: MagicMock = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_configs
        mock_session.execute.return_value = mock_result

        result = await config_manager.get_all()

        assert result == {"key1": "value1", "key2": "value2"}

    @pytest.mark.asyncio
    async def test_get_all_with_category_filter(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Konfigurációk lekérdezése kategória szerint."""
        mock_configs = [
            DynamicConfig(key="key1", value="value1", value_type="str", category="risk"),
        ]
        mock_result: MagicMock = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_configs
        mock_session.execute.return_value = mock_result

        result = await config_manager.get_all(category="risk")

        assert result == {"key1": "value1"}

    @pytest.mark.asyncio
    async def test_get_all_database_error_raises_config_error(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: ConfigError-t dob adatbázis hiba esetén."""
        mock_session.execute.side_effect = Exception("Database error")

        with pytest.raises(ConfigError, match="Összes konfiguráció lekérdezése sikertelen"):
            await config_manager.get_all()


class TestDynamicConfigManagerSetWithMetadata:
    """DynamicConfigManager set_with_metadata metódusának tesztjei."""

    @pytest.mark.asyncio
    async def test_set_with_metadata_new_config_success(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Új konfiguráció létrehozása metaadatokkal."""
        mock_result: MagicMock = MagicMock()
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
        assert config_manager._cache["test_key"] == "test_value"  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
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
        mock_result: MagicMock = MagicMock()
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

    @pytest.mark.asyncio
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
        mock_result: MagicMock = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = mock_result

        result = await config_manager.delete("test_key")

        assert result is True
        assert mock_config.is_active is False
        mock_session.commit.assert_awaited_once()
        assert "test_key" not in config_manager._cache  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
    async def test_delete_nonexistent_config_returns_false(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: False visszaadása, ha a konfiguráció nem található."""
        mock_result: MagicMock = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await config_manager.delete("nonexistent_key")

        assert result is False

    @pytest.mark.asyncio
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
        mock_result: MagicMock = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = mock_result
        mock_session.commit.side_effect = Exception("Database error")

        with pytest.raises(ConfigError, match="Konfiguráció törlése sikertelen"):
            await config_manager.delete("test_key")


class TestDynamicConfigManagerDetermineValueType:
    """_determine_value_type metódus tesztjei."""

    def test_determine_value_type_bool(self) -> None:
        """Teszt: Boolean típus felismerése."""
        assert DynamicConfigManager._determine_value_type(True) == "bool"  # pyright: ignore[reportPrivateUsage]
        assert DynamicConfigManager._determine_value_type(False) == "bool"  # pyright: ignore[reportPrivateUsage]

    def test_determine_value_type_int(self) -> None:
        """Teszt: Integer típus felismerése."""
        assert DynamicConfigManager._determine_value_type(42) == "int"  # pyright: ignore[reportPrivateUsage]
        assert DynamicConfigManager._determine_value_type(0) == "int"  # pyright: ignore[reportPrivateUsage]
        assert DynamicConfigManager._determine_value_type(-123) == "int"  # pyright: ignore[reportPrivateUsage]

    def test_determine_value_type_float(self) -> None:
        """Teszt: Float típus felismerése."""
        assert DynamicConfigManager._determine_value_type(3.14) == "float"  # pyright: ignore[reportPrivateUsage]
        assert DynamicConfigManager._determine_value_type(0.0) == "float"  # pyright: ignore[reportPrivateUsage]
        assert DynamicConfigManager._determine_value_type(-2.5) == "float"  # pyright: ignore[reportPrivateUsage]

    def test_determine_value_type_str(self) -> None:
        """Teszt: String típus felismerése."""
        assert DynamicConfigManager._determine_value_type("hello") == "str"  # pyright: ignore[reportPrivateUsage]
        assert DynamicConfigManager._determine_value_type("") == "str"  # pyright: ignore[reportPrivateUsage]

    def test_determine_value_type_list(self) -> None:
        """Teszt: List típus felismerése."""
        assert DynamicConfigManager._determine_value_type([1, 2, 3]) == "list"  # pyright: ignore[reportPrivateUsage]
        assert DynamicConfigManager._determine_value_type([]) == "list"  # pyright: ignore[reportPrivateUsage]

    def test_determine_value_type_dict(self) -> None:
        """Teszt: Dict típus felismerése."""
        assert DynamicConfigManager._determine_value_type({"key": "value"}) == "dict"  # pyright: ignore[reportPrivateUsage]
        assert DynamicConfigManager._determine_value_type({}) == "dict"  # pyright: ignore[reportPrivateUsage]

    def test_determine_value_type_unknown_defaults_to_str(self) -> None:
        """Teszt: Ismeretlen típus esetén str visszaadása."""

        # Példa ismeretlen típusra
        class CustomType:
            pass

        assert DynamicConfigManager._determine_value_type(CustomType()) == "str"  # pyright: ignore[reportPrivateUsage]


class TestDynamicConfigManagerNotifyListeners:
    """_notify_listeners metódus tesztjei."""

    @pytest.mark.asyncio
    async def test_notify_listeners_success(self, config_manager: DynamicConfigManager) -> None:
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
        await config_manager._notify_listeners("test_key", "test_value")  # pyright: ignore[reportPrivateUsage]

        assert listener_called is True
        assert listener_key == "test_key"
        assert listener_value == "test_value"

    @pytest.mark.asyncio
    async def test_notify_listeners_with_exception_in_listener(
        self, config_manager: DynamicConfigManager, mock_logger: MagicMock
    ) -> None:
        """Teszt: Listener hiba esetén a többi listener még mindig hívódik."""
        config_manager._logger = mock_logger  # pyright: ignore[reportPrivateUsage]

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
        await config_manager._notify_listeners("test_key", "test_value")  # pyright: ignore[reportPrivateUsage]

        assert error_listener_called is True
        assert good_listener_called is True
        # Ellenőrizzük, hogy a hibát naplózták-e
        mock_logger.error.assert_called()


class TestDynamicConfigManagerCheckForUpdates:
    """_check_for_updates metódus tesztjei."""

    @pytest.mark.asyncio
    async def test_check_for_updates_first_time_loads_all(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Első alkalommal betölti az összes konfigurációt."""
        config_manager._last_update = None  # pyright: ignore[reportPrivateUsage]

        mock_configs = [
            DynamicConfig(key="key1", value="value1", value_type="str", category="system"),
        ]
        mock_result: MagicMock = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_configs
        mock_session.execute.return_value = mock_result

        await config_manager._check_for_updates()  # pyright: ignore[reportPrivateUsage]

        assert config_manager._cache == {"key1": "value1"}  # pyright: ignore[reportPrivateUsage]
        assert config_manager._last_update is not None  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
    async def test_check_for_updates_with_changes(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock
    ) -> None:
        """Teszt: Változások észlelése és cache frissítése."""
        # Először beállítjuk az utolsó frissítés időpontját
        config_manager._last_update = datetime.now(UTC)  # pyright: ignore[reportPrivateUsage]

        # Mock konfiguráció, ami megváltozott
        updated_config = DynamicConfig(
            key="updated_key",
            value="new_value",
            value_type="str",
            category="system",
        )
        mock_result: MagicMock = MagicMock()
        mock_result.scalars.return_value.all.return_value = [updated_config]
        mock_session.execute.return_value = mock_result

        # Listener hozzáadása a változás észleléséhez
        listener_called = False

        async def test_listener(key: str, value: Any) -> None:
            nonlocal listener_called
            listener_called = True

        config_manager.add_listener(test_listener)

        await config_manager._check_for_updates()  # pyright: ignore[reportPrivateUsage]

        assert config_manager._cache["updated_key"] == "new_value"  # pyright: ignore[reportPrivateUsage]
        assert listener_called is True

    @pytest.mark.asyncio
    async def test_check_for_updates_database_error_logged(
        self, config_manager: DynamicConfigManager, mock_session: AsyncMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Adatbázis hiba esetén a hiba naplózásra kerül."""
        config_manager._logger = mock_logger  # pyright: ignore[reportPrivateUsage]
        config_manager._last_update = datetime.now(UTC)  # pyright: ignore[reportPrivateUsage]
        mock_session.execute.side_effect = Exception("Database error")

        # A hiba nem szabad, hogy kivételt dobjon, csak naplózásra kerüljön
        await config_manager._check_for_updates()  # pyright: ignore[reportPrivateUsage]

        mock_logger.error.assert_called()
class TestDynamicConfigManagerComprehensive:
    """Dinamikus konfiguráció kezelő hiányzó sorok lefedésére szolgáló tesztek."""

    @pytest.mark.asyncio
    async def test_get_logs_error_on_exception(self) -> None:
        """Teszteli a hiba logolását a get metódusban (114. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Adatbázis hiba")

        mock_logger = MagicMock()

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)

        with pytest.raises(ConfigError, match="Konfiguráció lekérdezése sikertelen"):
            await manager.get("test_key")

        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_logs_info_on_success(self) -> None:
        """Teszteli az info logolást a set metódusban (168. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()

        # Mockoljuk, hogy nem létezik a konfig
        stmt_result = MagicMock()
        stmt_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = stmt_result

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        await manager.set("test_key", value="test_value")

        # Ellenőrizzük, hogy a logger info metódusa meghívódott-e
        mock_logger.info.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_logs_error_on_exception(self) -> None:
        """Teszteli a hiba logolását a set metódusban (173. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        mock_logger = MagicMock()

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)

        with pytest.raises(ConfigError, match="Konfiguráció beállítása sikertelen"):
            await manager.set("test_key", value="test_value")

        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_section_logs_error_on_exception(self) -> None:
        """Teszteli a hiba logolását a get_section metódusban (206. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        mock_logger = MagicMock()

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)

        with pytest.raises(ConfigError, match="Konfigurációs szekció lekérdezése sikertelen"):
            await manager.get_section("test_section")

        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_hot_reload_logs_info_and_error(self) -> None:
        """Teszteli az info és error logolást a start_hot_reload metódusban (330, 337. sorok)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)

        # Mockoljuk a _check_for_updates-t, hogy dobjon egy kivételt
        with patch.object(manager, "_check_for_updates", side_effect=Exception("Hiba")):
            await manager.start_hot_reload(interval=0.1)

            # Várunk egy kicsit, hogy a task futni kezdjen
            await asyncio.sleep(0.2)

            # Leállítjuk a taskot
            await manager.stop_hot_reload()

            # Ellenőrizzük, hogy a logger metódusai meghívást kaptak-e
            mock_logger.info.assert_called()
            mock_logger.error.assert_called()

    @pytest.mark.asyncio
    async def test_stop_hot_reload_logs_warning_on_timeout(self) -> None:
        """Teszteli a warning logolást a stop_hot_reload metódusban timeout esetén (361. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)

        # Létrehozunk egy valódi taskot, ami nem áll le időben
        async def slow_task():
            await asyncio.sleep(20)  # Nem fog leállni 10 másodpercen belül

        # Mockoljuk az asyncio.wait_for-t, hogy timeout-ot okozzon
        with patch("asyncio.wait_for", side_effect=asyncio.TimeoutError):
            # Beállítjuk a taskot
            manager._hot_reload_task = asyncio.create_task(slow_task())  # pyright: ignore[reportPrivateUsage]
            # Beállítjuk, hogy a stop event is aktív legyen
            manager._stop_hot_reload.set()  # pyright: ignore[reportPrivateUsage]

            # Leállítjuk a hot reload-ot
            await manager.stop_hot_reload()

            # Ellenőrizzük, hogy a logger warning metódusa meghívódott-e
            mock_logger.warning.assert_called_once()

            # Takarítás
            if manager._hot_reload_task and not manager._hot_reload_task.done():  # pyright: ignore[reportPrivateUsage]
                manager._hot_reload_task.cancel()  # pyright: ignore[reportPrivateUsage]
                with suppress(asyncio.CancelledError):
                    await manager._hot_reload_task  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
    async def test_stop_hot_reload_logs_info_on_successful_stop(self) -> None:
        """Teszteli az info logolást a stop_hot_reload metódusban sikeres leállásnál (346. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)

        # Elindítjuk a hot reload-ot
        await manager.start_hot_reload(interval=0.1)

        # Leállítjuk a hot reload-ot
        await manager.stop_hot_reload()

        # Ellenőrizzük, hogy a logger info metódusa meghívódott-e (346. sor)
        mock_logger.info.assert_called()

        # Ellenőrizzük, hogy a warning NEM lett meghívva
        mock_logger.warning.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_logs_error_on_exception(self) -> None:
        """Teszteli a hiba logolását a get_all metódusban (391. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        mock_logger = MagicMock()

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)

        with pytest.raises(ConfigError, match="Összes konfiguráció lekérdezése sikertelen"):
            await manager.get_all()

        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_with_metadata_logs_info_and_error(self) -> None:
        """Teszteli az info és error logolást a set_with_metadata metódusban (449-458. sorok)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()

        # Mockoljuk, hogy nem létezik a konfig
        stmt_result = MagicMock()
        stmt_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = stmt_result

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        await manager.set_with_metadata("test_key", "test_value", category="test_category")

        # Ellenőrizzük, hogy a logger info metódusa meghívódott-e
        mock_logger.info.assert_called_once()

        # Teszteljük a hiba esetét is
        mock_session.execute.side_effect = Exception("Adatbázis hiba")

        with pytest.raises(ConfigError, match="Konfiguráció beállítása sikertelen"):
            await manager.set_with_metadata("test_key", "test_value")

        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        assert mock_logger.error.call_count >= 1

    @pytest.mark.asyncio
    async def test_delete_logs_info_and_error(self) -> None:
        """Teszteli az info és error logolást a delete metódusban (491, 498. sorok)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()

        # Mockoljuk, hogy létezik a konfig
        mock_config = MagicMock()
        mock_config.is_active = True
        stmt_result = MagicMock()
        stmt_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = stmt_result

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        result = await manager.delete("test_key")

        assert result is True
        # Ellenőrizzük, hogy a logger info metódusa meghívódott-e
        mock_logger.info.assert_called_once()

        # Teszteljük a hiba esetét is
        mock_session.execute.side_effect = Exception("Adatbázis hiba")

        with pytest.raises(ConfigError, match="Konfiguráció törlése sikertelen"):
            await manager.delete("test_key")

        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        assert mock_logger.error.call_count >= 1

    @pytest.mark.asyncio
    async def test_notify_listeners_logs_error(self) -> None:
        """Teszteli a hiba logolást a _notify_listeners metódusban (513. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)

        # Mockoljuk a listener-t, hogy dobjon egy kivételt
        async def failing_listener(key: str, value: Any) -> None:
            raise Exception("Listener hiba")

        manager.add_listener(failing_listener)

        # Értesítjük a listener-t
        await manager._notify_listeners("test_key", "test_value")  # pyright: ignore[reportPrivateUsage]

        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_for_updates_logs_error(self) -> None:
        """Teszteli a hiba logolást a _check_for_updates metódusban (539. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        mock_logger = MagicMock()

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        # Beállítjuk, hogy legyen last_update, így a _check_for_updates a változásokat ellenőrzi
        manager._last_update = datetime(2020, 1, 1, tzinfo=UTC)  # pyright: ignore[reportPrivateUsage]

        # Ellenőrizzük a változásokat, a kivételt elkapjuk
        try:
            await manager._check_for_updates()  # pyright: ignore[reportPrivateUsage]
        except ConfigError:
            pass  # A kivétel várható

        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_and_remove_listener_logging(self) -> None:
        """Teszteli a debug logolást az add_listener és remove_listener metódusokban."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()

        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)

        # Listener hozzáadása
        async def test_listener(key: str, value: Any) -> None:
            pass

        manager.add_listener(test_listener)
        mock_logger.debug.assert_called_once()

        # Listener eltávolítása
        manager.remove_listener(test_listener)
        assert mock_logger.debug.call_count == 2
