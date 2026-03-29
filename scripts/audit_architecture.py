"""Architecture Audit Script - Pre-audit a teljes projektre.

Ellenőrzi:
- Fájlnév konvenció (redundáns prefix-ek)
- Import típus (relatív vs abszolút)
- Struktúra (The Atomic Unit)
- Mirror Testing
- Export szabályok (__init__.py)

Output: docs/development/ARCHITECTURE_AUDIT.md
"""

import ast
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class FileIssue:
    """Egy fájl problémája."""

    file: Path
    category: Literal["filename", "import", "structure", "mirror", "export"]
    severity: Literal["critical", "warning"]
    message: str
    line: int | None = None


class ArchitectureAuditor:
    """Architecture audit végrehajtó."""

    def __init__(self) -> None:
        """Inicializálja az auditor-t."""
        self.issues: list[FileIssue] = []
        self.scan_dirs = [
            Path("neural_ai"),
            Path("tests"),
            Path("scripts"),
        ]
        self.ignored_dirs = {"__pycache__", ".pytest_cache", ".ruff_cache"}

    def scan_codebase(self) -> list[Path]:
        """Szkenneli a projektet."""
        python_files: list[Path] = []
        for scan_dir in self.scan_dirs:
            if not scan_dir.exists():
                continue
            for file in scan_dir.rglob("*.py"):
                if not any(ignored in str(file) for ignored in self.ignored_dirs):
                    python_files.append(file)
        return python_files

    def check_filename(self, file: Path) -> None:
        """Ellenőrzi a fájlnév konvenciót."""
        parts = file.parts
        if len(parts) >= 2:
            parent_name = parts[-2]
            file_name = file.stem

            # Ha a fájlnév tartalmazza a szülő mappa nevét
            if parent_name in file_name and file_name != parent_name:
                # pl. config/config_factory.py
                if file_name.startswith(parent_name + "_"):
                    suggested_name = file_name.replace(parent_name + "_", "")
                    self.issues.append(
                        FileIssue(
                            file=file,
                            category="filename",
                            severity="warning",
                            message=f"Redundáns prefix: '{file_name}.py' → '{suggested_name}.py'",
                        )
                    )

    def check_imports(self, file: Path) -> None:
        """Ellenőrzi az importokat."""
        try:
            with open(file, encoding="utf-8") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    # Relatív import keresése
                    if node.level > 0:
                        module_str = "." * node.level + (node.module or "")
                        self.issues.append(
                            FileIssue(
                                file=file,
                                category="import",
                                severity="critical",
                                message=f"Relatív import: {module_str}",
                                line=node.lineno,
                            )
                        )
        except (SyntaxError, FileNotFoundError, UnicodeDecodeError):
            pass

    def check_structure(self, file: Path) -> None:
        """Ellenőrzi a modul struktúrát."""
        # Csak neural_ai/ mappában
        if not str(file).startswith("neural_ai/"):
            return

        parts = file.parts
        # Ha ez egy modul gyökér (pl. neural_ai/core/logger/)
        if len(parts) >= 3 and file.name == "__init__.py":
            module_dir = file.parent

            # Ellenőrizzük, hogy van-e factory.py
            factory_file = module_dir / "factory.py"
            if not factory_file.exists():
                # Lehet, hogy ez egy almappa (interfaces/, implementations/)
                # Csak a fő moduloknál várjuk el a factory.py-t
                if module_dir.name not in [
                    "interfaces",
                    "implementations",
                    "exceptions",
                    "formatters",
                    "backends",
                    "mocks",
                ]:
                    # Ellenőrizzük, hogy van-e almappa (interfaces/, implementations/)
                    has_submodules = any(
                        (module_dir / subdir).exists()
                        for subdir in ["interfaces", "implementations", "exceptions"]
                    )
                    if has_submodules:
                        self.issues.append(
                            FileIssue(
                                file=file,
                                category="structure",
                                severity="warning",
                                message=f"Hiányzó factory.py a {module_dir.name} modulban",
                            )
                        )

    def check_mirror_test(self, file: Path) -> None:
        """Ellenőrzi a Mirror Testing szabályt."""
        # Csak neural_ai/ és scripts/ fájlokhoz
        if not (str(file).startswith("neural_ai/") or str(file).startswith("scripts/")):
            return

        # Kiszámítjuk a mirror test útvonalat
        if str(file).startswith("neural_ai/"):
            rel_path = str(file)[len("neural_ai/") :]
            parts = Path(rel_path).parts
            dir_parts = parts[:-1] if len(parts) > 1 else ()
            file_name = parts[-1] if parts else ""

            # __init__.py fájlokhoz test_init.py
            if file_name == "__init__.py":
                test_file = Path("tests/neural_ai") / Path(*dir_parts) / "test_init.py"
            else:
                test_file_name = f"test_{file_name}"
                test_file = Path("tests/neural_ai") / Path(*dir_parts) / test_file_name

        elif str(file).startswith("scripts/"):
            rel_path = str(file)[len("scripts/") :]
            parts = Path(rel_path).parts
            dir_parts = parts[:-1] if len(parts) > 1 else ()
            file_name = parts[-1] if parts else ""

            # __init__.py fájlokhoz test_init.py
            if file_name == "__init__.py":
                test_file = Path("tests/scripts") / Path(*dir_parts) / "test_init.py"
            else:
                test_file_name = f"test_{file_name}"
                test_file = Path("tests/scripts") / Path(*dir_parts) / test_file_name
        else:
            return

        if not test_file.exists():
            self.issues.append(
                FileIssue(
                    file=file,
                    category="mirror",
                    severity="warning",
                    message=f"Hiányzó mirror teszt: {test_file}",
                )
            )

    def check_exports(self, file: Path) -> None:
        """Ellenőrzi az export szabályokat (__init__.py)."""
        if file.name != "__init__.py":
            return

        try:
            with open(file, encoding="utf-8") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    # Implementáció import keresése
                    if node.module and "implementations" in node.module:
                        self.issues.append(
                            FileIssue(
                                file=file,
                                category="export",
                                severity="critical",
                                message=f"Implementáció import: {node.module}",
                                line=node.lineno,
                            )
                        )
        except (SyntaxError, FileNotFoundError, UnicodeDecodeError):
            pass

    def run_audit(self) -> None:
        """Futtatja az audit-ot."""
        print("🔍 Architecture Audit futtatása...")
        files = self.scan_codebase()
        print(f"✅ {len(files)} Python fájl találva")

        print("\n📊 Ellenőrzések futtatása...")
        for i, file in enumerate(files, 1):
            if i % 100 == 0:
                print(f"  ✅ {i}/{len(files)} fájl ellenőrizve")

            self.check_filename(file)
            self.check_imports(file)
            self.check_structure(file)
            self.check_mirror_test(file)
            self.check_exports(file)

        print(f"✅ {len(files)} fájl ellenőrizve")
        print(f"📋 {len(self.issues)} probléma találva")

    def generate_report(self) -> str:
        """Generálja a riportot."""
        # Csoportosítás severity szerint
        critical_issues = [i for i in self.issues if i.severity == "critical"]
        warning_issues = [i for i in self.issues if i.severity == "warning"]

        # Csoportosítás kategória szerint
        by_category: dict[str, list[FileIssue]] = {}
        for issue in self.issues:
            if issue.category not in by_category:
                by_category[issue.category] = []
            by_category[issue.category].append(issue)

        # Riport generálás
        report = f"""# 🔍 ARCHITECTURE AUDIT REPORT

**Generálva:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Szkennelt fájlok:** {len(self.scan_codebase())}
**Problémák száma:** {len(self.issues)}

## 📊 Összefoglaló

- 🔴 **Kritikus problémák:** {len(critical_issues)}
- 🟡 **Figyelmeztetések:** {len(warning_issues)}

## 🔴 Kritikus Problémák (Azonnal javítandó)

"""

        # Kritikus problémák kategóriánként
        for category in ["import", "export"]:
            cat_issues = [i for i in critical_issues if i.category == category]
            if cat_issues:
                category_names = {
                    "import": "Relatív Importok",
                    "export": "Implementáció Exportok",
                }
                report += f"\n### {category_names[category]} ({len(cat_issues)} db)\n\n"

                for issue in cat_issues[:20]:  # Max 20 példa
                    line_info = f" (sor {issue.line})" if issue.line else ""
                    report += f"- `{issue.file}`{line_info}\n  - {issue.message}\n"

                if len(cat_issues) > 20:
                    report += f"\n... és még {len(cat_issues) - 20} probléma\n"

        report += "\n## 🟡 Figyelmeztetések (Javítandó)\n\n"

        # Figyelmeztetések kategóriánként
        for category in ["filename", "structure", "mirror"]:
            cat_issues = [i for i in warning_issues if i.category == category]
            if cat_issues:
                category_names = {
                    "filename": "Fájlnév Konvenció",
                    "structure": "Modul Struktúra",
                    "mirror": "Mirror Testing",
                }
                report += f"\n### {category_names[category]} ({len(cat_issues)} db)\n\n"

                for issue in cat_issues[:20]:  # Max 20 példa
                    report += f"- `{issue.file}`\n  - {issue.message}\n"

                if len(cat_issues) > 20:
                    report += f"\n... és még {len(cat_issues) - 20} probléma\n"

        report += "\n## 📋 Részletes Statisztika\n\n"
        report += "| Kategória | Kritikus | Figyelmeztetés | Összesen |\n"
        report += "|:----------|:---------|:---------------|:---------|\n"

        for category in ["filename", "import", "structure", "mirror", "export"]:
            cat_critical = len([i for i in critical_issues if i.category == category])
            cat_warning = len([i for i in warning_issues if i.category == category])
            cat_total = cat_critical + cat_warning

            category_names = {
                "filename": "Fájlnév",
                "import": "Import",
                "structure": "Struktúra",
                "mirror": "Mirror Test",
                "export": "Export",
            }

            report += (
                f"| {category_names[category]} | {cat_critical} | "
                f"{cat_warning} | {cat_total} |\n"
            )

        report += (
            f"| **Összesen** | **{len(critical_issues)}** | "
            f"**{len(warning_issues)}** | **{len(self.issues)}** |\n"
        )

        return report

    def save_report(self, output_file: Path) -> None:
        """Menti a riportot."""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        report = self.generate_report()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n✅ Riport mentve: {output_file}")


if __name__ == "__main__":
    auditor = ArchitectureAuditor()
    auditor.run_audit()
    auditor.save_report(Path("docs/development/ARCHITECTURE_AUDIT.md"))

    print("\n🎉 Audit kész!")
    print("📄 Riport: docs/development/ARCHITECTURE_AUDIT.md")
