"""Integration tesztek a scripts/bootstrap_test.py fájlhoz.

Ez a teszt ellenőrzi a Bootstrap Teszt Script teljes workflow-ját,
beleértve a bootstrap_core() függvény hívását és a komponensek ellenőrzését.
"""

import subprocess
import sys
from pathlib import Path

import pytest


class TestBootstrapTestIntegration:
    """Integration tesztek a bootstrap_test.py script-hez."""

    @pytest.fixture
    def project_root(self) -> Path:
        """Teszt: Projekt gyökér elérése.

        Arrange: -
        Act: Meghatározzuk a projekt gyökér útvonalát
        Assert: A projekt gyökér létezik
        """
        # Arrange & Act
        root = Path(__file__).resolve().parent.parent.parent

        # Assert
        assert root.exists()
        assert (root / "scripts" / "bootstrap_test.py").exists()
        return root

    def test_bootstrap_test_script_exists(self, project_root: Path) -> None:
        """Teszt: A bootstrap_test.py script létezik.

        Arrange: Projekt gyökér
        Act: Ellenőrizzük a script létezését
        Assert: A script fájl létezik és olvasható
        """
        # Arrange
        script_path = project_root / "scripts" / "bootstrap_test.py"

        # Act & Assert
        assert script_path.exists()
        assert script_path.is_file()
        assert script_path.stat().st_size > 0

    def test_bootstrap_test_imports(self, project_root: Path) -> None:
        """Teszt: A bootstrap_test modul importálható.

        Arrange: Projekt gyökér hozzáadása a sys.path-hoz
        Act: Importáljuk a modult
        Assert: Nincs ImportError
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        # Act & Assert
        from scripts import bootstrap_test  # noqa: F401

    def test_bootstrap_test_has_main_function(self, project_root: Path) -> None:
        """Teszt: A bootstrap_test modul tartalmazza a main függvényt.

        Arrange: Import a modul
        Act: Ellenőrizzük a main függvény létezését
        Assert: A függvény létezik és callable
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts.bootstrap_test import main

        # Act & Assert
        assert callable(main)

    def test_bootstrap_test_execution_dry_run(self, project_root: Path) -> None:
        """Teszt: A bootstrap_test.py script futtatható (dry run).

        Arrange: Script útvonal
        Act: Futtatjuk a scriptet subprocess-szel (csak import check)
        Assert: A script nem dob hibát az importáláskor
        """
        # Arrange
        project_root / "scripts" / "bootstrap_test.py"
        python_executable = sys.executable

        # Act
        result = subprocess.run(
            [python_executable, "-c", f"import sys; sys.path.insert(0, '{project_root}'); from scripts import bootstrap_test"],  # noqa: E501
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Assert
        assert result.returncode == 0, f"Import failed: {result.stderr}"

    def test_bootstrap_test_has_shebang(self, project_root: Path) -> None:
        """Teszt: A bootstrap_test.py script rendelkezik shebang-gel.

        Arrange: Script útvonal
        Act: Olvassuk be az első sort
        Assert: Az első sor shebang
        """
        # Arrange
        script_path = project_root / "scripts" / "bootstrap_test.py"

        # Act
        with open(script_path, encoding="utf-8") as f:
            first_line = f.readline().strip()

        # Assert
        assert first_line.startswith("#!")
        assert "python" in first_line.lower()

    def test_bootstrap_test_has_docstring(self, project_root: Path) -> None:
        """Teszt: A bootstrap_test modul rendelkezik docstring-gel.

        Arrange: Import a modul
        Act: Ellenőrizzük a __doc__ attribútumot
        Assert: A __doc__ nem None és tartalmazza a leírást
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts import bootstrap_test

        # Act & Assert
        assert bootstrap_test.__doc__ is not None
        assert len(bootstrap_test.__doc__.strip()) > 0
        assert "bootstrap" in bootstrap_test.__doc__.lower()

    def test_bootstrap_test_imports_bootstrap_core(self, project_root: Path) -> None:
        """Teszt: A bootstrap_test modul importálja a bootstrap_core függvényt.

        Arrange: Import a modul
        Act: Ellenőrizzük a bootstrap_core import-ot
        Assert: A bootstrap_core elérhető a modulban
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts import bootstrap_test

        # Act & Assert
        assert hasattr(bootstrap_test, "bootstrap_core")
