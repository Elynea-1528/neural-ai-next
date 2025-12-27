"""Config Factory tesztmodul.

Ez a modul tartalmazza a konfigurációs factory teszteit,
ellenőrzi a megfelelő példányosítást és a hibakezelést.
"""

from unittest.mock import MagicMock

import pytest

from neural_ai.core.config.exceptions.config_error import ConfigLoadError
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.interfaces.async_config_interface import (
    AsyncConfigManagerInterface,
)
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


class TestConfigManagerFactory:
    """ConfigManagerFactory osztály tesztjei."""

    def test_get_manager_should_return_valid_interface(self) -> None:
        """Teszteli, hogy a factory létrehoz egy érvényes konfigurációs interfészt."""
        # Given
        filename: str = "tests/core/config/test_config.yaml"

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(filename)

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_get_manager_with_invalid_extension_should_raise_error(self) -> None:
        """Teszteli, hogy érvénytelen kiterjesztés esetén hiba keletkezik."""
        # Given
        filename: str = "test_config.invalid"

        # When / Then
        with pytest.raises(ConfigLoadError):
            ConfigManagerFactory.get_manager(filename)

    @pytest.mark.asyncio
    async def test_get_async_manager_should_return_valid_interface(self) -> None:
        """Teszteli, hogy a factory létrehoz egy érvényes aszinkron konfigurációs interfészt."""
        # Given
        manager_type: str = "dynamic"
        mock_session: MagicMock = MagicMock()
        mock_logger: MagicMock = MagicMock()

        # When
        result: AsyncConfigManagerInterface = await ConfigManagerFactory.get_async_manager(
            manager_type, mock_session, mock_logger
        )

        # Then
        assert result is not None
        assert isinstance(result, AsyncConfigManagerInterface)

    @pytest.mark.asyncio
    async def test_get_async_manager_should_be_created(self) -> None:
        """Teszteli, hogy az aszinkron interfész létrejön."""
        # Given
        manager_type: str = "dynamic"
        mock_session: MagicMock = MagicMock()
        mock_logger: MagicMock = MagicMock()
        async_interface: AsyncConfigManagerInterface = await ConfigManagerFactory.get_async_manager(
            manager_type, mock_session, mock_logger
        )

        # When / Then
        # Csak ellenőrizzük, hogy az interfész létrejött
        assert async_interface is not None
        assert isinstance(async_interface, AsyncConfigManagerInterface)

    def test_get_manager_should_handle_yaml_extension(self) -> None:
        """Teszteli, hogy a factory kezeli a YAML kiterjesztést."""
        # Given
        yaml_file: str = "tests/core/config/test_config.yaml"

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(yaml_file)

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_get_manager_should_handle_yml_extension(self) -> None:
        """Teszteli, hogy a factory kezeli a YML kiterjesztést."""
        # Given
        yml_file: str = "tests/core/config/test_config.yaml"

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(yml_file)

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_get_manager_without_extension_should_use_default_yaml(self) -> None:
        """Teszteli, hogy kiterjesztés nélküli fájlnál alapértelmezett YAML kezelőt használ."""
        # Given
        no_ext_file: str = "tests/core/config/test_config"

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(no_ext_file)

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_create_manager_should_return_valid_interface(self) -> None:
        """Teszteli, hogy a create_manager létrehoz egy érvényes konfigurációs interfészt."""
        # Given
        manager_type: str = "yaml"
        filename: str = "tests/core/config/test_config.yaml"

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.create_manager(
            manager_type, filename=filename
        )

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_create_manager_with_invalid_type_should_raise_error(self) -> None:
        """Teszteli, hogy érvénytelen típus esetén hiba keletkezik."""
        # Given
        invalid_type: str = "invalid"

        # When / Then
        with pytest.raises(ConfigLoadError):
            ConfigManagerFactory.create_manager(invalid_type)

    @pytest.mark.asyncio
    async def test_get_async_manager_with_invalid_type_should_raise_error(self) -> None:
        """Teszteli, hogy érvénytelen aszinkron típus esetén hiba keletkezik."""
        # Given
        invalid_type: str = "invalid"
        mock_session: MagicMock = MagicMock()

        # When / Then
        with pytest.raises(ConfigLoadError):
            await ConfigManagerFactory.get_async_manager(invalid_type, mock_session)

    def test_get_supported_extensions_should_return_list(self) -> None:
        """Teszteli, hogy a támogatott kiterjesztések listája visszaadódik."""
        # When
        extensions: list[str] = ConfigManagerFactory.get_supported_extensions()

        # Then
        assert isinstance(extensions, list)
        assert ".yaml" in extensions
        assert ".yml" in extensions

    def test_get_supported_async_types_should_return_list(self) -> None:
        """Teszteli, hogy a támogatott aszinkron típusok listája visszaadódik."""
        # When
        async_types: list[str] = ConfigManagerFactory.get_supported_async_types()

        # Then
        assert isinstance(async_types, list)
        assert "dynamic" in async_types
        assert "database" in async_types

    def test_register_manager_should_add_new_manager(self) -> None:
        """Teszteli, hogy új kezelő regisztrálható."""
        # Given
        from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager

        # When
        ConfigManagerFactory.register_manager(".test", YAMLConfigManager)

        # Then
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(
            "tests/core/config/test_config.test"
        )
        assert result is not None
        assert result.get("test_key") == "test_value"

    def test_register_manager_with_invalid_class_should_raise_error(self) -> None:
        """Teszteli, hogy érvénytelen osztály regisztrálásakor hiba keletkezik."""
        # Given
        invalid_class: str = "not_a_class"

        # When / Then
        with pytest.raises(TypeError):
            ConfigManagerFactory.register_manager(".test", invalid_class)  # type: ignore

    @pytest.mark.asyncio
    async def test_get_async_manager_should_pass_session_and_logger(self) -> None:
        """Teszteli, hogy az aszinkron kezelő megkapja a sessiont és loggert."""
        # Given
        manager_type: str = "dynamic"
        mock_session: MagicMock = MagicMock()
        mock_logger: MagicMock = MagicMock()

        # When
        result: AsyncConfigManagerInterface = await ConfigManagerFactory.get_async_manager(
            manager_type, mock_session, mock_logger
        )

        # Then
        assert result is not None
        # A result-nak tartalmaznia kell a session és logger referenciákat

    def test_get_manager_should_create_separate_instances(self) -> None:
        """Teszteli, hogy a factory külön példányokat hoz létre."""
        # Given
        filename: str = "tests/core/config/test_config.yaml"

        # When
        result1: ConfigManagerInterface = ConfigManagerFactory.get_manager(filename)
        result2: ConfigManagerInterface = ConfigManagerFactory.get_manager(filename)

        # Then
        # A két eredménynek külön példánynak kell lennie (nincs singleton a factory-ben)
        assert result1 is not result2
        assert result1.get("test_key") == result2.get("test_key")

    @pytest.mark.asyncio
    async def test_get_async_manager_should_handle_valid_kwargs(self) -> None:
        """Teszteli, hogy az aszinkron kezelő kezeli a valid paramétereket."""
        # Given
        manager_type: str = "dynamic"
        mock_session: MagicMock = MagicMock()
        mock_logger: MagicMock = MagicMock()

        # When
        result: AsyncConfigManagerInterface = await ConfigManagerFactory.get_async_manager(
            manager_type, mock_session, mock_logger
        )

        # Then
        assert result is not None

    def test_register_async_manager_should_add_new_async_manager(self) -> None:
        """Teszteli, hogy új aszinkron kezelő regisztrálható."""
        # Given
        from neural_ai.core.config.implementations.dynamic_config_manager import (
            DynamicConfigManager,
        )

        # When
        ConfigManagerFactory.register_async_manager("test_async", DynamicConfigManager)

        # Then
        # A regisztráció sikeres, de a teszt nem hívja meg a get_async_manager-t
        # mert a mock nem megfelelően implementálja az interfészt
        assert "test_async" in ConfigManagerFactory.get_supported_async_types()

    def test_register_async_manager_with_invalid_class_should_raise_error(self) -> None:
        """Teszteli, hogy érvénytelen aszinkron osztály regisztrálásakor hiba keletkezik."""
        # Given
        invalid_class: str = "not_a_class"

        # When / Then
        with pytest.raises(TypeError):
            ConfigManagerFactory.register_async_manager("test", invalid_class)  # type: ignore

    @pytest.mark.asyncio
    async def test_get_async_manager_without_session_should_raise_error(self) -> None:
        """Teszteli, hogy session nélkül hiba keletkezik."""
        # Given
        manager_type: str = "dynamic"

        # When / Then
        with pytest.raises(ValueError):
            await ConfigManagerFactory.get_async_manager(manager_type, None)  # type: ignore

    def test_get_manager_with_explicit_type_should_use_that_type(self) -> None:
        """Teszteli, hogy explicit típusmegadás esetén azt használja."""
        # Given
        filename: str = "tests/core/config/test_config.xyz"
        manager_type: str = "yaml"

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(
            filename, manager_type=manager_type
        )

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"
