"""YAML alapú konfigurációkezelő implementáció.

Ez a modul tartalmazza a YAML fájlokat kezelő konfigurációkezelő implementációt.
"""

import os
from typing import Any, Dict, Optional, Tuple, Type

import yaml

from neural_ai.core.config.interfaces import ConfigManagerInterface


class YAMLConfigManager(ConfigManagerInterface):
    """YAML fájlokat kezelő konfigurációkezelő.

    Ez az osztály a YAML formátumú konfigurációs fájlok kezelését végzi.
    Támogatja a hierarchikus konfigurációkat és a sémaalapú validációt.
    """

    # pylint: disable=too-many-instance-attributes

    _TYPE_MAP: Dict[str, Type[Any]] = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
    }

    def __init__(self, filename: Optional[str] = None) -> None:
        """Inicializálja a YAML konfigurációkezelőt.

        Args:
            filename: Opcionális konfig fájl neve
        """
        self._config: Dict[str, Any] = {}
        self._filename: Optional[str] = None

        if filename:
            self.load(filename)

    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból.

        Args:
            *keys: Kulcs útvonal (pl. "database", "host")
            default: Alapértelmezett érték, ha a kulcs nem létezik

        Returns:
            Any: A kért konfigurációs érték vagy az alapértelmezett érték
        """
        current = self._config
        for key in keys:
            if not isinstance(current, dict):
                return default
            current = current.get(key)
            if current is None:
                return default
        return current

    def get_section(self, section: str) -> Dict[str, Any]:
        """Teljes konfigurációs szekció lekérése.

        Args:
            section: A szekció neve

        Returns:
            Dict[str, Any]: A szekció összes beállítása

        Raises:
            KeyError: Ha a szekció nem létezik
        """
        if section not in self._config:
            raise KeyError(f"Configuration section not found: {section}")
        return self._config[section]

    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban.

        Args:
            *keys: Kulcs útvonal (pl. "database", "host")
            value: Az új érték

        Raises:
            ValueError: Ha a kulcs útvonal érvénytelen
        """
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

    def save(self, filename: Optional[str] = None) -> None:
        """Aktuális konfiguráció mentése fájlba.

        Args:
            filename: Opcionális fájlnév. Ha nincs megadva,
                az eredeti fájlba ment

        Raises:
            IOError: Ha a mentés sikertelen
        """
        save_filename = filename or self._filename
        if not save_filename:
            raise ValueError("No filename specified for save operation")

        os.makedirs(os.path.dirname(save_filename), exist_ok=True)
        with open(save_filename, "w", encoding="utf-8") as f:
            yaml.dump(self._config, f, default_flow_style=False, sort_keys=False)

    def load(self, filename: str) -> None:
        """Konfiguráció betöltése fájlból.

        Args:
            filename: A betöltendő fájl neve

        Raises:
            FileNotFoundError: Ha a fájl nem létezik
            ValueError: Ha a fájl formátuma érvénytelen
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}
            self._filename = filename
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {str(e)}") from e

    def validate(self, schema: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, str]]]:
        """Konfiguráció validálása séma alapján.

        Args:
            schema: Validációs séma

        Returns:
            Tuple[bool, Optional[Dict[str, str]]]: (érvényes-e, hibaüzenetek)
        """
        errors: Dict[str, str] = {}
        self._validate_dict(self._config, schema, "", errors)
        return not bool(errors), errors if errors else None

    def _validate_dict(
        self,
        config: Dict[str, Any],
        schema: Dict[str, Any],
        path: str,
        errors: Dict[str, str]
    ) -> None:
        """Rekurzív séma validáció."""
        for key, schema_value in schema.items():
            current_path = f"{path}.{key}" if path else key
            config_value = config.get(key)

            if not self._validate_required(config_value, schema_value, current_path, errors):
                continue

            if not self._validate_type(config_value, schema_value, current_path, errors):
                continue

            self._validate_nested(config_value, schema_value, current_path, errors)
            self._validate_constraints(config_value, schema_value, current_path, errors)

    def _validate_required(
        self,
        value: Any,
        schema: Dict[str, Any],
        path: str,
        errors: Dict[str, str]
    ) -> bool:
        """Kötelező mező ellenőrzése."""
        if value is None and not schema.get("optional", False):
            errors[path] = "Required field is missing"
            return False
        return True

    def _validate_type(
        self,
        value: Any,
        schema: Dict[str, Any],
        path: str,
        errors: Dict[str, str]
    ) -> bool:
        """Típus ellenőrzése."""
        if value is None:
            return True

        expected_type = schema.get("type")
        if not expected_type:
            return True

        expected_type_class = self._TYPE_MAP.get(expected_type)
        if not expected_type_class:
            errors[path] = f"Unsupported type: {expected_type}"
            return False

        if not isinstance(value, expected_type_class):
            errors[path] = f"Invalid type, expected {expected_type}"
            return False

        return True

    def _validate_nested(
        self,
        value: Any,
        schema: Dict[str, Any],
        path: str,
        errors: Dict[str, str]
    ) -> None:
        """Beágyazott értékek validálása."""
        if schema.get("type") == "dict" and "schema" in schema:
            if not isinstance(value, dict):
                errors[path] = "Expected dictionary"
                return
            self._validate_dict(value, schema["schema"], path, errors)

    def _validate_constraints(
        self,
        value: Any,
        schema: Dict[str, Any],
        path: str,
        errors: Dict[str, str]
    ) -> None:
        """Érték korlátok validálása."""
        if "choices" in schema and value not in schema["choices"]:
            errors[path] = f"Value must be one of: {schema['choices']}"

        if isinstance(value, (int, float)):
            if "min" in schema and value < schema["min"]:
                errors[path] = f"Value must be >= {schema['min']}"
            if "max" in schema and value > schema["max"]:
                errors[path] = f"Value must be <= {schema['max']}"
