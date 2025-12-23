#!/usr/bin/env python3
"""Teszt fájl a compile_mql.sh shell scripthez.

Ez egy dummy teszt, mivel a shell scriptet nehéz unit tesztelni.
A teszt ellenőrzi a script szintaxisát és alapvető funkcionalitását.

Fájl: tests/scripts/install/scripts/test_compile_mql.py
"""

import os
import subprocess  # nosec: B404 - trusted input only
from pathlib import Path

import pytest


class TestCompileMqlScript:
    """Tesztek a compile_mql.sh scripthez."""

    SCRIPT_PATH = Path("scripts/install/scripts/compile_mql.sh")

    def test_script_exists(self) -> None:
        """Ellenőrzi, hogy a script fájl létezik-e."""
        assert self.SCRIPT_PATH.exists(), f"A script nem létezik: {self.SCRIPT_PATH}"
        assert self.SCRIPT_PATH.is_file(), f"A script nem fájl: {self.SCRIPT_PATH}"

    def test_script_is_executable(self) -> None:
        """Ellenőrzi, hogy a script futtatható-e."""
        assert os.access(self.SCRIPT_PATH, os.X_OK), f"A script nem futtatható: {self.SCRIPT_PATH}"

    def test_script_syntax(self) -> None:
        """Ellenőrzi a bash script szintaxisát.

        Ez a teszt futtatja a `bash -n` parancsot a script szintaxisának
        ellenőrzésére anélkül, hogy végrehajtaná azt.
        """
        result = subprocess.run(  # nosec: B603, B607 - trusted input
            ["bash", "-n", str(self.SCRIPT_PATH)], capture_output=True, text=True
        )

        assert result.returncode == 0, (
            f"A script szintaxisa hibás.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )

    def test_script_has_shebang(self) -> None:
        """Ellenőrzi, hogy a script tartalmazza-e a shebang sort."""
        with open(self.SCRIPT_PATH, encoding="utf-8") as f:
            first_line = f.readline().strip()

        assert first_line.startswith("#!"), "A script nem tartalmaz shebang sort"
        assert "bash" in first_line, "A shebang nem bash-re mutat"

    def test_script_has_required_functions(self) -> None:
        """Ellenőrzi, hogy a script tartalmazza-e a szükséges függvényeket."""
        with open(self.SCRIPT_PATH, encoding="utf-8") as f:
            content = f.read()

        # Ellenőrizzük a fő függvények jelenlétét
        assert "compile_file()" in content, "Hiányzik a compile_file függvény"
        assert "copy_to_mt5()" in content, "Hiányzik a copy_to_mt5 függvény"

    def test_script_has_required_variables(self) -> None:
        """Ellenőrzi a szükséges konfigurációs változók jelenlétét."""
        with open(self.SCRIPT_PATH, encoding="utf-8") as f:
            content = f.read()

        required_vars = [
            "WINEPREFIX",
            "MQL_DIR",
            "METAEDITOR",
            "SOURCE_DIR",
            "OUTPUT_DIR",
            "COMPILED_DIR",
        ]

        for var in required_vars:
            assert var in content, f"Hiányzó változó: {var}"

    def test_script_has_color_definitions(self) -> None:
        """Ellenőrzi a színváltozók jelenlétét."""
        with open(self.SCRIPT_PATH, encoding="utf-8") as f:
            content = f.read()

        color_vars = ["RED", "GREEN", "YELLOW", "NC"]

        for var in color_vars:
            assert var in content, f"Hiányzó színváltozó: {var}"

    def test_script_has_hungarian_comments(self) -> None:
        """Ellenőrzi, hogy a script magyar kommenteket tartalmaz-e.

        Ez a teszt ellenőrzi, hogy a refaktorálás során hozzá lettek-e adva
        a magyar kommentek a scripthez.
        """
        with open(self.SCRIPT_PATH, encoding="utf-8") as f:
            content = f.read()

        # Ellenőrizzük néhány kulcsszó jelenlétét a magyar kommentekben
        hungarian_keywords = [
            "fordítás",
            "konfiguráció",
            "ellenőrzés",
            "másolás",
            "sikeres",
            "sikertelen",
        ]

        for keyword in hungarian_keywords:
            assert keyword.lower() in content.lower(), f"Hiányzó magyar kulcsszó: {keyword}"

    def test_script_handles_file_types(self) -> None:
        """Ellenőrzi, hogy a script kezeli-e a különböző fájltípusokat."""
        with open(self.SCRIPT_PATH, encoding="utf-8") as f:
            content = f.read()

        # Ellenőrizzük a fájltípus-kezelést
        assert "mq5)" in content, "Hiányzik az .mq5 fájltípus kezelése"
        assert "mqh)" in content, "Hiányzik a .mqh fájltípus kezelése"
        assert "Experts" in content, "Hiányzik az Experts mappa kezelése"

    @pytest.mark.skip(reason="Manuális teszt - Wine és MT5 telepítést igényel")
    def test_script_execution_with_wine(self) -> None:
        """Manuális teszt a script tényleges futtatásához.

        Ez a teszt csak akkor fut le, ha Wine és MetaTrader 5 telepítve van.
        Manuálisan kell futtatni a következő paranccsal:
        pytest tests/scripts/install/scripts/test_compile_mql.py::
        TestCompileMqlScript::test_script_execution_with_wine -v
        """
        # Ellenőrizzük, hogy Wine telepítve van-e
        try:
            subprocess.run(  # nosec: B603, B607 - trusted input
                ["wine", "--version"], check=True, capture_output=True
            )
            wine_installed = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            wine_installed = False

        if not wine_installed:
            pytest.skip("Wine nincs telepítve")

        # Ellenőrizzük, hogy a Wine prefix létezik-e
        wineprefix = os.environ.get("WINEPREFIX", os.path.expanduser("~/.mt5"))
        if not os.path.isdir(wineprefix):
            pytest.skip(f"Wine prefix nem létezik: {wineprefix}")

        # Ellenőrizzük, hogy MetaEditor létezik-e
        metaeditor_path = os.path.join(
            wineprefix, "drive_c", "Program Files", "MetaTrader 5", "MetaEditor64.exe"
        )
        if not os.path.isfile(metaeditor_path):
            pytest.skip(f"MetaEditor nem létezik: {metaeditor_path}")

        # Ha minden előfeltétel teljesül, futtathatjuk a scriptet
        # Ez a rész csak akkor fut le, ha ténylegesen tesztelni szeretnénk
        # a script működését egy teszt fájllal
        pass

    def test_documentation_exists(self) -> None:
        """Ellenőrzi, hogy a dokumentációs fájl létezik-e."""
        doc_path = Path("docs/components/scripts/install/scripts/compile_mql.md")
        assert doc_path.exists(), f"A dokumentáció nem létezik: {doc_path}"

    def test_documentation_is_complete(self) -> None:
        """Ellenőrzi, hogy a dokumentáció tartalmazza-e a szükséges részeket."""
        doc_path = Path("docs/components/scripts/install/scripts/compile_mql.md")

        with open(doc_path, encoding="utf-8") as f:
            content = f.read()

        required_sections = ["Áttekintés", "Funkciók", "Használat", "Előfeltételek", "Kimenet"]

        for section in required_sections:
            assert section in content, f"Hiányzó dokumentációs szakasz: {section}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
