"""YAML alapú konfigurációkezelő implementáció."""

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

import yaml

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.interfaces import ConfigManagerInterface

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces import LoggerInterface
    from neural_ai.core.storage.interfaces import StorageInterface


@dataclass
class ValidationContext:
    """Séma validációs kontextus.

    Ez az osztály tartalmazza a validációs folyamat során szükséges adatokat.
    """

    path: str
    errors: dict[str, str]
    value: Any | None
    schema: dict[str, Any]


class YAMLConfigManager(ConfigManagerInterface):
    """YAML fájlokat kezelő konfigurációkezelő.

    A konfigurációk mentésekor automatikusan hozzáadja a schema_version-t,
    és betöltéskor ellenőrzi a kompatibilitást.
    """

    _TYPE_MAP: dict[str, type[Any]] = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
    }

    # Jelenlegi séma verzió - változtatás esetén frissíteni kell
    _CURRENT_SCHEMA_VERSION: str = "1.0"

    def __init__(
        self,
        filename: str | None = None,
        logger: "LoggerInterface | None" = None,
        storage: "StorageInterface | None" = None,
    ) -> None:
        """Inicializálja a YAML konfigurációkezelőt.

        Args:
            filename: Konfigurációs fájl útvonala (opcionális)
            logger: Logger interfész a naplózásra (opcionális)
            storage: Storage interfész a perzisztens tárolásra (opcionális)
        """
        self._config: dict[str, Any] = {}
        self._filename: str | None = None
        self._logger: LoggerInterface | None = logger
        self._storage: StorageInterface | None = storage

        if filename:
            self.load(filename)

    def _get_current_schema_version(self) -> str:
        """Visszaadja a jelenlegi séma verzióját.

        Returns:
            str: A jelenlegi séma verziója
        """
        return self._CURRENT_SCHEMA_VERSION

    def _check_schema_compatibility(self, loaded_version: str) -> bool:
        """Ellenőrzi a betöltött séma kompatibilitását.

        Args:
            loaded_version: A betöltött konfiguráció séma verziója

        Returns:
            bool: True ha kompatibilis, False egyébként
        """
        # Jelenleg csak a pontos egyezést ellenőrizzük
        # Jövőbeli fejlesztés: verzió kompatibilitási mátrix
        return loaded_version == self._CURRENT_SCHEMA_VERSION

    @staticmethod
    def _ensure_dict(data: Any) -> dict[str, Any]:
        """Adatok dictionary típusának biztosítása.

        Args:
            data: Ellenőrizendő adatok

        Returns:
            Dict[str, Any]: Az adatok dictionary formátumban

        Raises:
            ConfigLoadError: Ha az adatok nem None és nem dictionary
        """
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise ConfigLoadError("YAML tartalom dictionary típusúnak kell lennie")
        return cast(dict[str, Any], data)

    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból.

        Args:
            *keys: A konfigurációs kulcsok hierarchiája
            default: Alapértelmezett érték, ha a kulcs nem található

        Returns:
            A konfigurációs érték vagy az alapértelmezett érték
        """
        current: dict[str, Any] | Any = self._config
        for key in keys:
            if not isinstance(current, dict):
                return default
            current = cast(dict[str, Any], current).get(key)
            if current is None:
                return default
        
        # DEBUG log a konfigurációs lekérdezésekhez
        if self._logger:
            self._logger.debug(f"Config get: {'.'.join(keys)} -> {current}")
        
        return current

    def get_section(self, section: str) -> dict[str, Any]:
        """Teljes konfigurációs szekció lekérése.

        Args:
            section: A szekció neve

        Returns:
            A szekció konfigurációs adatai

        Raises:
            KeyError: Ha a szekció nem található
        """
        if section not in self._config:
            raise KeyError(f"Konfigurációs szekció nem található: {section}")
        section_data = self._config.get(section, {})
        return cast(dict[str, Any], section_data)

    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban.

        Args:
            *keys: A konfigurációs kulcsok hierarchiája
            value: A beállítandó érték

        Raises:
            ValueError: Ha nincs kulcs megadva vagy érvénytelen hierarchia
        """
        if not keys:
            raise ValueError("Legalább egy kulcsot meg kell adni")

        current = self._config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            elif not isinstance(current[key], dict):
                raise ValueError(
                    f"Nem lehet beágyazott kulcsot beállítani nem dictionary értékben: {key}"
                )
            current = current[key]
        current[keys[-1]] = value

    def save(self, filename: str | None = None) -> None:
        """Aktuális konfiguráció mentése fájlba.

        A konfiguráció mentésekor automatikusan hozzáadja a schema_version-t,
        hogy a jövőbeli betöltések kompatibilitást ellenőrizhessenek.

        Args:
            filename: A mentési fájl neve (opcionális, alapértelmezett az eredeti fájlnév)

        Raises:
            ValueError: Ha nincs fájlnév megadva vagy mentési hiba történik
        """
        save_filename = filename or self._filename
        if not save_filename:
            raise ValueError("Nincs fájlnév megadva a mentési művelethez")

        try:
            os.makedirs(os.path.dirname(save_filename), exist_ok=True)

            # Verzióinformáció hozzáadása a konfigurációhoz
            config_to_save = self._config.copy()
            if "_schema_version" not in config_to_save:
                config_to_save["_schema_version"] = self._get_current_schema_version()

            with open(save_filename, "w", encoding="utf-8") as f:
                yaml.dump(config_to_save, f, default_flow_style=False, sort_keys=False)
        except (OSError, yaml.YAMLError) as e:
            raise ValueError(f"Konfiguráció mentése sikertelen: {str(e)}") from e

    def load(self, filename: str) -> None:
        """Konfiguráció betöltése fájlból.

        A betöltés során ellenőrzi a séma verzió kompatibilitást, ha a fájl
        tartalmaz verzióinformációt.

        Args:
            filename: A betöltendő fájl neve

        Raises:
            ConfigLoadError: Ha a fájl nem található vagy betöltési hiba történik
        """
        if not os.path.exists(filename):
            raise ConfigLoadError(f"Fájl nem található: {filename}")

        try:
            with open(filename, encoding="utf-8") as f:
                file_content = f.read()
                data = yaml.safe_load(file_content)
                config_data = self._ensure_dict(data)

                # Verzióellenőrzés
                loaded_version = config_data.get("_schema_version")
                if loaded_version and not self._check_schema_compatibility(loaded_version):
                    if self._logger:
                        msg = (
                            f"Konfiguráció verziója ({loaded_version}) eltér a vártól "
                            f"({self._CURRENT_SCHEMA_VERSION}). "
                            "Kompatibilitási problémák léphetnek fel."
                        )
                        self._logger.warning(msg)

                # Verzióinformáció eltávolítása a konfigurációból
                config_data.pop("_schema_version", None)

                self._config = config_data
                self._filename = filename
        except (FileNotFoundError, yaml.YAMLError) as e:
            raise ConfigLoadError(f"Konfiguráció betöltése sikertelen: {str(e)}") from e

    def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        """Konfiguráció validálása séma alapján.

        Args:
            schema: A validációs séma definíció

        Returns:
            Tuple[bool, dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None)
        """
        ctx = ValidationContext(path="", errors={}, value=self._config, schema=schema)
        self._validate_dict(ctx)
        return not bool(ctx.errors), ctx.errors if ctx.errors else None

    def _validate_dict(self, ctx: ValidationContext) -> None:
        """Rekurzív séma validáció.

        Args:
            ctx: Validációs kontextus a konfigurációs adatokkal
        """
        if not isinstance(ctx.value, dict):
            ctx.errors[ctx.path] = "Dictionary típusú érték szükséges a validáláshoz"
            return

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
        """Kötelező mező ellenőrzése.

        Args:
            ctx: Validációs kontextus

        Returns:
            bool: True ha a mező érvényes, False ha hiányzik
        """
        if ctx.value is None and not ctx.schema.get("optional", False):
            ctx.errors[ctx.path] = "Kötelező mező hiányzik"
            return False
        return True

    def _validate_type(self, ctx: ValidationContext) -> bool:
        """Típus ellenőrzése.

        Args:
            ctx: Validációs kontextus

        Returns:
            bool: True ha a típus érvényes, False ha nem
        """
        if ctx.value is None:
            return True

        expected_type = ctx.schema.get("type")
        if not expected_type:
            return True

        expected_type_class = self._TYPE_MAP.get(expected_type)
        if not expected_type_class:
            ctx.errors[ctx.path] = f"Nem támogatott típus: {expected_type}"
            return False

        if not isinstance(ctx.value, expected_type_class):
            ctx.errors[ctx.path] = f"Érvénytelen típus, várt: {expected_type}"
            return False

        return True

    def _validate_nested(self, ctx: ValidationContext) -> None:
        """Beágyazott értékek validálása.

        Args:
            ctx: Validációs kontextus
        """
        if ctx.schema.get("type") == "dict" and "schema" in ctx.schema:
            if not isinstance(ctx.value, dict):
                ctx.errors[ctx.path] = "Dictionary típusú érték szükséges"
                return
            nested_ctx = ValidationContext(
                path=ctx.path,
                errors=ctx.errors,
                value=ctx.value,
                schema=ctx.schema["schema"],
            )
            self._validate_dict(nested_ctx)

    def _validate_constraints(self, ctx: ValidationContext) -> None:
        """Érték korlátok validálása.

        Args:
            ctx: Validációs kontextus
        """
        self._validate_choices(ctx)
        self._validate_range(ctx)

    def _validate_choices(self, ctx: ValidationContext) -> None:
        """Választható értékek validálása.

        Args:
            ctx: Validációs kontextus
        """
        choices = ctx.schema.get("choices")
        if choices is not None and ctx.value not in choices:
            ctx.errors[ctx.path] = f"Értéknek a következőek egyikének kell lennie: {choices}"

    def _validate_range(self, ctx: ValidationContext) -> None:
        """Érték tartományának validálása.

        Args:
            ctx: Validációs kontextus
        """
        if not isinstance(ctx.value, (int, float)):
            return

        min_value = ctx.schema.get("min")
        max_value = ctx.schema.get("max")

        if min_value is not None and ctx.value < min_value:
            ctx.errors[ctx.path] = f"Értéknek >= {min_value} kell lennie"
        if max_value is not None and ctx.value > max_value:
            ctx.errors[ctx.path] = f"Értéknek <= {max_value} kell lennie"

    def load_directory(self, path: str) -> None:
        """Betölti az összes YAML fájlt egy mappából namespaced struktúrába.

        A fájlneveket (kiterjesztés nélkül) használja kulcsként, és a tartalmukat
        az adott kulcs alá tölti be. A 'system.yaml' fájl tartalmát a gyökérbe is
        betölti az app_name, debug stb. elérhetősége érdekében.

        Args:
            path: A konfigurációs mappa útvonala

        Raises:
            ConfigLoadError: Ha a mappa nem található vagy betöltési hiba történik
        """
        if not os.path.exists(path):
            raise ConfigLoadError(f"Konfigurációs mappa nem található: {path}")

        if not os.path.isdir(path):
            raise ConfigLoadError(f"Az útvonal nem egy mappa: {path}")

        try:
            # Összes .yaml fájl listázása
            yaml_files = [f for f in os.listdir(path) if f.endswith((".yaml", ".yml"))]

            for filename in yaml_files:
                file_path = os.path.join(path, filename)

                # Fájlnév kiterjesztés nélkül (kulcsként használjuk)
                key = os.path.splitext(filename)[0]

                # DEBUG log a fájlbetöltéshez
                if self._logger:
                    self._logger.debug(f"Config betöltve: {filename}")

                # Fájl tartalmának betöltése
                with open(file_path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data:
                        # Tartalom elhelyezése a kulcs alatt
                        self._config[key] = data

                        # system.yaml speciális kezelése: gyökérbe is betöltjük
                        if key == "system":
                            # A gyökérbe csak azokat a kulcsokat töltjük, amik még nincsenek ott
                            for sys_key, sys_value in data.items():
                                if sys_key not in self._config:
                                    self._config[sys_key] = sys_value

        except (OSError, yaml.YAMLError) as e:
            raise ConfigLoadError(f"Konfigurációs mappa betöltése sikertelen: {str(e)}") from e
