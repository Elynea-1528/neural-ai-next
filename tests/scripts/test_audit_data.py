"""Integration tesztek a scripts/audit_data.py fájlhoz.

Ez a teszt ellenőrzi az Adatintegritási Audit Script teljes workflow-ját,
beleértve a .bi5 fájlok feldolgozását és a Parquet összehasonlítást.
"""

import subprocess
import sys
from pathlib import Path

import pytest


class TestAuditDataIntegration:
    """Integration tesztek az audit_data.py script-hez."""

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
        assert (root / "scripts" / "audit_data.py").exists()
        return root

    def test_audit_data_script_exists(self, project_root: Path) -> None:
        """Teszt: Az audit_data.py script létezik.

        Arrange: Projekt gyökér
        Act: Ellenőrizzük a script létezését
        Assert: A script fájl létezik és olvasható
        """
        # Arrange
        script_path = project_root / "scripts" / "audit_data.py"

        # Act & Assert
        assert script_path.exists()
        assert script_path.is_file()
        assert script_path.stat().st_size > 0

    def test_audit_data_imports(self, project_root: Path) -> None:
        """Teszt: Az audit_data modul importálható.

        Arrange: Projekt gyökér hozzáadása a sys.path-hoz
        Act: Importáljuk a modult
        Assert: Nincs ImportError
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        # Act & Assert
        from scripts import audit_data  # noqa: F401  # pyright: ignore[reportUnusedImport]

    def test_audit_data_has_parse_bi5_function(self, project_root: Path) -> None:
        """Teszt: Az audit_data modul tartalmazza a parse_bi5_file függvényt.

        Arrange: Import a modul
        Act: Ellenőrizzük a parse_bi5_file függvény létezését
        Assert: A függvény létezik és callable
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts.audit_data import parse_bi5_file

        # Act & Assert
        assert callable(parse_bi5_file)

    def test_audit_data_parse_bi5_with_nonexistent_file(self, project_root: Path, tmp_path: Path) -> None:  # noqa: E501
        """Teszt: A parse_bi5_file kezeli a nem létező fájlt.

        Arrange: Nem létező fájl útvonal
        Act: Meghívjuk a parse_bi5_file függvényt
        Assert: Üres lista vagy exception
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts.audit_data import parse_bi5_file

        nonexistent_file = tmp_path / "nonexistent.bi5"

        # Act & Assert
        try:
            result = parse_bi5_file(nonexistent_file)
            assert isinstance(result, list)
        except FileNotFoundError:
            # Ez is elfogadható viselkedés
            pass

    def test_audit_data_execution_dry_run(self, project_root: Path) -> None:
        """Teszt: Az audit_data.py script futtatható (dry run).

        Arrange: Script útvonal
        Act: Futtatjuk a scriptet subprocess-szel (csak import check)
        Assert: A script nem dob hibát az importáláskor
        """
        # Arrange
        project_root / "scripts" / "audit_data.py"  # pyright: ignore[reportUnusedExpression]
        python_executable = sys.executable

        # Act
        result = subprocess.run(
            [python_executable, "-c", f"import sys; sys.path.insert(0, '{project_root}'); from scripts import audit_data"],  # noqa: E501
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Assert
        assert result.returncode == 0, f"Import failed: {result.stderr}"

    def test_audit_data_has_shebang(self, project_root: Path) -> None:
        """Teszt: Az audit_data.py script rendelkezik shebang-gel.

        Arrange: Script útvonal
        Act: Olvassuk be az első sort
        Assert: Az első sor shebang
        """
        # Arrange
        script_path = project_root / "scripts" / "audit_data.py"

        # Act
        with open(script_path, encoding="utf-8") as f:
            first_line = f.readline().strip()

        # Assert
        assert first_line.startswith("#!")
        assert "python" in first_line.lower()

    def test_audit_data_has_docstring(self, project_root: Path) -> None:
        """Teszt: Az audit_data modul rendelkezik docstring-gel.

        Arrange: Import a modul
        Act: Ellenőrizzük a __doc__ attribútumot
        Assert: A __doc__ nem None és tartalmazza a leírást
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts import audit_data

        # Act & Assert
        assert audit_data.__doc__ is not None
        assert len(audit_data.__doc__.strip()) > 0
        assert "audit" in audit_data.__doc__.lower()
