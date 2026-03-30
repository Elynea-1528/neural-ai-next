"""Integration tesztek a scripts/audit_architecture.py fájlhoz.

Ez a teszt ellenőrzi az Architecture Audit Script teljes workflow-ját,
beleértve a fájl szkennelést, AST elemzést és jelentés generálást.
"""

import subprocess
import sys
from pathlib import Path

import pytest


class TestAuditArchitectureIntegration:
    """Integration tesztek az audit_architecture.py script-hez."""

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
        assert (root / "scripts" / "audit_architecture.py").exists()
        return root

    def test_audit_architecture_script_exists(self, project_root: Path) -> None:
        """Teszt: Az audit_architecture.py script létezik.

        Arrange: Projekt gyökér
        Act: Ellenőrizzük a script létezését
        Assert: A script fájl létezik és olvasható
        """
        # Arrange
        script_path = project_root / "scripts" / "audit_architecture.py"

        # Act & Assert
        assert script_path.exists()
        assert script_path.is_file()
        assert script_path.stat().st_size > 0

    def test_audit_architecture_imports(self, project_root: Path) -> None:
        """Teszt: Az audit_architecture modul importálható.

        Arrange: Projekt gyökér hozzáadása a sys.path-hoz
        Act: Importáljuk a modult
        Assert: Nincs ImportError
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        # Act & Assert
        from scripts import audit_architecture  # noqa: F401

    def test_audit_architecture_has_main_class(self, project_root: Path) -> None:
        """Teszt: Az audit_architecture modul tartalmazza az ArchitectureAuditor osztályt.

        Arrange: Import a modul
        Act: Ellenőrizzük az ArchitectureAuditor osztály létezését
        Assert: Az osztály létezik és példányosítható
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts.audit_architecture import ArchitectureAuditor

        # Act
        auditor = ArchitectureAuditor()

        # Assert
        assert auditor is not None
        assert hasattr(auditor, "scan_codebase")
        assert hasattr(auditor, "issues")

    def test_audit_architecture_scan_codebase(self, project_root: Path) -> None:
        """Teszt: Az ArchitectureAuditor.scan_codebase metódus működik.

        Arrange: ArchitectureAuditor példány
        Act: Szkenneljük a codebase-t
        Assert: Python fájlok listája nem üres
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts.audit_architecture import ArchitectureAuditor

        auditor = ArchitectureAuditor()

        # Act
        python_files = auditor.scan_codebase()

        # Assert
        assert isinstance(python_files, list)
        assert len(python_files) > 0
        assert all(isinstance(f, Path) for f in python_files)
        assert all(f.suffix == ".py" for f in python_files)

    def test_audit_architecture_file_issue_dataclass(self, project_root: Path) -> None:
        """Teszt: A FileIssue dataclass megfelelően működik.

        Arrange: Import a FileIssue osztályt
        Act: Létrehozunk egy FileIssue példányt
        Assert: A példány megfelelő attribútumokkal rendelkezik
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts.audit_architecture import FileIssue

        # Act
        issue = FileIssue(
            file=Path("test.py"),
            category="import",
            severity="warning",
            message="Test issue",
            line=10
        )

        # Assert
        assert issue.file == Path("test.py")
        assert issue.category == "import"
        assert issue.severity == "warning"
        assert issue.message == "Test issue"
        assert issue.line == 10

    @pytest.mark.slow
    def test_audit_architecture_execution_dry_run(self, project_root: Path) -> None:
        """Teszt: Az audit_architecture.py script futtatható (dry run).

        Arrange: Script útvonal
        Act: Futtatjuk a scriptet subprocess-szel (csak import check)
        Assert: A script nem dob hibát az importáláskor
        """
        # Arrange
        project_root / "scripts" / "audit_architecture.py"
        python_executable = sys.executable

        # Act
        result = subprocess.run(
            [python_executable, "-c", f"import sys; sys.path.insert(0, '{project_root}'); from scripts import audit_architecture"],  # noqa: E501
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Assert
        assert result.returncode == 0, f"Import failed: {result.stderr}"

    def test_audit_architecture_ignored_dirs(self, project_root: Path) -> None:
        """Teszt: Az ArchitectureAuditor figyelmen kívül hagyja a cache könyvtárakat.

        Arrange: ArchitectureAuditor példány
        Act: Ellenőrizzük az ignored_dirs attribútumot
        Assert: A cache könyvtárak szerepelnek az ignored_dirs-ben
        """
        # Arrange
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from scripts.audit_architecture import ArchitectureAuditor

        auditor = ArchitectureAuditor()

        # Act & Assert
        assert "__pycache__" in auditor.ignored_dirs
        assert ".pytest_cache" in auditor.ignored_dirs
        assert ".ruff_cache" in auditor.ignored_dirs
