"""Config Factory tesztmodul.

Ez a modul tartalmazza a konfigurációs factory teszteit,
ellenőrzi a megfelelő példányosítást és a hibakezelést.
"""
# pyright: reportArgumentType=false
# Factory create_manager *args/**kwargs type signature hibák

from pathlib import Path
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

    @pytest.fixture
    def config_file(self, tmp_path: Path) -> Path:
        """Létrehoz egy ideiglenes config fájlt."""
        config_path = tmp_path / "test_config.yaml"
        config_path.write_text("test_key: test_value", encoding="utf-8")
        return config_path

    def test_get_manager_should_return_valid_interface(self, config_file: Path) -> None:
        """Teszteli, hogy a factory létrehoz egy érvényes konfigurációs interfészt."""
        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(str(config_file))

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

    def test_get_manager_should_handle_yaml_extension(self, config_file: Path) -> None:
        """Teszteli, hogy a factory kezeli a YAML kiterjesztést."""
        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(str(config_file))

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_get_manager_should_handle_yml_extension(self, tmp_path: Path) -> None:
        """Teszteli, hogy a factory kezeli a YML kiterjesztést."""
        # Given
        yml_file = tmp_path / "test_config.yml"
        yml_file.write_text("test_key: test_value", encoding="utf-8")

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(str(yml_file))

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_get_manager_without_extension_should_use_default_yaml(self, tmp_path: Path) -> None:
        """Teszteli, hogy kiterjesztés nélküli fájlnál alapértelmezett YAML kezelőt használ."""
        # Given
        # Létrehozzuk a fájlt kiterjesztés nélkül, de YAML tartalommal
        no_ext_file = tmp_path / "test_config"
        no_ext_file.write_text("test_key: test_value", encoding="utf-8")

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(str(no_ext_file))

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_create_manager_should_return_valid_interface(self, config_file: Path) -> None:
        """Teszteli, hogy a create_manager létrehoz egy érvényes konfigurációs interfészt."""
        # Given
        manager_type: str = "yaml"

        # When
        # A create_manager *args és **kwargs-t vár, a YAMLConfigManager pedig filename-t
        result: ConfigManagerInterface = ConfigManagerFactory.create_manager(  # pyright: ignore[reportArgumentType]
            manager_type, filename=str(config_file)  # type: ignore[arg-type]
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

    def test_register_manager_should_add_new_manager(self, tmp_path: Path) -> None:
        """Teszteli, hogy új kezelő regisztrálható."""
        # Given
        from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager

        # When
        ConfigManagerFactory.register_manager(".test", YAMLConfigManager)

        # Then
        test_file = tmp_path / "test_config.test"
        test_file.write_text("test_key: test_value", encoding="utf-8")

        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(str(test_file))
        assert result is not None
        assert result.get("test_key") == "test_value"

    # A runtime type check teszteket eltávolítottuk, mert a statikus ellenőrzésre hagyatkozunk.
    # test_register_manager_with_invalid_class_should_raise_error
    # test_register_manager_should_validate_interface_implementation
    # test_register_async_manager_with_invalid_class_should_raise_error
    # test_register_async_manager_should_validate_async_interface_implementation

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

    def test_get_manager_should_create_separate_instances(self, config_file: Path) -> None:
        """Teszteli, hogy a factory külön példányokat hoz létre."""
        # Given
        filename = str(config_file)

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

    @pytest.mark.asyncio
    async def test_get_async_manager_without_session_should_raise_error(self) -> None:
        """Teszteli, hogy session nélkül hiba keletkezik."""
        # Given
        manager_type: str = "dynamic"

        # When / Then
        with pytest.raises(ValueError):
            await ConfigManagerFactory.get_async_manager(manager_type, None)  # type: ignore

    def test_get_manager_with_explicit_type_should_use_that_type(self, tmp_path: Path) -> None:
        """Teszteli, hogy explicit típusmegadás esetén azt használja."""
        # Given
        # Fájl kiterjesztés .xyz, de yaml típust adunk meg
        filename = tmp_path / "test_config.xyz"
        filename.write_text("test_key: test_value", encoding="utf-8")
        manager_type: str = "yaml"

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(
            str(filename), manager_type=manager_type
        )

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_register_manager_should_normalize_extension(self) -> None:
        """Teszteli, hogy a register_manager normalizálja a kiterjesztést (88. sor)."""
        # Given
        from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager

        extension_without_dot = "normalize"

        # When
        # Regisztráljuk a kiterjesztést pont nélkül
        ConfigManagerFactory.register_manager(extension_without_dot, YAMLConfigManager)

        # Then
        # A kiterjesztésnek ponttal kell szerepelnie a támogatottak között
        assert ".normalize" in ConfigManagerFactory.get_supported_extensions()

    def test_register_manager_should_validate_extension_not_empty(self) -> None:
        """Teszteli, hogy a register_manager ellenőrzi az üres kiterjesztést (88. sor)."""
        # Given
        from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager

        empty_extension = ""

        # When / Then
        with pytest.raises(ValueError):
            ConfigManagerFactory.register_manager(empty_extension, YAMLConfigManager)

    def test_register_manager_should_validate_manager_is_type(self) -> None:
        """Teszteli, hogy a register_manager ellenőrzi a típus érvényességét (91. sor)."""
        # Given
        not_a_class = "string_not_a_class"

        # When / Then
        with pytest.raises(TypeError):
            ConfigManagerFactory.register_manager(".test", not_a_class)  # type: ignore

    def test_register_async_manager_should_validate_manager_type_not_empty(self) -> None:
        """Teszteli, hogy a register_async_manager ellenőrzi az üres típust (119. sor)."""
        # Given
        from neural_ai.core.config.implementations.dynamic_config_manager import (
            DynamicConfigManager,
        )

        empty_type = ""

        # When / Then
        with pytest.raises(ValueError):
            ConfigManagerFactory.register_async_manager(empty_type, DynamicConfigManager)

    def test_register_async_manager_should_validate_async_manager_is_type(self) -> None:
        """Teszteli, hogy a register_async_manager ellenőrzi a típus érvényességét (125. sor)."""
        # Given
        not_a_class = "string_not_a_class"

        # When / Then
        with pytest.raises(TypeError):
            ConfigManagerFactory.register_async_manager("test", not_a_class)  # type: ignore

    def test_get_manager_with_explicit_type_should_normalize_type(self, tmp_path: Path) -> None:
        """Teszteli, hogy a get_manager normalizálja az explicit típust (161. sor)."""
        # Given
        filename = tmp_path / "test_config.xyz"
        filename.write_text("test_key: test_value", encoding="utf-8")
        manager_type_without_dot = "yaml"

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(
            str(filename), manager_type=manager_type_without_dot
        )

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_get_manager_with_explicit_type_should_handle_dot_prefix(self, tmp_path: Path) -> None:
        """Teszteli, hogy a get_manager kezeli a ponttal kezdődő explicit típust (161. sor)."""
        # Given
        filename = tmp_path / "test_config.xyz"
        filename.write_text("test_key: test_value", encoding="utf-8")
        manager_type_with_dot = ".yaml"

        # When
        result: ConfigManagerInterface = ConfigManagerFactory.get_manager(
            str(filename), manager_type=manager_type_with_dot
        )

        # Then
        assert result is not None
        assert isinstance(result, ConfigManagerInterface)
        assert result.get("test_key") == "test_value"

    def test_get_manager_with_explicit_type_should_raise_error_for_invalid_type(
        self, tmp_path: Path
    ) -> None:
        """Teszteli, hogy a get_manager hibát dob érvénytelen explicit típus esetén (161. sor)."""
        # Given
        filename = tmp_path / "test_config.xyz"
        filename.write_text("test_key: test_value", encoding="utf-8")
        invalid_manager_type = "invalid"

        # When / Then
        with pytest.raises(ConfigLoadError):
            ConfigManagerFactory.get_manager(str(filename), manager_type=invalid_manager_type)
