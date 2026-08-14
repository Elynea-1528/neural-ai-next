"""ConfigLoader implementáció SOPS támogatással.

Ez a modul tartalmazza a ConfigLoader osztályt, amely képes plain YAML és
SOPS titkosított YAML fájlok betöltésére. A SOPS dekódolás subprocess-en
keresztül történik a `sops -d` paranccsal.

Attributes:
    ConfigLoader: Konfiguráció betöltő osztály SOPS támogatással.
"""

import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import yaml

from neural_ai.core.config.exceptions import ConfigLoadError, SOPSDecryptError
from neural_ai.core.config.interfaces.config_loader_interface import IConfigLoader

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces import LoggerInterface


class ConfigLoader(IConfigLoader):
    """Konfiguráció betöltő SOPS támogatással.

    Ez az osztály képes plain YAML és SOPS titkosított YAML fájlok betöltésére.
    A SOPS fájlokat a `sops -d` paranccsal dekódolja subprocess-en keresztül.

    Képességek:
        - Plain YAML fájlok betöltése (yaml.safe_load)
        - SOPS titkosított YAML fájlok dekódolása (subprocess sops -d)
        - Könyvtár szintű betöltés (namespace struktúra)
        - Automatikus detektálás (.yaml.sops kiterjesztés)

    Attributes:
        _logger: Logger interfész (opcionális).
        _sops_binary: SOPS binary útvonala (default: "sops").

    Example:
        >>> loader = ConfigLoader()
        >>> config = loader.load_file("configs/database.yaml")
        >>> print(config["host"])
        localhost

        >>> secure_loader = ConfigLoader(sops_binary="/usr/local/bin/sops")
        >>> secrets = secure_loader.load_file("configs/secrets.yaml.sops")
        >>> print(secrets["api_key"])
        secret_key_value

        >>> all_configs = loader.load("configs/")
        >>> print(all_configs.keys())
        dict_keys(['database', 'secrets', 'logging'])
    """

    def __init__(
        self,
        logger: "LoggerInterface | None" = None,
        sops_binary: str = "sops"
    ) -> None:
        """Inicializálja a ConfigLoader-t.

        Args:
            logger: Logger interfész a naplózáshoz (opcionális).
            sops_binary: SOPS binary útvonala (default: "sops" a PATH-ból).
        """
        self._logger = logger
        self._sops_binary = sops_binary

    def _is_sops_file(self, file_path: str) -> bool:
        """Ellenőrzi, hogy SOPS fájlról van-e szó.

        A detektálás a .yaml.sops vagy .yml.sops kiterjesztés alapján történik.

        Args:
            file_path: Fájl útvonala.

        Returns:
            True ha SOPS fájl, False egyébként.

        Example:
            >>> loader = ConfigLoader()
            >>> loader._is_sops_file("config.yaml.sops")
            True
            >>> loader._is_sops_file("config.yaml")
            False
        """
        return file_path.endswith(".yaml.sops") or file_path.endswith(".yml.sops")

    def _decrypt_sops_file(self, file_path: str) -> str:
        """SOPS fájl dekódolása subprocess-el.

        Futtatja a `sops -d <file_path>` parancsot és visszaadja a dekódolt
        YAML tartalmat string formátumban.

        Args:
            file_path: SOPS fájl útvonala.

        Returns:
            Dekódolt YAML tartalom (string).

        Raises:
            SOPSDecryptError: Ha a dekódolás sikertelen (pl. SOPS nincs telepítve,
                vagy a fájl dekódolása nem lehetséges).

        Example:
            >>> loader = ConfigLoader()
            >>> content = loader._decrypt_sops_file("secrets.yaml.sops")
            >>> print(type(content))
            <class 'str'>
        """
        try:
            result = subprocess.run(
                [self._sops_binary, "-d", file_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=30  # 30 sec timeout
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            # SOPS parancs hiba (pl. rossz fájl formátum, nincs kulcs)
            raise SOPSDecryptError(
                f"SOPS dekódolás sikertelen: {e.stderr}",
                file_path=file_path,
                sops_command=f"{self._sops_binary} -d {file_path}",
                exit_code=e.returncode
            ) from e
        except FileNotFoundError as e:
            # SOPS binary nem található
            raise SOPSDecryptError(
                f"SOPS binary nem található: {self._sops_binary}. "
                f"Telepítsd a SOPS-t: https://github.com/getsops/sops",
                file_path=file_path,
                sops_command=f"{self._sops_binary} -d {file_path}",
                exit_code=None
            ) from e
        except subprocess.TimeoutExpired as e:
            # Timeout hiba
            raise SOPSDecryptError(
                f"SOPS dekódolás timeout (30s): {file_path}",
                file_path=file_path,
                sops_command=f"{self._sops_binary} -d {file_path}",
                exit_code=None
            ) from e

    def load_file(self, file_path: str) -> dict[str, Any]:
        """Betölt egyetlen config fájlt (SOPS vagy plain YAML).

        Automatikusan detektálja a .yaml.sops kiterjesztést és SOPS
        dekódolást alkalmaz szükség esetén.

        Args:
            file_path: Fájl útvonala (.yaml vagy .yaml.sops).

        Returns:
            Fájl tartalma dictionary formában.

        Raises:
            ConfigLoadError: Ha fájl nem található vagy betöltési hiba történik.
            SOPSDecryptError: Ha SOPS fájl dekódolása sikertelen.

        Example:
            >>> loader = ConfigLoader()
            >>> config = loader.load_file("configs/database.yaml")
            >>> print(config["host"])
            localhost

            >>> secrets = loader.load_file("configs/secrets.yaml.sops")
            >>> print(type(secrets))
            <class 'dict'>
        """
        if not os.path.exists(file_path):
            raise ConfigLoadError(
                f"Config fájl nem található: {file_path}",
                file_path=file_path
            )

        try:
            # SOPS fájl detektálás és dekódolás
            if self._is_sops_file(file_path):
                if self._logger:
                    self._logger.debug(
                        "SOPS fájl dekódolása",
                        extra={"file_path": file_path}
                    )

                yaml_content = self._decrypt_sops_file(file_path)
                data = yaml.safe_load(yaml_content)
            else:
                # Plain YAML betöltés
                with open(file_path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)

            # Üres fájl kezelése
            if data is None:
                if self._logger:
                    self._logger.warning(
                        "Üres config fájl",
                        extra={"file_path": file_path}
                    )
                return {}

            # Típus ellenőrzés
            if not isinstance(data, dict):
                raise ConfigLoadError(
                    f"Config fájl nem dictionary típusú: {file_path}",
                    file_path=file_path
                )

            # Explicit type cast a type checker számára
            result = cast(dict[str, Any], data)

            if self._logger:
                self._logger.debug(
                    "Config fájl betöltve",
                    extra={"file_path": file_path, "keys": len(result)}
                )

            return result

        except (yaml.YAMLError, OSError) as e:
            # YAML parse hiba vagy fájl olvasási hiba
            raise ConfigLoadError(
                f"Config fájl betöltése sikertelen: {e}",
                file_path=file_path,
                original_error=e
            ) from e

    def load(self, config_dir: str) -> dict[str, Any]:
        """Betölti az összes config fájlt egy könyvtárból.

        A fájlneveket (kiterjesztés nélkül) használja kulcsként, és a tartalmukat
        az adott kulcs alá tölti be namespace struktúrába.

        Args:
            config_dir: Konfiguráció könyvtár útvonala.

        Returns:
            Egyesített konfiguráció dictionary (namespace struktúra).

        Raises:
            ConfigLoadError: Ha a könyvtár nem található.
            SOPSDecryptError: Ha SOPS dekódolás sikertelen.

        Example:
            >>> loader = ConfigLoader()
            >>> config = loader.load("configs/")
            >>> print(config.keys())
            dict_keys(['database', 'secrets', 'logging'])

            >>> print(config["database"]["host"])
            localhost

        Note:
            Fájlnév → kulcs konverzió:
                - secrets.yaml.sops → "secrets"
                - database.yaml → "database"
                - logging.yml → "logging"
        """
        if not os.path.exists(config_dir):
            raise ConfigLoadError(
                f"Config könyvtár nem található: {config_dir}",
                file_path=config_dir
            )

        if not os.path.isdir(config_dir):
            raise ConfigLoadError(
                f"Az útvonal nem könyvtár: {config_dir}",
                file_path=config_dir
            )

        merged_config: dict[str, Any] = {}

        # Összes .yaml és .yaml.sops fájl listázása
        config_files = [
            f for f in os.listdir(config_dir)
            if f.endswith((".yaml", ".yml", ".yaml.sops", ".yml.sops"))
        ]

        if self._logger:
            self._logger.info(
                "Config könyvtár betöltése",
                extra={"config_dir": config_dir, "files": len(config_files)}
            )

        for filename in config_files:
            file_path = os.path.join(config_dir, filename)

            # Fájlnév → kulcs (kiterjesztés nélkül)
            # secrets.yaml.sops → secrets
            # database.yaml → database
            key = Path(filename).stem
            if key.endswith(".yaml"):
                key = key[:-5]  # .yaml.sops esetén .yaml levágása

            # Fájl betöltése
            file_data = self.load_file(file_path)

            # Namespace struktúrába helyezés
            merged_config[key] = file_data

        if self._logger:
            self._logger.info(
                "Config könyvtár betöltve",
                extra={
                    "config_dir": config_dir,
                    "namespaces": list(merged_config.keys())
                }
            )

        return merged_config
