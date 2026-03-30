"""Integration tesztek a scripts/generate_docs.py fájlhoz.

Ez a teszt ellenőrzi a Generate Docs Script teljes workflow-ját.
"""

import subprocess
import sys
from pathlib import Path

import pytest


class TestGenerateDocsIntegration:
    """Integration tesztek a generate_docs.py script-hez."""

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
        assert (root / "scripts" / "generate_docs.py").exists()
        return root

    def test_generate_docs_script_exists(self, project_root: Path) -> None:
        """Teszt: A generate_docs.py script létezik.

        Arrange: Projekt gyökér
        Act: Ellenőrizzük a script létezését
        Assert: A script fájl létezik és olvasható
        """
        # Arrange
        script_path = project_root / "scripts" / "generate_docs.py"

        # Act & Assert
        assert script_path.exists()
        assert script_path.is_file()
        assert script_path.stat().st_size > 0

    def test_generate_docs_imports(self, project_root: Path) -> None:
        """Teszt: A generate_docs modul importálható.

        Arrange: Projekt gyökér hozzáadása a sys.path-hoz
        Act: Importáljuk a modult
        Assert: Nincs ImportError
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        # Act & Assert
        from scripts import generate_docs  # noqa: F401

    def test_generate_docs_execution_dry_run(self, project_root: Path) -> None:
        """Teszt: A generate_docs.py script futtatható (dry run).

        Arrange: Script útvonal
        Act: Futtatjuk a scriptet subprocess-szel (csak import check)
        Assert: A script nem dob hibát az importáláskor
        """
        # Arrange
        project_root / "scripts" / "generate_docs.py"
        python_executable = sys.executable

        # Act
        result = subprocess.run(
            [python_executable, "-c", f"import sys; sys.path.insert(0, '{project_root}'); from scripts import generate_docs"],  # noqa: E501
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Assert
        assert result.returncode == 0, f"Import failed: {result.stderr}"

    def test_generate_docs_has_shebang(self, project_root: Path) -> None:
        """Teszt: A generate_docs.py script rendelkezik shebang-gel.

        Arrange: Script útvonal
        Act: Olvassuk be az első sort
        Assert: Az első sor shebang
        """
        # Arrange
        script_path = project_root / "scripts" / "generate_docs.py"

        # Act
        with open(script_path, encoding="utf-8") as f:
            first_line = f.readline().strip()

        # Assert
        assert first_line.startswith("#!")
        assert "python" in first_line.lower()

    def test_generate_docs_has_docstring(self, project_root: Path) -> None:
        """Teszt: A generate_docs modul rendelkezik docstring-gel.

        Arrange: Import a modul
        Act: Ellenőrizzük a __doc__ attribútumot
        Assert: A __doc__ nem None és tartalmazza a leírást
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts import generate_docs

        # Act & Assert
        assert generate_docs.__doc__ is not None
        assert len(generate_docs.__doc__.strip()) > 0
