"""YAML alapú konfigurációkezelő implementáció."""

import os
from dataclasses import dataclass
from typing import Any, cast

import yaml

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.interfaces import ConfigManagerInterface


@dataclass
class ValidationContext:
    """Validation context for schema validation."""

    path: str
    errors: dict[str, str]
    value: Any
    schema: dict[str, Any]


class YAMLConfigManager(ConfigManagerInterface):
    """YAML fájlokat kezelő konfigurációkezelő."""

    _TYPE_MAP: dict[str, type[Any]] = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
    }

    def __init__(self, filename: str | None = None) -> None:
        """Inicializálja a YAML konfigurációkezelőt."""
        self._config: dict[str, Any] = {}
        self._filename: str | None = None
        if filename:
            self.load(filename)

    @staticmethod
    def _ensure_dict(data: Any) -> dict[str, Any]:
        """Ensure the data is a dictionary.

        Args:
            data: Any data to check

        Returns:
            Dict[str, Any]: The data as a dictionary

        Raises:
            ConfigLoadError: If the data is not None and not a dictionary
        """
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise ConfigLoadError("YAML content must be a dictionary")
        return data

    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból."""
        current: dict[str, Any] | Any = self._config
        for key in keys:
            if not isinstance(current, dict):
                return default
            current = cast(dict[str, Any], current).get(key)
            if current is None:
                return default
        return current

    def get_section(self, section: str) -> dict[str, Any]:
        """Teljes konfigurációs szekció lekérése."""
        if section not in self._config:
            raise KeyError(f"Configuration section not found: {section}")
        section_data = self._config.get(section, {})
        return cast(dict[str, Any], section_data)

    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban."""
        if not keys:
            raise ValueError("At least one key must be provided")

        current = self._config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            elif not isinstance(current[key], dict):
                raise ValueError(f"Cannot set nested key in non-dict value: {key}")
            current = current[key]
        current[keys[-1]] = value

    def save(self, filename: str | None = None) -> None:
        """Aktuális konfiguráció mentése fájlba."""
        save_filename = filename or self._filename
        if not save_filename:
            raise ValueError("No filename specified for save operation")

        try:
            os.makedirs(os.path.dirname(save_filename), exist_ok=True)
            with open(save_filename, "w", encoding="utf-8") as f:
                yaml.dump(self._config, f, default_flow_style=False, sort_keys=False)
        except (OSError, yaml.YAMLError) as e:
            raise ValueError(f"Failed to save configuration: {str(e)}") from e

    def load(self, filename: str) -> None:
        """Konfiguráció betöltése fájlból."""
        if not os.path.exists(filename):
            raise ConfigLoadError(f"File not found: {filename}")

        try:
            with open(filename, encoding="utf-8") as f:
                file_content = f.read()
                data = yaml.safe_load(file_content)
                self._config = self._ensure_dict(data)
                self._filename = filename
        except (FileNotFoundError, yaml.YAMLError) as e:
            raise ConfigLoadError(f"Failed to load configuration: {str(e)}") from e

    def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        """Konfiguráció validálása séma alapján."""
        ctx = ValidationContext(path="", errors={}, value=self._config, schema=schema)
        self._validate_dict(ctx)
        return not bool(ctx.errors), ctx.errors if ctx.errors else None

    def _validate_dict(self, ctx: ValidationContext) -> None:
        """Rekurzív séma validáció."""
        config = cast(dict[str, Any], ctx.value)
        for key, schema_value in ctx.schema.items():
            current_path = f"{ctx.path}.{key}" if ctx.path else key
            config_value = config.get(key)

            sub_ctx = ValidationContext(
                path=current_path,
                errors=ctx.errors,
                value=config_value,
                schema=schema_value,
            )

            if not self._validate_required(sub_ctx):
                continue

            if not self._validate_type(sub_ctx):
                continue

            self._validate_nested(sub_ctx)
            self._validate_constraints(sub_ctx)

    def _validate_required(self, ctx: ValidationContext) -> bool:
        """Kötelező mező ellenőrzése."""
        if ctx.value is None and not ctx.schema.get("optional", False):
            ctx.errors[ctx.path] = "Required field is missing"
            return False
        return True

    def _validate_type(self, ctx: ValidationContext) -> bool:
        """Típus ellenőrzése."""
        if ctx.value is None:
            return True

        expected_type = ctx.schema.get("type")
        if not expected_type:
            return True

        expected_type_class = self._TYPE_MAP.get(expected_type)
        if not expected_type_class:
            ctx.errors[ctx.path] = f"Unsupported type: {expected_type}"
            return False

        if not isinstance(ctx.value, expected_type_class):
            ctx.errors[ctx.path] = f"Invalid type, expected {expected_type}"
            return False

        return True

    def _validate_nested(self, ctx: ValidationContext) -> None:
        """Beágyazott értékek validálása."""
        if ctx.schema.get("type") == "dict" and "schema" in ctx.schema:
            if not isinstance(ctx.value, dict):
                ctx.errors[ctx.path] = "Expected dictionary"
                return
            nested_ctx = ValidationContext(
                path=ctx.path,
                errors=ctx.errors,
                value=ctx.value,
                schema=ctx.schema["schema"],
            )
            self._validate_dict(nested_ctx)

    def _validate_constraints(self, ctx: ValidationContext) -> None:
        """Érték korlátok validálása."""
        self._validate_choices(ctx)
        self._validate_range(ctx)

    def _validate_choices(self, ctx: ValidationContext) -> None:
        """Választható értékek validálása."""
        choices = ctx.schema.get("choices")
        if choices is not None and ctx.value not in choices:
            ctx.errors[ctx.path] = f"Value must be one of: {choices}"

    def _validate_range(self, ctx: ValidationContext) -> None:
        """Érték tartományának validálása."""
        if not isinstance(ctx.value, (int, float)):
            return

        min_value = ctx.schema.get("min")
        max_value = ctx.schema.get("max")

        if min_value is not None and ctx.value < min_value:
            ctx.errors[ctx.path] = f"Value must be >= {min_value}"
        if max_value is not None and ctx.value > max_value:
            ctx.errors[ctx.path] = f"Value must be <= {max_value}"
