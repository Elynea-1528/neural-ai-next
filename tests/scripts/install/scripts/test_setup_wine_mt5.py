"""Teszt fájl a setup_wine_mt5.sh scripthez.

Ez egy bash telepítő script, amely Wine és MetaTrader 5 telepítését végzi
Linux rendszereken. A script rendszergazdai jogosultságot igényel és
interaktív telepítést végez, ezért automatikus unit tesztelés nehézkes.

MANUÁLIS TESZTELÉS SZÜKSÉGES:
- A script futtatása előtt ellenőrizni kell a rendszer kompatibilitást
- Szükséges sudo jogosultság a Wine telepítéséhez
- A telepítés során felhasználói interakció szükséges (bróker választás)
- A teszteléshez szükséges egy tesztkörnyezet (VM vagy dedikált teszt gép)

Author: Neural AI Next Team
Date: 2025-12-22
"""

import os
import unittest
from pathlib import Path


class TestSetupWineMT5(unittest.TestCase):
    """Teszt osztály a setup_wine_mt5.sh scripthez."""

    def test_script_file_exists(self):
        """Ellenőrzi, hogy a script fájl létezik-e."""
        script_path = Path("scripts/install/scripts/setup_wine_mt5.sh")
        self.assertTrue(script_path.exists(), "A setup_wine_mt5.sh fájlnak léteznie kell")

    def test_script_is_executable(self):
        """Ellenőrzi, hogy a script futtatható-e."""
        script_path = Path("scripts/install/scripts/setup_wine_mt5.sh")
        if script_path.exists():
            # Ellenőrizzük a fájl jogosultságokat
            stat_info = os.stat(script_path)
            is_executable = bool(stat_info.st_mode & 0o111)  # Execute permission
            self.assertTrue(
                is_executable or os.access(script_path, os.X_OK),
                "A scriptnek futtathatónak kell lennie",
            )

    def test_script_has_shebang(self):
        """Ellenőrzi, hogy a script tartalmazza-e a shebang sort."""
        script_path = Path("scripts/install/scripts/setup_wine_mt5.sh")
        if script_path.exists():
            with open(script_path, encoding="utf-8") as f:
                first_line = f.readline().strip()
                self.assertTrue(
                    first_line.startswith("#!"), "A scriptnek tartalmaznia kell shebang sort"
                )
                self.assertIn("bash", first_line, "A scriptnek bash interpretert kell használnia")

    def test_script_contains_required_variables(self):
        """Ellenőrzi, hogy a script tartalmazza-e a szükséges változókat."""
        script_path = Path("scripts/install/scripts/setup_wine_mt5.sh")
        if script_path.exists():
            with open(script_path, encoding="utf-8") as f:
                content = f.read()
                # Alapvető változók ellenőrzése
                required_vars = ["URL_MT5", "URL_WEBVIEW", "WINE_VERSION", "WINEPREFIX_MT5"]
                for var in required_vars:
                    self.assertIn(var, content, f"A scriptnek tartalmaznia kell a {var} változót")

    def test_script_contains_broker_selection(self):
        """Ellenőrzi, hogy a script tartalmazza-e a bróker választási logikát."""
        script_path = Path("scripts/install/scripts/setup_wine_mt5.sh")
        if script_path.exists():
            with open(script_path, encoding="utf-8") as f:
                content = f.read()
                # Bróker választási elemek ellenőrzése
                required_elements = [
                    "Válaszd ki a brókert",
                    "MetaTrader 5",
                    "XM Forex MT5",
                    "BROKER_CHOICE",
                    "case",
                ]
                for element in required_elements:
                    self.assertIn(element, content, f"A scriptnek tartalmaznia kell: {element}")

    def test_script_contains_wine_installation(self):
        """Ellenőrzi, hogy a script tartalmazza-e a Wine telepítési logikát."""
        script_path = Path("scripts/install/scripts/setup_wine_mt5.sh")
        if script_path.exists():
            with open(script_path, encoding="utf-8") as f:
                content = f.read()
                # Wine telepítési elemek ellenőrzése
                required_elements = ["winehq", "wine-mono", "wineboot", "winecfg"]
                for element in required_elements:
                    self.assertIn(element, content, f"A scriptnek tartalmaznia kell: {element}")

    def test_script_contains_webview_installation(self):
        """Ellenőrzi, hogy a script tartalmazza-e a WebView2 telepítést."""
        script_path = Path("scripts/install/scripts/setup_wine_mt5.sh")
        if script_path.exists():
            with open(script_path, encoding="utf-8") as f:
                content = f.read()
                self.assertIn(
                    "webview2.exe", content, "A scriptnek tartalmaznia kell a WebView2 telepítést"
                )

    def test_script_contains_cleanup(self):
        """Ellenőrzi, hogy a script tartalmazza-e a takarítási lépést."""
        script_path = Path("scripts/install/scripts/setup_wine_mt5.sh")
        if script_path.exists():
            with open(script_path, encoding="utf-8") as f:
                content = f.read()
                self.assertIn("rm -f", content, "A scriptnek tartalmaznia kell a takarítási lépést")

    def test_documentation_exists(self):
        """Ellenőrzi, hogy a dokumentációs fájl létezik-e."""
        doc_path = Path("docs/components/scripts/install/scripts/setup_wine_mt5.md")
        self.assertTrue(doc_path.exists(), "A dokumentációs fájlnak léteznie kell")


class ManualTestInstructions:
    """Manuális tesztelési utasítások a setup_wine_mt5.sh scripthez.

    Ezt a tesztelést KIZÁRÓLAG tesztkörnyezetben végezze el!
    """

    @staticmethod
    def get_manual_test_steps():
        """Visszaadja a manuális tesztelés lépéseit.

        Returns:
            list: A manuális tesztelés lépéseinek listája
        """
        return [
            "1. TESZTKÖRNYEZET LÉTREHOZÁSA",
            "   - Hozzon létre egy virtuális gépet vagy használjon dedikált teszt gépet",
            "   - Telepítse a támogatott Linux disztribúciót (Ubuntu/Fedora/Linux Mint/Debian)",
            "   - Győződjön meg róla, hogy van internetkapcsolat",
            "",
            "2. SCRIPT MÁSOLÁSA",
            "   - Másolja a setup_wine_mt5.sh fájlt a teszt gépére",
            "   - Futtathatóvá tétele: chmod +x setup_wine_mt5.sh",
            "",
            "3. FUTTATÁS ÉS ELLENŐRZÉS",
            "   - Futtassa a scriptet: ./setup_wine_mt5.sh",
            "   - Válassza ki a brókert (1 vagy 2)",
            "   - Figyelje a telepítési folyamatot",
            "   - Ellenőrizze, hogy minden lépés sikeresen lefutott-e",
            "",
            "4. WINE ELLENŐRZÉSE",
            "   - Ellenőrizze a Wine verziót: wine --version",
            "   - Ellenőrizze a Wine prefix létrejöttét: ls -la ~/.mt5",
            "",
            "5. MT5 INDÍTÁSA",
            "   - Indítsa el az MT5-öt a script által megadott utasítások szerint",
            "   - Ellenőrizze, hogy az MT5 megfelelően indul-e el",
            "",
            "6. FUNKCIONÁLIS TESZT",
            "   - Hozzon létre egy demo fiókot",
            "   - Ellenőrizze az alapvető funkcionalitást",
            "   - Zárja be az MT5-öt és indítsa újra",
            "",
            "7. VISSZATELEPÍTÉS TESZT (opcionális)",
            "   - Távolítsa el a ~/.mt5 mappát",
            "   - Futtassa újra a scriptet",
            "   - Ellenőrizze, hogy a második telepítés is sikeres-e",
            "",
            "⚠️ FIGYELEM:",
            "   - A script rendszergazdai jogosultságot igényel",
            "   - A telepítés hosszú ideig tarthat",
            "   - Szükség lehet a rendszer újraindítására",
            "   - Csak tesztkörnyezetben futtassa!",
        ]


def run_manual_test_checklist():
    """Futtatja a manuális teszt ellenőrzőlistát."""
    print("=" * 60)
    print("MANUÁLIS TESZTELÉSI ELLENŐRZŐLISTA")
    print("=" * 60)
    print()

    steps = ManualTestInstructions.get_manual_test_steps()
    for step in steps:
        print(step)

    print()
    print("=" * 60)
    print("TESZTELÉS ÁLLAPOTA: MANUÁLIS TESZT SZÜKSÉGES")
    print("=" * 60)


if __name__ == "__main__":
    # Unit tesztek futtatása
    unittest.main(verbosity=2, exit=False)

    print("\n")
    # Manuális tesztelési utasítások megjelenítése
    run_manual_test_checklist()
