#!/usr/bin/env python3
"""TASK_TREE v3.0 Deep Auditor - AST-alapú kódminőség audit.

Ez a script rekurzívan bejárja a neural_ai/ mappát, AST analízissel feltérképezi
a kódbázist és generálja a docs/development/TASK_TREE.md dashboardot.
"""

import ast
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal


@dataclass
class FileAnalysis:
    """Egyetlen fájl analízis eredménye."""

    path: Path
    relative_path: str
    test_file_exists: bool
    test_file_path: Path | None
    test_count: int
    config_status: Literal["✅ OK", "🔴 TYPED_DICT", "⚪ N/A"]
    logger_status: Literal["✅ OK", "⚠️ UNUSED", "🔴 MISSING", "⚪ N/A"]
    overall_status: Literal["✅ SECURE", "🟡 WARNING", "🔴 VULNERABLE"]
    notes: str


class ASTAnalyzer:
    """AST-alapú Python fájl elemző."""

    def __init__(self, file_path: Path) -> None:
        """Inicializálja az analizátort."""
        self.file_path = file_path
        self.tree: ast.AST | None = None

    def parse(self) -> bool:
        """Beolvassa és parse-olja a fájlt."""
        try:
            with open(self.file_path, encoding="utf-8") as f:
                content = f.read()
            self.tree = ast.parse(content)
            return True
        except (SyntaxError, FileNotFoundError, UnicodeDecodeError):
            return False

    def check_config_type(self) -> Literal["✅ OK", "🔴 TYPED_DICT", "⚪ N/A"]:
        """Ellenőrzi a config típusát (Pydantic vs TypedDict)."""
        if not self.tree:
            return "⚪ N/A"

        has_pydantic = False
        has_typeddict = False

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ImportFrom):
                if node.module == "pydantic":
                    if any(alias.name == "BaseModel" for alias in node.names):
                        has_pydantic = True
                elif node.module == "typing":
                    if any(alias.name == "TypedDict" for alias in node.names):
                        has_typeddict = True

        if has_pydantic:
            return "✅ OK"
        elif has_typeddict:
            return "🔴 TYPED_DICT"
        return "⚪ N/A"

    def check_logger_injection(self) -> Literal["✅ OK", "⚠️ UNUSED", "🔴 MISSING", "⚪ N/A"]:
        """Ellenőrzi a logger dependency injection-t."""
        if not self.tree:
            return "⚪ N/A"

        logger_injected = False
        logger_used = False

        # Keres __init__ metódust logger paraméterrel
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                for arg in node.args.args:
                    if arg.arg == "logger":
                        logger_injected = True
                        break

        # Keres self.logger.* használatot
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Attribute):
                    if (
                        isinstance(node.value.value, ast.Name)
                        and node.value.value.id == "self"
                        and node.value.attr == "logger"
                    ):
                        logger_used = True
                        break

        if logger_injected and logger_used:
            return "✅ OK"
        elif logger_injected and not logger_used:
            return "⚠️ UNUSED"
        elif not logger_injected and logger_used:
            return "🔴 MISSING"
        return "⚪ N/A"

    def count_tests(self) -> int:
        """Megszámolja a test_ prefixű függvényeket."""
        if not self.tree:
            return 0

        count = 0
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("test_"):
                    count += 1
        return count


class MirrorChecker:
    """Mirror Rule ellenőrző (neural_ai/x.py ↔ tests/x/test_x.py)."""

    @staticmethod
    def get_test_path(source_path: Path) -> Path:
        """Kiszámítja a mirror test fájl útvonalát.

        Ha a test_X.py nem létezik, megpróbálja a test_X_integration.py-t is.
        Ha implementations/interfaces/exceptions mappában van, a szülő mappában is keres.
        """
        # neural_ai/processors/dimensions/d01_price/processor.py
        # → tests/processors/dimensions/d01_price/test_processor.py

        parts = source_path.parts
        if parts[0] != "neural_ai":
            raise ValueError(f"Nem neural_ai/-ból származó fájl: {source_path}")

        # Eltávolítjuk a "neural_ai/" prefix-et
        relative_parts = parts[1:]  # processors/dimensions/d01_price/processor.py

        # Szétválasztjuk könyvtár és fájl
        dir_parts = relative_parts[:-1]  # processors/dimensions/d01_price
        file_name = relative_parts[-1]  # processor.py

        # test_ prefix hozzáadása
        test_file_name = f"test_{file_name}"
        base_name = file_name.replace('.py', '')
        integration_file_name = f"test_{base_name}_integration.py"

        # 1. Elsődleges hely (Mirror Rule szerint)
        test_path = Path("tests") / Path(*dir_parts) / test_file_name

        # DEBUG: Útvonal ellenőrzés (csak UI fájloknál, hogy lássuk a hibát)
        if "ui" in str(source_path):
            print(f"DEBUG: Checking {source_path} -> {test_path} (Exists: {test_path.exists()})")

        if test_path.exists():
            return test_path

        # UI Services Fallback (ha a standard logika valamiért nem találja)
        if "ui" in dir_parts and "services" in dir_parts:
             ui_test_path = Path("tests/ui/services") / test_file_name
             if ui_test_path.exists():
                 print(f"DEBUG: FOUND via fallback: {ui_test_path}")
                 return ui_test_path

        # 2. Integration verzió (Mirror Rule szerint)
        integration_path = Path("tests") / Path(*dir_parts) / integration_file_name
        if integration_path.exists():
            return integration_path

        # 3. Ha implementations/interfaces/exceptions mappában van, szülő mappában is keres
        if dir_parts and dir_parts[-1] in ["implementations", "interfaces", "exceptions"]:
            parent_dir_parts = dir_parts[:-1]

            # 3a. Szülő mappában test_X.py
            parent_test_path = Path("tests") / Path(*parent_dir_parts) / test_file_name
            if parent_test_path.exists():
                return parent_test_path

            # 3b. Szülő mappában test_X_integration.py
            parent_integration_path = (
                Path("tests") / Path(*parent_dir_parts) / integration_file_name
            )
            if parent_integration_path.exists():
                return parent_integration_path

        # Ha sehol nem találtuk, visszaadjuk az eredeti Mirror Rule szerinti helyet
        return test_path

    @staticmethod
    def check_mirror(source_path: Path) -> tuple[bool, Path]:
        """Ellenőrzi, hogy létezik-e a mirror teszt fájl."""
        test_path = MirrorChecker.get_test_path(source_path)
        exists = test_path.exists()
        return exists, test_path


class StatusCalculator:
    """Státusz kalkulátor logika."""

    @staticmethod
    def calculate(analysis: FileAnalysis) -> Literal["✅ SECURE", "🟡 WARNING", "🔴 VULNERABLE"]:
        """Kiszámítja az overall státuszt."""
        # 🔴 VULNERABLE feltételek
        if (
            not analysis.test_file_exists
            or analysis.test_count == 0
            or analysis.config_status == "🔴 TYPED_DICT"
            or analysis.logger_status == "🔴 MISSING"
        ):
            return "🔴 VULNERABLE"

        # ✅ SECURE feltételek
        if (
            analysis.test_file_exists
            and analysis.test_count > 0
            and analysis.config_status in ["✅ OK", "⚪ N/A"]
            and analysis.logger_status in ["✅ OK", "⚪ N/A"]
        ):
            return "✅ SECURE"

        # 🟡 WARNING: minden más
        return "🟡 WARNING"

    @staticmethod
    def generate_notes(analysis: FileAnalysis) -> str:
        """Generál teendő megjegyzéseket."""
        if analysis.overall_status == "✅ SECURE":
            return "-"

        notes: list[str] = []
        if not analysis.test_file_exists or analysis.test_count == 0:
            notes.append("**KRITIKUS: Teszt írás!**")
        if analysis.config_status == "🔴 TYPED_DICT":
            notes.append("**Migráld Pydantic-ra!**")
        if analysis.logger_status == "🔴 MISSING":
            notes.append("**Logger DI hiányzik!**")

        return " | ".join(notes) if notes else "-"


class MarkdownGenerator:
    """TASK_TREE.md generátor."""

    LAYER_MAPPING = {
        "core": ("1", "Infrastructure", "neural_ai/core/"),
        "collectors": ("2", "Input", "neural_ai/collectors/"),
        "data": ("3", "Persistence", "neural_ai/data/"),
        "processors": ("4", "Domain", "neural_ai/processors/"),
        "ui": ("5", "Presentation", "neural_ai/ui/"),
    }

    def __init__(self, analyses: list[FileAnalysis]) -> None:
        """Inicializálja a generátort."""
        self.analyses = analyses
        self.grouped = self._group_by_layer()

    def _group_by_layer(self) -> dict[str, list[FileAnalysis]]:
        """Csoportosítja a fájlokat réteg szerint."""
        grouped: dict[str, list[FileAnalysis]] = {layer: [] for layer in self.LAYER_MAPPING.keys()}

        for analysis in self.analyses:
            parts = Path(analysis.relative_path).parts
            # parts[0] = "neural_ai", parts[1] = "core/collectors/data/processors/ui"
            if len(parts) > 1 and parts[1] in self.LAYER_MAPPING:
                grouped[parts[1]].append(analysis)

        return grouped

    def calculate_statistics(self) -> dict[str, int]:
        """Statisztikákat számol."""
        stats = {
            "total": len(self.analyses),
            "secure": 0,
            "warning": 0,
            "vulnerable": 0,
            "tested": 0,
        }

        for analysis in self.analyses:
            if analysis.overall_status == "✅ SECURE":
                stats["secure"] += 1
            elif analysis.overall_status == "🟡 WARNING":
                stats["warning"] += 1
            elif analysis.overall_status == "🔴 VULNERABLE":
                stats["vulnerable"] += 1

            if analysis.test_file_exists:
                stats["tested"] += 1

        return stats

    def _create_table(self, layer: str, files: list[FileAnalysis]) -> str:
        """Létrehoz egy táblázatot egy réteghez."""
        if not files:
            return ""

        num, name, path = self.LAYER_MAPPING[layer]

        lines = [
            f"### {num}. {name} Layer (`{path}`)",
            "",
            (
                "| Modul / Fájl | Státusz | Teszt Pár | Tesztek Száma | "
                "Config (Pydantic) | Logger (DI) | Coverage | Teendők / Megjegyzés |"
            ),
            (
                "|--------------|---------|-----------|---------------|"
                "-------------------|-------------|----------|----------------------|"
            ),
        ]

        for file in sorted(files, key=lambda x: x.relative_path):
            # Rövidített fájl név
            short_path = file.relative_path.replace("neural_ai/", "")
            test_pair = "✅ FOUND" if file.test_file_exists else "❌ MISSING"

            row = (
                f"| `{short_path}` "
                f"| {file.overall_status} "
                f"| {test_pair} "
                f"| {file.test_count} "
                f"| {file.config_status} "
                f"| {file.logger_status} "
                f"| N/A "
                f"| {file.notes} |"
            )
            lines.append(row)

        lines.append("")
        return "\n".join(lines)

    def generate(self) -> str:
        """Generálja a teljes TASK_TREE.md tartalmat."""
        stats = self.calculate_statistics()
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

        lines = [
            "# 🌳 NEURAL AI NEXT - TASK TREE v3.0 (DEEP AUDIT)",
            "",
            f"**Generálva:** {now}",
            "**Módszer:** AST Statikus Analízis",
            f"**Fájlok száma:** {stats['total']} elemezve",
            "",
            "---",
            "",
            "## 📊 ÖSSZESÍTŐ STATISZTIKA",
            "",
            (
                f"- **✅ SECURE**: {stats['secure']} fájl "
                f"({stats['secure'] / stats['total'] * 100:.1f}%)"
            ),
            (
                f"- **🟡 WARNING**: {stats['warning']} fájl "
                f"({stats['warning'] / stats['total'] * 100:.1f}%)"
            ),
            (
                f"- **🔴 VULNERABLE**: {stats['vulnerable']} fájl "
                f"({stats['vulnerable'] / stats['total'] * 100:.1f}%)"
            ),
            (
                f"- **Teszt lefedettség**: {stats['tested']}/{stats['total']} fájl "
                f"({stats['tested'] / stats['total'] * 100:.1f}%)"
            ),
            "",
            "---",
            "",
            "## 📂 RÉSZLETES AUDIT EREDMÉNYEK (DDD RÉTEGEK)",
            "",
        ]

        # Rétegek sorrendben
        for layer in ["core", "collectors", "data", "processors", "ui"]:
            if layer in self.grouped and self.grouped[layer]:
                table = self._create_table(layer, self.grouped[layer])
                lines.append(table)
                lines.append("---")
                lines.append("")

        return "\n".join(lines)


class TaskTreeGenerator:
    """Fő orchestrator osztály."""

    def __init__(
        self,
        source_dir: str = "neural_ai",
        output_file: str = "docs/development/TASK_TREE.md",
    ) -> None:
        """Inicializálja a generátort."""
        self.source_dir = Path(source_dir)
        self.output_file = Path(output_file)
        self.ignored_dirs = {"__pycache__", ".pytest_cache", ".ruff_cache"}
        self.ignored_files = {"__init__.py"}

    def scan_codebase(self) -> list[Path]:
        """Rekurzívan bejárja a neural_ai/ mappát."""
        python_files: list[Path] = []

        for root, dirs, files in os.walk(self.source_dir):
            # Kihagyott könyvtárak szűrése
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]

            for file in files:
                if file.endswith(".py") and file not in self.ignored_files:
                    python_files.append(Path(root) / file)

        return python_files

    def analyze_file(self, file_path: Path) -> FileAnalysis:
        """Elemez egy fájlt."""
        relative_path = str(file_path)

        # Mirror check
        test_exists, test_path = MirrorChecker.check_mirror(file_path)

        # Test count (ha van teszt fájl)
        test_count = 0
        if test_exists:
            test_analyzer = ASTAnalyzer(test_path)
            if test_analyzer.parse():
                test_count = test_analyzer.count_tests()

        # Forrás fájl analízis
        analyzer = ASTAnalyzer(file_path)
        if not analyzer.parse():
            # Parse hiba esetén alapértelmezett értékek
            config_status = "⚪ N/A"
            logger_status = "⚪ N/A"
        else:
            config_status = analyzer.check_config_type()
            logger_status = analyzer.check_logger_injection()

        # Előzetes FileAnalysis (overall_status nélkül)
        temp_analysis = FileAnalysis(
            path=file_path,
            relative_path=relative_path,
            test_file_exists=test_exists,
            test_file_path=test_path if test_exists else None,
            test_count=test_count,
            config_status=config_status,
            logger_status=logger_status,
            overall_status="🟡 WARNING",  # Placeholder
            notes="",
        )

        # Overall status kiszámítása
        overall_status = StatusCalculator.calculate(temp_analysis)
        notes = StatusCalculator.generate_notes(temp_analysis)

        # Végleges FileAnalysis
        return FileAnalysis(
            path=file_path,
            relative_path=relative_path,
            test_file_exists=test_exists,
            test_file_path=test_path if test_exists else None,
            test_count=test_count,
            config_status=config_status,
            logger_status=logger_status,
            overall_status=overall_status,
            notes=notes,
        )

    def generate(self) -> None:
        """Generálja a TASK_TREE.md fájlt."""
        print("🔍 Kódbázis szkennelése...")
        files = self.scan_codebase()
        print(f"✅ {len(files)} Python fájl találva")

        print("\n📊 Fájlok elemzése...")
        analyses: list[FileAnalysis] = []
        for i, file_path in enumerate(files, 1):
            print(f"  [{i}/{len(files)}] {file_path}")
            analysis = self.analyze_file(file_path)
            analyses.append(analysis)

        print("\n📝 TASK_TREE.md generálása...")
        generator = MarkdownGenerator(analyses)
        content = generator.generate()

        # Kimenet írása
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ TASK_TREE.md generálva: {self.output_file}")

        # Statisztika
        stats = generator.calculate_statistics()
        print("\n📈 Statisztika:")
        secure_pct = stats["secure"] / stats["total"] * 100
        warning_pct = stats["warning"] / stats["total"] * 100
        vuln_pct = stats["vulnerable"] / stats["total"] * 100
        print(f"  ✅ SECURE: {stats['secure']} ({secure_pct:.1f}%)")
        print(f"  🟡 WARNING: {stats['warning']} ({warning_pct:.1f}%)")
        print(f"  🔴 VULNERABLE: {stats['vulnerable']} ({vuln_pct:.1f}%)")


if __name__ == "__main__":
    generator = TaskTreeGenerator()
    generator.generate()
