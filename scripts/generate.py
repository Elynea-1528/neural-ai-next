"""TASK_TREE v5.0 Simplified Auditor - Hibrid Kódminőség Ellenőrző.

Egyszerűsített verzió: egyetlen TASK_TREE.md/html generálás (összes réteg).

Funkciók:
- AST: Config típus, Logger DI, Mirror Test ellenőrzés
- Pytest: Teszt eredmények (Pass/Fail/Warn)
- Coverage: Utasítás és elágazás lefedettség
- Ruff: Linter hibák száma
- Mypy: Típus hibák száma
- Pyright: Pylance hibák száma
"""

import ast
import html  # HTML escape-hez
import json
import os
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

# --- KONSTANSOK ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONDA_ENV_BIN = Path("/home/elynea/miniconda3/envs/neural-ai-next/bin")
PYTEST_BIN = CONDA_ENV_BIN / "pytest"
COVERAGE_BIN = CONDA_ENV_BIN / "coverage"
RUFF_BIN = CONDA_ENV_BIN / "ruff"
MYPY_BIN = CONDA_ENV_BIN / "mypy"

# Riport fájlok
REPORT_DIR = PROJECT_ROOT / "reports"
COVERAGE_FILE = REPORT_DIR / "coverage.json"
RUFF_FILE = REPORT_DIR / "ruff.json"
MYPY_FILE = REPORT_DIR / "mypy.json"

# Output fájlok
OUTPUT_MD = PROJECT_ROOT / "docs" / "development" / "TASK_TREE.md"
OUTPUT_HTML = PROJECT_ROOT / "docs" / "development" / "TASK_TREE.html"


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
    # Dinamikus metrikák
    coverage_stmt: float = 0.0
    coverage_branch: float = 0.0
    lint_errors: int = 0
    type_errors: int = 0
    pylance_errors: int = 0
    # Teszt eredmények
    test_passed: int = 0
    test_failed: int = 0
    test_errors: int = 0
    test_skipped: int = 0
    # Forráskód warnings (pytest warnings)
    source_warnings: int = 0
    # Dokumentáció
    has_documentation: bool = False


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
    def check_documentation(source_path: Path) -> bool:
        """Ellenőrzi, hogy van-e dokumentáció a fájlhoz a docs/ mappában.
        
        Példa: neural_ai/core/config/factory.py -> docs/components/neural_ai/core/config/factory.md
        """
        parts = source_path.parts

        # Csak neural_ai fájlokhoz keresünk dokumentációt
        if parts[0] != "neural_ai":
            return False

        # neural_ai/core/config/factory.py -> core/config/factory.py
        relative_parts = parts[1:]

        # Fájlnév .py -> .md
        file_name = relative_parts[-1].replace('.py', '.md')
        dir_parts = relative_parts[:-1]

        # docs/components/neural_ai/core/config/factory.md (TELJES TÜKÖR)
        doc_path = Path("docs/components/neural_ai") / Path(*dir_parts) / file_name

        return doc_path.exists()

    @staticmethod
    def get_test_path(source_path: Path) -> Path:
        """Kiszámítja a mirror test fájl útvonalát.

        Ha a test_X.py nem létezik, megpróbálja a test_X_integration.py-t is.
        Ha implementations/interfaces/exceptions mappában van, a szülő mappában is keres.
        """
        parts = source_path.parts

        # Ha már tests/ mappában van, nincs mirror test
        if parts[0] == "tests":
            return source_path  # Önmaga

        # Ha scripts/ vagy docs/ mappában van, nincs mirror test
        if parts[0] in ["scripts", "docs"]:
            return Path("tests") / source_path  # Nem létező útvonal

        # neural_ai/ esetén
        if parts[0] != "neural_ai":
            # Egyéb mappák esetén nincs mirror test
            return Path("tests") / source_path

        # Eltávolítjuk a "neural_ai/" prefix-et
        relative_parts = parts[1:]  # processors/dimensions/d01_price/processor.py

        # Szétválasztjuk könyvtár és fájl
        dir_parts = relative_parts[:-1]  # processors/dimensions/d01_price
        file_name = relative_parts[-1]  # processor.py

        # test_ prefix hozzáadása
        test_file_name = f"test_{file_name}"
        base_name = file_name.replace('.py', '')
        integration_file_name = f"test_{base_name}_integration.py"

        # 1. Elsődleges hely (Mirror Rule szerint - TELJES TÜKÖR)
        # neural_ai/collectors/jforex/factory.py -> tests/neural_ai/collectors/jforex/test_factory.py
        test_path = Path("tests") / Path("neural_ai") / Path(*dir_parts) / test_file_name

        # DEBUG: Útvonal ellenőrzés (csak UI fájloknál, hogy lássuk a hibát)
        if "ui" in str(source_path):
            print(f"DEBUG: Checking {source_path} -> {test_path} (Exists: {test_path.exists()})")

        if test_path.exists():
            return test_path

        # 1.5 Factory speciális kezelés: test_MODULE_factory.py
        # pl. neural_ai/core/config/factory.py -> tests/neural_ai/core/config/test_config_factory.py
        if base_name == "factory" and dir_parts:
            module_name = dir_parts[-1]  # pl. "config", "db", "logger"
            module_factory_name = f"test_{module_name}_factory.py"
            module_factory_path = Path("tests") / Path("neural_ai") / Path(*dir_parts) / module_factory_name
            if module_factory_path.exists():
                return module_factory_path

        # UI Services Fallback (ha a standard logika valamiért nem találja)
        if "ui" in dir_parts and "services" in dir_parts:
             ui_test_path = Path("tests/neural_ai/ui/services") / test_file_name
             if ui_test_path.exists():
                 print(f"DEBUG: FOUND via fallback: {ui_test_path}")
                 return ui_test_path

        # 2. Integration verzió (Mirror Rule szerint - TELJES TÜKÖR)
        integration_path = Path("tests") / Path("neural_ai") / Path(*dir_parts) / integration_file_name
        if integration_path.exists():
            return integration_path

        # 3. Ha implementations/interfaces/exceptions mappában van, szülő mappában is keres
        if dir_parts and dir_parts[-1] in ["implementations", "interfaces", "exceptions"]:
            parent_dir_parts = dir_parts[:-1]

            # 3a. Szülő mappában test_X.py (TELJES TÜKÖR)
            parent_test_path = Path("tests") / Path("neural_ai") / Path(*parent_dir_parts) / test_file_name
            if parent_test_path.exists():
                return parent_test_path

            # 3b. Szülő mappában test_X_integration.py (TELJES TÜKÖR)
            parent_integration_path = (
                Path("tests") / Path("neural_ai") / Path(*parent_dir_parts) / integration_file_name
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
        """Kiszámítja az overall státuszt.
        
        ✅ SECURE: Minden tökéletes (0 hiba, 0 warning, tesztek OK, dokumentáció OK)
        🟡 WARNING: Van javítanivaló, de nem kritikus
        🔴 VULNERABLE: Kritikus problémák (teszt hiány, TypedDict, Logger DI hiány, failed tesztek)
        """
        # Ellenőrizzük, hogy tests/ vagy scripts/ mappában vagyunk-e
        is_test_or_script = analysis.relative_path.startswith(("tests/", "scripts/"))

        # 🔴 VULNERABLE feltételek
        vulnerable_reasons = []

        # Neural_ai fájlokhoz: teszt pár kötelező
        if not is_test_or_script:
            if not analysis.test_file_exists or analysis.test_count == 0:
                vulnerable_reasons.append("teszt_hiany")
            if analysis.config_status == "🔴 TYPED_DICT":
                vulnerable_reasons.append("typeddict")
            if analysis.logger_status == "🔴 MISSING":
                vulnerable_reasons.append("logger_di")

        # Minden fájlhoz: failed/error tesztek
        if analysis.test_failed > 0 or analysis.test_errors > 0:
            vulnerable_reasons.append("failed_tests")

        if vulnerable_reasons:
            return "🔴 VULNERABLE"

        # ✅ SECURE feltételek (SZIGORÚ!)
        # Csak akkor SECURE, ha MINDEN rendben van
        problems = []

        # 1. Lint hibák
        if analysis.lint_errors > 0:
            problems.append("lint")

        # 2. Type hibák (Mypy)
        if analysis.type_errors > 0:
            problems.append("mypy")

        # 3. Pylance hibák
        if analysis.pylance_errors > 0:
            problems.append("pylance")

        # 4. Source warnings
        if analysis.source_warnings > 0:
            problems.append("warnings")

        # 5. Skipped tesztek
        if analysis.test_skipped > 0:
            problems.append("skipped")

        # Neural_ai fájlokhoz további feltételek
        if not is_test_or_script:
            # 6. Dokumentáció hiány
            if not analysis.has_documentation:
                problems.append("docs")

            # 7. Alacsony coverage (ha van coverage adat)
            if 0 < analysis.coverage_stmt < 80:
                problems.append("coverage")

        # Ha NINCS probléma, akkor SECURE
        if not problems:
            return "✅ SECURE"

        # 🟡 WARNING: van javítanivaló, de nem kritikus
        return "🟡 WARNING"

    @staticmethod
    def generate_notes(analysis: FileAnalysis) -> str:
        """Generál részletes teendő megjegyzéseket."""
        notes: list[str] = []

        # Ellenőrizzük, hogy tests/ vagy scripts/ mappában vagyunk-e
        is_test_or_script = analysis.relative_path.startswith(("tests/", "scripts/"))

        # 1. KRITIKUS problémák (VULNERABLE)
        if not is_test_or_script:
            if not analysis.test_file_exists or analysis.test_count == 0:
                notes.append("🔴 **Teszt írás KÖTELEZŐ!**")
            if analysis.config_status == "🔴 TYPED_DICT":
                notes.append("🔴 **Migráld Pydantic-ra!**")
            if analysis.logger_status == "🔴 MISSING":
                notes.append("🔴 **Logger DI hiányzik!**")

        if analysis.test_failed > 0 or analysis.test_errors > 0:
            notes.append(f"🔴 **Tesztek javítása: {analysis.test_failed} failed, {analysis.test_errors} error**")

        # 2. Dokumentáció hiány (neural_ai fájlokhoz)
        if not is_test_or_script and not analysis.has_documentation:
            notes.append("📝 Dokumentáció írása (docs/components/)")

        # 3. Linter hibák
        if analysis.lint_errors > 0:
            notes.append(f"🔧 Ruff: {analysis.lint_errors} hiba javítása")

        # 4. Type hibák
        if analysis.type_errors > 0:
            notes.append(f"🔬 Mypy: {analysis.type_errors} type hiba javítása")

        # 5. Pylance hibák
        if analysis.pylance_errors > 0:
            notes.append(f"🔎 Pylance: {analysis.pylance_errors} hiba javítása")

        # 6. Source warnings
        if analysis.source_warnings > 0:
            notes.append(f"⚠️ {analysis.source_warnings} warning javítása")

        # 7. Alacsony coverage (neural_ai fájlokhoz)
        if not is_test_or_script and 0 < analysis.coverage_stmt < 80:
            notes.append(f"📊 Coverage növelése: {analysis.coverage_stmt:.0f}% → 80%+")

        # 8. Skipped tesztek
        if analysis.test_skipped > 0:
            notes.append(f"⏭️ {analysis.test_skipped} skipped teszt aktiválása")

        return " | ".join(notes) if notes else "-"


class GeneratorBase:
    """Közös bázis osztály a Markdown és HTML generátorokhoz."""

    LAYER_MAPPING = {
        "root": ("0", "Root", "./"),
        "core": ("1", "Infrastructure", "neural_ai/core/"),
        "collectors": ("2", "Input", "neural_ai/collectors/"),
        "data": ("3", "Persistence", "neural_ai/data/"),
        "processors": ("4", "Domain", "neural_ai/processors/"),
        "ui": ("5", "Presentation", "neural_ai/ui/"),
        "tests": ("6", "Tests", "tests/"),
        "scripts": ("7", "Scripts", "scripts/"),
    }

    def __init__(self, analyses: list[FileAnalysis]) -> None:
        """Inicializálja a generátort.
        
        Args:
            analyses: Fájl analízisek listája
        """
        self.analyses = analyses
        self.grouped = self._group_by_layer()

    def _group_by_layer(self) -> dict[str, list[FileAnalysis]]:
        """Csoportosítja a fájlokat réteg szerint."""
        grouped: dict[str, list[FileAnalysis]] = {layer: [] for layer in self.LAYER_MAPPING.keys()}

        for analysis in self.analyses:
            parts = Path(analysis.relative_path).parts

            # Root fájlok (main.py, neural_ai/__init__.py)
            if len(parts) == 1 or (len(parts) == 2 and parts[0] == "neural_ai" and parts[1] == "__init__.py"):
                grouped["root"].append(analysis)
            # Első rész alapján csoportosítunk (neural_ai, tests, scripts)
            elif len(parts) > 0:
                first_part = parts[0]
                if first_part == "neural_ai" and len(parts) > 1:
                    # neural_ai esetén a második rész a layer (core, collectors, stb.)
                    if parts[1] in self.LAYER_MAPPING:
                        grouped[parts[1]].append(analysis)
                elif first_part in self.LAYER_MAPPING:
                    # tests, scripts esetén az első rész a layer
                    grouped[first_part].append(analysis)

        return grouped

    def calculate_statistics(self) -> dict[str, int]:
        """Statisztikákat számol az összes fájlhoz."""
        stats = {
            "total": len(self.analyses),
            "secure": 0,
            "warning": 0,
            "vulnerable": 0,
        }

        for analysis in self.analyses:
            if analysis.overall_status == "✅ SECURE":
                stats["secure"] += 1
            elif analysis.overall_status == "🟡 WARNING":
                stats["warning"] += 1
            elif analysis.overall_status == "🔴 VULNERABLE":
                stats["vulnerable"] += 1

        return stats


class MarkdownGenerator(GeneratorBase):
    """TASK_TREE.md generátor."""

    def _create_table(self, layer: str, files: list[FileAnalysis]) -> str:
            """Létrehoz egy Markdown táblázatot egy réteghez."""
            if not files:
                return ""

            num, name, path = self.LAYER_MAPPING[layer]

            table = f"\n## {num}. {name} Layer (`{path}`)\n\n"

            # Tests és Scripts layerekhez egyszerűsített táblázat
            if layer in ["tests", "scripts"]:
                table += "| Fájl | Státusz | Pass/Fail/Err/Skip | Lint/Mypy/Pylance | Src Warn | Teendők |\n"
                table += "|:-----|:--------|:-------------------|:------------------|:---------|:--------|\n"

                for file in sorted(files, key=lambda x: x.relative_path):
                    short_path = file.relative_path

                    # Teszt eredmények
                    if file.test_passed > 0 or file.test_failed > 0 or file.test_errors > 0 or file.test_skipped > 0:
                        test_results = f"**{file.test_passed}**/{file.test_failed}/{file.test_errors}/{file.test_skipped}"
                    else:
                        test_results = "-"

                    # Lint/Mypy/Pylance
                    lint_mypy_pylance = f"{file.lint_errors} / {file.type_errors} / {file.pylance_errors}"

                    # Source Warnings
                    src_warn = str(file.source_warnings) if file.source_warnings > 0 else "-"

                    table += f"| `{short_path}` | {file.overall_status} | {test_results} | {lint_mypy_pylance} | {src_warn} | {file.notes if file.notes else '-'} |\n"
            else:
                # Neural_ai layerekhez teljes táblázat + Dokumentálva oszlop
                table += "| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |\n"
                table += "|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|\n"

                for file in sorted(files, key=lambda x: x.relative_path):
                    # Root layer esetén ne távolítsuk el a neural_ai/ prefix-et
                    if layer == "root":
                        short_path = file.relative_path
                    else:
                        short_path = file.relative_path.replace("neural_ai/", "")

                    # Teszt pár
                    test_pair = "✅ FOUND" if file.test_file_exists else "❌ MISSING"

                    # Teszt eredmények
                    if file.test_file_exists and (file.test_passed > 0 or file.test_failed > 0 or file.test_errors > 0 or file.test_skipped > 0):
                        test_results = f"**{file.test_passed}**/{file.test_failed}/{file.test_errors}/{file.test_skipped}"
                    else:
                        test_results = "-"

                    # Coverage
                    if file.coverage_stmt > 0:
                        coverage = f"{file.coverage_stmt:.0f}% / {file.coverage_branch:.0f}%"
                    else:
                        coverage = "N/A"

                    # Lint/Mypy/Pylance
                    lint_mypy_pylance = f"{file.lint_errors} / {file.type_errors} / {file.pylance_errors}"

                    # Source Warnings (pytest warnings a forráskódban)
                    src_warn = str(file.source_warnings) if file.source_warnings > 0 else "-"

                    # Dokumentálva
                    doc_status = "✅" if file.has_documentation else "❌"

                    table += f"| `{short_path}` | {file.overall_status} | {test_pair} | {test_results} | {coverage} | {lint_mypy_pylance} | {src_warn} | {file.config_status} | {file.logger_status} | {doc_status} | {file.notes if file.notes else '-'} |\n"

            return table

    def generate(self) -> str:
        """Generálja a teljes Markdown tartalmat."""
        stats = self.calculate_statistics()
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

        content = f"""# 🌳 NEURAL AI NEXT - TASK TREE

**Generálva:** {now}
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
**Fájlok száma:** {stats['total']}

## 📊 Statisztika

- ✅ **SECURE:** {stats['secure']} ({stats['secure'] / stats['total'] * 100:.1f}%)
- 🟡 **WARNING:** {stats['warning']} ({stats['warning'] / stats['total'] * 100:.1f}%)
- 🔴 **VULNERABLE:** {stats['vulnerable']} ({stats['vulnerable'] / stats['total'] * 100:.1f}%)

---
"""

        # Összes réteg generálása
        for layer in self.LAYER_MAPPING.keys():
            if layer in self.grouped and self.grouped[layer]:
                content += self._create_table(layer, self.grouped[layer])

        return content


class HTMLGenerator(GeneratorBase):
    """HTML Dashboard generátor."""

    def calculate_statistics(self) -> dict[str, int]:
        """Statisztikákat számol az összes fájlhoz (HTML specifikus)."""
        stats = {
            "total": len(self.analyses),
            "secure": 0,
            "warning": 0,
            "critical": 0,
            "tested": 0,
        }

        for analysis in self.analyses:
            if analysis.overall_status == "✅ SECURE":
                stats["secure"] += 1
            elif analysis.overall_status == "🟡 WARNING":
                stats["warning"] += 1
            elif analysis.overall_status == "🔴 VULNERABLE":
                stats["critical"] += 1

            if analysis.test_file_exists:
                stats["tested"] += 1

        return stats

    def generate(self) -> str:
        """Generálja a teljes HTML tartalmat."""
        stats = self.calculate_statistics()
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

        secure_pct = (stats["secure"] / stats["total"] * 100) if stats["total"] > 0 else 0
        warning_pct = (stats["warning"] / stats["total"] * 100) if stats["total"] > 0 else 0
        critical_pct = (stats["critical"] / stats["total"] * 100) if stats["total"] > 0 else 0
        tested_pct = (stats["tested"] / stats["total"] * 100) if stats["total"] > 0 else 0

        page_title = "Neural AI Next - Task Tree Dashboard"
        header_title = "⚡ Neural AI Next - Task Tree Dashboard"

        html_output = f"""<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #e4e7eb;
            min-height: 100vh;
            padding: 0;
            overflow-x: auto;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            padding: 2rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }}
        
        .header-content {{
            max-width: 100%;
            padding: 0 2rem;
        }}
        
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.75rem;
            letter-spacing: -0.02em;
        }}
        
        .meta {{
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.6;
        }}
        
        .meta strong {{ color: #cbd5e1; }}
        
        .container {{
            max-width: 100%;
            padding: 2rem;
            overflow-x: auto;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 12px;
            padding: 1.75rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-color), transparent);
        }}
        
        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.4);
            border-color: rgba(148, 163, 184, 0.2);
        }}
        
        .stat-card.secure {{ --accent-color: #10b981; }}
        .stat-card.warning {{ --accent-color: #f59e0b; }}
        .stat-card.critical {{ --accent-color: #ef4444; }}
        .stat-card.tested {{ --accent-color: #3b82f6; }}
        
        .stat-header {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }}
        
        .stat-icon {{
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }}
        
        .stat-card.secure .stat-icon {{ background: rgba(16, 185, 129, 0.15); }}
        .stat-card.warning .stat-icon {{ background: rgba(245, 158, 11, 0.15); }}
        .stat-card.critical .stat-icon {{ background: rgba(239, 68, 68, 0.15); }}
        .stat-card.tested .stat-icon {{ background: rgba(59, 130, 246, 0.15); }}
        
        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 0.5rem;
        }}
        
        .stat-card.secure .stat-value {{ color: #10b981; }}
        .stat-card.warning .stat-value {{ color: #f59e0b; }}
        .stat-card.critical .stat-value {{ color: #ef4444; }}
        .stat-card.tested .stat-value {{ color: #3b82f6; }}
        
        .stat-label {{
            color: #94a3b8;
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .stat-percent {{
            color: #cbd5e1;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }}
        
        .search-box {{
            width: 100%;
            padding: 1rem 1.25rem;
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 12px;
            color: #e4e7eb;
            font-size: 1rem;
            margin-bottom: 2rem;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #60a5fa;
            background: rgba(30, 41, 59, 0.8);
            box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
        }}
        
        .search-box::placeholder {{ color: #64748b; }}
        
        .layer {{
            margin-bottom: 2.5rem;
            border-radius: 12px;
            overflow-x: auto;
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(148, 163, 184, 0.1);
        }}
        
        .layer-title {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 1.25rem 1.5rem;
            font-size: 1.125rem;
            font-weight: 600;
            color: #60a5fa;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            table-layout: auto;
            min-width: 1200px;
        }}
        
        th {{
            background: rgba(15, 23, 42, 0.6);
            padding: 1rem 1.25rem;
            text-align: left;
            font-weight: 600;
            color: #94a3b8;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            white-space: nowrap;
        }}
        
        /* Rugalmas oszlopszélességek */
        th:nth-child(1) {{ min-width: 250px; max-width: 400px; }} /* Fájl */
        th:nth-child(2) {{ min-width: 100px; width: 120px; }} /* Státusz */
        th:nth-child(3) {{ min-width: 80px; width: 100px; }} /* Teszt Pár / Pass-Fail */
        th:nth-child(4) {{ min-width: 120px; width: 150px; }} /* Pass/Fail/Err/Skip */
        th:nth-child(5) {{ min-width: 120px; width: 140px; }} /* Coverage */
        th:nth-child(6) {{ min-width: 120px; width: 150px; }} /* Lint/Mypy/Pylance */
        th:nth-child(7) {{ min-width: 60px; width: 80px; }} /* Src Warn */
        th:nth-child(8) {{ min-width: 60px; width: 80px; }} /* Config */
        th:nth-child(9) {{ min-width: 60px; width: 80px; }} /* Logger */
        th:nth-child(10) {{ min-width: 60px; width: 100px; }} /* Dokumentálva */
        th:nth-child(11) {{ min-width: 150px; }} /* Teendők */
        
        td {{
            padding: 1rem 1.25rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.05);
            font-size: 0.9rem;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
        
        /* Rugalmas oszlopszélességek */
        td:nth-child(1) {{ min-width: 250px; max-width: 400px; }} /* Fájl */
        td:nth-child(2) {{ min-width: 100px; width: 120px; }} /* Státusz */
        td:nth-child(3) {{ min-width: 80px; width: 100px; }} /* Teszt Pár / Pass-Fail */
        td:nth-child(4) {{ min-width: 120px; width: 150px; }} /* Pass/Fail/Err/Skip */
        td:nth-child(5) {{ min-width: 120px; width: 140px; }} /* Coverage */
        td:nth-child(6) {{ min-width: 120px; width: 150px; }} /* Lint/Mypy/Pylance */
        td:nth-child(7) {{ min-width: 60px; width: 80px; }} /* Src Warn */
        td:nth-child(8) {{ min-width: 60px; width: 80px; }} /* Config */
        td:nth-child(9) {{ min-width: 60px; width: 80px; }} /* Logger */
        td:nth-child(10) {{ min-width: 60px; width: 100px; }} /* Dokumentálva */
        td:nth-child(11) {{ min-width: 150px; }} /* Teendők */
        
        tr:hover td {{
            background: rgba(30, 41, 59, 0.4);
        }}
        
        .file-path {{
            font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Courier New', monospace;
            color: #93c5fd;
            font-size: 0.875rem;
        }}
        
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.375rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }}
        
        .status-secure {{
            background: rgba(16, 185, 129, 0.15);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}
        
        .status-warning {{
            background: rgba(245, 158, 11, 0.15);
            color: #f59e0b;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }}
        
        .status-critical {{
            background: rgba(239, 68, 68, 0.15);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}
        
        .icon {{ font-style: normal; }}
        .test-found {{ color: #10b981; font-weight: 600; }}
        .test-missing {{ color: #ef4444; font-weight: 600; }}
        .test-results {{ font-family: 'SF Mono', monospace; font-size: 0.875rem; }}
        .test-pass {{ color: #10b981; font-weight: 600; }}
        .test-fail {{ color: #ef4444; font-weight: 600; }}
        .test-error {{ color: #f87171; font-weight: 600; }}
        .test-skip {{ color: #f59e0b; font-weight: 600; }}
        .test-warn {{ color: #f59e0b; font-weight: 600; }}
        .coverage {{ font-family: 'SF Mono', monospace; font-size: 0.875rem; }}
        .cov-low {{ color: #ef4444; font-weight: 600; }}
        .cov-good {{ color: #10b981; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>{header_title}</h1>
            <div class="meta">
                <strong>Generálva:</strong> {now} &nbsp;|&nbsp;
                <strong>Módszer:</strong> Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance) &nbsp;|&nbsp;
                <strong>Fájlok:</strong> {stats['total']}
            </div>
        </div>
    </div>

    <div class="container">
        <div class="stats">
            <div class="stat-card secure">
                <div class="stat-header">
                    <div class="stat-icon">✓</div>
                </div>
                <div class="stat-value">{stats['secure']}</div>
                <div class="stat-label">Secure</div>
                <div class="stat-percent">{secure_pct:.1f}% a teljes kódbázisból</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-header">
                    <div class="stat-icon">⚠</div>
                </div>
                <div class="stat-value">{stats['warning']}</div>
                <div class="stat-label">Warning</div>
                <div class="stat-percent">{warning_pct:.1f}% javítást igényel</div>
            </div>
            <div class="stat-card critical">
                <div class="stat-header">
                    <div class="stat-icon">✕</div>
                </div>
                <div class="stat-value">{stats['critical']}</div>
                <div class="stat-label">Critical</div>
                <div class="stat-percent">{critical_pct:.1f}% azonnali beavatkozás</div>
            </div>
            <div class="stat-card tested">
                <div class="stat-header">
                    <div class="stat-icon">◉</div>
                </div>
                <div class="stat-value">{stats['tested']}/{stats['total']}</div>
                <div class="stat-label">Tesztelt</div>
                <div class="stat-percent">{tested_pct:.1f}% teszt lefedettség</div>
            </div>
        </div>

        <input type="text" class="search-box" id="searchBox" placeholder="🔍 Keresés fájl név alapján..." onkeyup="filterTable()">
"""

        # Összes réteg generálása
        for layer in self.LAYER_MAPPING.keys():
            if layer in self.grouped and self.grouped[layer]:
                html_output += self._create_html_table(layer, self.grouped[layer])

        html_output += """
    </div>
    <script>
        function filterTable() {{
            const input = document.getElementById('searchBox');
            const filter = input.value.toLowerCase();
            const tables = document.querySelectorAll('table');
            
            tables.forEach(table => {{
                const rows = table.getElementsByTagName('tr');
                for (let i = 1; i < rows.length; i++) {{
                    const td = rows[i].getElementsByTagName('td')[0];
                    if (td) {{
                        const txtValue = td.textContent || td.innerText;
                        rows[i].style.display = txtValue.toLowerCase().indexOf(filter) > -1 ? '' : 'none';
                    }}
                }}
            }});
        }}
    </script>
</body>
</html>"""
        return html_output

    def _create_html_table(self, layer: str, files: list[FileAnalysis]) -> str:
            """Létrehoz egy HTML táblázatot egy réteghez."""
            if not files:
                return ""

            num, name, path = self.LAYER_MAPPING[layer]

            # Layer ikonok
            layer_icons = {
                "root": "🏠",
                "core": "⚙️",
                "collectors": "📡",
                "data": "💾",
                "processors": "🧠",
                "ui": "🎨",
                "tests": "🧪",
                "scripts": "📜",
            }
            icon = layer_icons.get(layer, "📦")

            html_output = f"""
            <div class="layer">
                <div class="layer-title">{icon} {num}. {name} Layer <span style="opacity: 0.6; font-size: 0.9rem;">({path})</span></div>
                <table>
                    <thead>
                        <tr>"""

            # Tests és Scripts layerekhez egyszerűsített fejléc
            if layer in ["tests", "scripts"]:
                html_output += """
                            <th>Fájl</th>
                            <th>Státusz</th>
                            <th>Pass/Fail/Err/Skip</th>
                            <th>Lint/Mypy/Pylance</th>
                            <th>Src Warn</th>
                            <th>Teendők</th>"""
            else:
                # Neural_ai layerekhez teljes fejléc + Dokumentálva
                html_output += """
                            <th>Modul / Fájl</th>
                            <th>Státusz</th>
                            <th>Teszt Pár</th>
                            <th>Pass/Fail/Err/Skip</th>
                            <th>Coverage (Stmt/Brch)</th>
                            <th>Lint/Mypy/Pylance</th>
                            <th>Src Warn</th>
                            <th>Config</th>
                            <th>Logger</th>
                            <th>Dokumentálva</th>
                            <th>Teendők</th>"""

            html_output += """
                        </tr>
                    </thead>
                    <tbody>
    """

            for file in sorted(files, key=lambda x: x.relative_path):
                # Root layer esetén ne távolítsuk el a neural_ai/ prefix-et
                if layer == "root":
                    short_path = file.relative_path
                elif layer not in ["tests", "scripts"]:
                    short_path = file.relative_path.replace("neural_ai/", "")
                else:
                    short_path = file.relative_path
                # HTML escape a biztonság érdekében
                short_path_escaped = html.escape(short_path)

                # Státusz badge
                if file.overall_status == "✅ SECURE":
                    status_badge = '<span class="status-badge status-secure"><span class="icon">✓</span> SECURE</span>'
                elif file.overall_status == "🟡 WARNING":
                    status_badge = '<span class="status-badge status-warning"><span class="icon">⚠</span> WARNING</span>'
                else:
                    status_badge = '<span class="status-badge status-critical"><span class="icon">✕</span> CRITICAL</span>'

                # Teszt eredmények
                if file.test_passed > 0 or file.test_failed > 0 or file.test_errors > 0 or file.test_skipped > 0:
                    pass_str = f'<span class="test-pass">{file.test_passed}</span>' if file.test_passed > 0 else '0'
                    fail_str = f'<span class="test-fail">{file.test_failed}</span>' if file.test_failed > 0 else '0'
                    error_str = f'<span class="test-error">{file.test_errors}</span>' if file.test_errors > 0 else '0'
                    skip_str = f'<span class="test-skip">{file.test_skipped}</span>' if file.test_skipped > 0 else '0'
                    test_results = f'{pass_str}/{fail_str}/{error_str}/{skip_str}'
                else:
                    test_results = '<span style="opacity: 0.4;">-</span>'

                # Lint/Mypy/Pylance
                lint_str = f'<span class="test-fail">{file.lint_errors}</span>' if file.lint_errors > 0 else '<span style="opacity: 0.6;">0</span>'
                mypy_str = f'<span class="test-fail">{file.type_errors}</span>' if file.type_errors > 0 else '<span style="opacity: 0.6;">0</span>'
                pylance_str = f'<span class="test-fail">{file.pylance_errors}</span>' if file.pylance_errors > 0 else '<span style="opacity: 0.6;">0</span>'
                lint_type = f'{lint_str} / {mypy_str} / {pylance_str}'

                # Source Warnings
                src_warn = f'<span class="test-warn">{file.source_warnings}</span>' if file.source_warnings > 0 else '<span style="opacity: 0.4;">-</span>'

                # Teendők (HTML escape)
                notes_display = html.escape(file.notes) if file.notes and file.notes != "-" else '<span style="opacity: 0.4;">-</span>'

                # Tests és Scripts layerekhez egyszerűsített sor
                if layer in ["tests", "scripts"]:
                    html_output += f"""
                        <tr>
                            <td class="file-path">{short_path_escaped}</td>
                            <td>{status_badge}</td>
                            <td class="test-results">{test_results}</td>
                            <td>{lint_type}</td>
                            <td>{src_warn}</td>
                            <td>{notes_display}</td>
                        </tr>
    """
                else:
                    # Neural_ai layerekhez teljes sor
                    # Teszt pár
                    test_pair = '<span class="test-found">✓ FOUND</span>' if file.test_file_exists else '<span class="test-missing">✕ MISSING</span>'

                    # Coverage
                    if file.coverage_stmt > 0:
                        cov_class = 'cov-good' if file.coverage_stmt >= 80 else 'cov-low'
                        coverage = f'<span class="{cov_class}">{file.coverage_stmt:.0f}%</span> / {file.coverage_branch:.0f}%'
                    else:
                        coverage = '<span style="opacity: 0.4;">N/A</span>'

                    # Config és Logger státusz (HTML escape)
                    config_display = html.escape(file.config_status.replace("✅", "✓").replace("🔴", "✕").replace("⚪", "○"))
                    logger_display = html.escape(file.logger_status.replace("✅", "✓").replace("⚠️", "⚠").replace("🔴", "✕").replace("⚪", "○"))

                    # Dokumentálva
                    doc_display = '<span class="test-found">✓</span>' if file.has_documentation else '<span class="test-missing">✕</span>'

                    html_output += f"""
                        <tr>
                            <td class="file-path">{short_path_escaped}</td>
                            <td>{status_badge}</td>
                            <td>{test_pair}</td>
                            <td class="test-results">{test_results}</td>
                            <td class="coverage">{coverage}</td>
                            <td>{lint_type}</td>
                            <td>{src_warn}</td>
                            <td>{config_display}</td>
                            <td>{logger_display}</td>
                            <td>{doc_display}</td>
                            <td>{notes_display}</td>
                        </tr>
    """

            html_output += """
                    </tbody>
                </table>
            </div>
    """
            return html_output


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
        self.ignored_files = set()  # Üres - __init__.py fájlokat is szkenneljük
        # Szkennelendő mappák
        self.scan_dirs = [
            Path("neural_ai"),
            Path("tests"),
            Path("scripts"),
            Path("docs"),
        ]
        self.coverage_data = {}
        self.ruff_data = []
        self.mypy_data = []
        self.pylance_data = []
        self.pytest_data = {}  # test_file_path -> {passed, failed, errors, warnings}
        self.source_warnings = {}  # source_file_path -> warning_count (pytest warnings)

    def run_dynamic_tools(self) -> None:
        """Futtatja a dinamikus ellenőrző eszközöket."""
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT)

        print("\n🚀 Dinamikus eszközök futtatása...")

        # 1. Coverage + Pytest + JSON Report
        print("  📊 Coverage + Pytest...")
        try:
            # Először pytest JSON reporttal (collection errorok ellenére folytatjuk)
            cmd_pytest = [
                str(PYTEST_BIN),
                "-q", "--tb=no",
                "--continue-on-collection-errors",
                "--json-report", f"--json-report-file={REPORT_DIR}/pytest_report.json",
                "tests/"
            ]
            subprocess.run(cmd_pytest, check=False, env=env, capture_output=True)

            # Majd coverage futtatás
            cmd_cov = [
                str(COVERAGE_BIN), "run", "--branch", "--source=neural_ai",
                "-m", "pytest", "-q", "--tb=no", "tests/"
            ]
            subprocess.run(cmd_cov, check=False, env=env, capture_output=True)

            cmd_json = [str(COVERAGE_BIN), "json", "-o", str(COVERAGE_FILE)]
            subprocess.run(cmd_json, check=False, env=env)

            if COVERAGE_FILE.exists():
                with open(COVERAGE_FILE) as f:
                    cov_json = json.load(f)
                    self.coverage_data = cov_json.get("files", {})
        except Exception as e:
            print(f"    ⚠️ Hiba: {e}")

        # 2. Ruff (neural_ai + tests + scripts)
        print("  🔍 Ruff linter...")
        try:
            with open(RUFF_FILE, "w") as f:
                cmd = [str(RUFF_BIN), "check", "neural_ai", "tests", "scripts", "--output-format=json"]
                subprocess.run(cmd, stdout=f, check=False, env=env)

            if RUFF_FILE.exists():
                with open(RUFF_FILE) as f:
                    self.ruff_data = json.load(f)
        except Exception as e:
            print(f"    ⚠️ Hiba: {e}")

        # 3. Mypy (neural_ai + tests + scripts)
        print("  🔬 Mypy type checker...")
        try:
            cmd = [str(MYPY_BIN), "neural_ai", "tests", "scripts", "--no-error-summary"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False, env=env)

            mypy_errors = []
            for line in result.stdout.strip().split("\n"):
                if line.strip() and ": error:" in line:
                    parts = line.split(":", 3)
                    if len(parts) >= 4:
                        mypy_errors.append({
                            "file": parts[0].strip(),
                            "line": parts[1].strip(),
                            "severity": "error",
                            "message": parts[3].strip()
                        })

            with open(MYPY_FILE, "w") as f:
                json.dump(mypy_errors, f, indent=2)

            self.mypy_data = mypy_errors
        except Exception as e:
            print(f"    ⚠️ Hiba: {e}")

        # 4. Pylance (Pyright) - Problems fül hibák (neural_ai + tests + scripts)
        print("  🔎 Pylance/Pyright type checker...")
        pylance_file = REPORT_DIR / "pylance.json"
        try:
            # Pyright futtatása JSON outputtal (neural_ai + tests + scripts)
            cmd = ["pyright", "neural_ai", "tests", "scripts", "--outputjson"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False, env=env, timeout=60)

            if result.stdout.strip():
                pylance_json = json.loads(result.stdout)

                # Hibák kinyerése
                pylance_errors = []
                for diagnostic in pylance_json.get("generalDiagnostics", []):
                    file_path = diagnostic.get("file", "")
                    severity = diagnostic.get("severity", "")

                    # Csak error és warning szintű hibák
                    if severity in ["error", "warning"]:
                        # Abszolút útvonal -> relatív útvonal konverzió
                        # Pyright abszolút útvonalat ad: /home/.../neural-ai-next/neural_ai/...
                        # Nekünk relatív kell: neural_ai/...
                        if file_path.startswith(str(PROJECT_ROOT)):
                            file_path = file_path[len(str(PROJECT_ROOT)) + 1:]  # +1 a / miatt

                        pylance_errors.append({
                            "file": file_path,
                            "line": diagnostic.get("range", {}).get("start", {}).get("line", 0) + 1,
                            "severity": severity,
                            "message": diagnostic.get("message", "")
                        })

                with open(pylance_file, "w") as f:
                    json.dump(pylance_errors, f, indent=2)

                self.pylance_data = pylance_errors
                print(f"    ✅ {len(pylance_errors)} Pylance hiba/figyelmeztetés találva (strict mode)")
            else:
                self.pylance_data = []
        except subprocess.TimeoutExpired:
            print("    ⚠️ Pyright timeout (60s), kihagyva")
            self.pylance_data = []
        except FileNotFoundError:
            print("    ⚠️ Pyright nincs telepítve, Pylance hibák nem elérhetők")
            self.pylance_data = []
        except Exception as e:
            print(f"    ⚠️ Hiba: {e}")
            self.pylance_data = []

        # 5. Pytest Report feldolgozása
        print("  📋 Pytest eredmények feldolgozása...")
        pytest_report_file = REPORT_DIR / "pytest_report.json"
        if pytest_report_file.exists():
            try:
                with open(pytest_report_file) as f:
                    pytest_json = json.load(f)

                # Tesztek csoportosítása fájlonként
                for test in pytest_json.get("tests", []):
                    nodeid = test.get("nodeid", "")
                    outcome = test.get("outcome", "")

                    # nodeid formátum: tests/core/config/test_config_factory.py::TestClass::test_method
                    if "::" in nodeid:
                        test_file = nodeid.split("::")[0]

                        if test_file not in self.pytest_data:
                            self.pytest_data[test_file] = {
                                "passed": 0,
                                "failed": 0,
                                "errors": 0,
                                "skipped": 0
                            }

                        if outcome == "passed":
                            self.pytest_data[test_file]["passed"] += 1
                        elif outcome == "failed":
                            self.pytest_data[test_file]["failed"] += 1
                        elif outcome == "error":
                            self.pytest_data[test_file]["errors"] += 1
                        elif outcome == "skipped":
                            self.pytest_data[test_file]["skipped"] += 1

                # Warnings feldolgozása (TOP LEVEL, forráskód fájlokhoz)
                # A warnings-ok a forráskód fájlokban vannak, nem a teszt fájlokban
                for warning in pytest_json.get("warnings", []):
                    filename = warning.get("filename", "")
                    # Ha a neural-ai-next projektben van
                    if "neural-ai-next" in filename:
                        rel_path = filename.split("neural-ai-next/")[-1]
                        # Csak a neural_ai/ mappában lévő fájlokat számoljuk
                        if rel_path.startswith("neural_ai/"):
                            if rel_path not in self.source_warnings:
                                self.source_warnings[rel_path] = 0
                            self.source_warnings[rel_path] += 1

            except Exception as e:
                print(f"    ⚠️ Hiba a pytest report feldolgozásakor: {e}")

    def get_dynamic_metrics(self, file_path: Path) -> dict:
        """Visszaadja a dinamikus metrikákat egy fájlhoz."""
        rel_path = str(file_path)
        metrics = {
            "coverage_stmt": 0.0,
            "coverage_branch": 0.0,
            "lint_errors": 0,
            "type_errors": 0,
            "pylance_errors": 0,
            "test_passed": 0,
            "test_failed": 0,
            "test_errors": 0,
            "test_skipped": 0,
            "source_warnings": 0,  # Pytest warnings a forráskódban
        }

        # Coverage
        if rel_path in self.coverage_data:
            file_cov = self.coverage_data[rel_path]
            summary = file_cov.get("summary", {})
            metrics["coverage_stmt"] = summary.get("percent_covered", 0.0)

            covered_branches = summary.get("covered_branches", 0)
            num_branches = summary.get("num_branches", 0)
            if num_branches > 0:
                metrics["coverage_branch"] = covered_branches / num_branches * 100
            else:
                metrics["coverage_branch"] = 100.0 if metrics["coverage_stmt"] > 0 else 0.0

        # Ruff
        if isinstance(self.ruff_data, list):
            metrics["lint_errors"] = sum(
                1 for err in self.ruff_data if err.get("filename") == rel_path
            )

        # Mypy
        if isinstance(self.mypy_data, list):
            metrics["type_errors"] = sum(
                1 for err in self.mypy_data
                if err.get("file") == rel_path and err.get("severity") == "error"
            )

        # Pylance
        if isinstance(self.pylance_data, list):
            metrics["pylance_errors"] = sum(
                1 for err in self.pylance_data
                if err.get("file") == rel_path and err.get("severity") in ["error", "warning"]
            )

        # Source Warnings (pytest warnings a forráskódban)
        if rel_path in self.source_warnings:
            metrics["source_warnings"] = self.source_warnings[rel_path]

        # Pytest eredmények
        # Ha tests/ vagy scripts/ mappában vagyunk, akkor önmaga a teszt fájl
        if rel_path.startswith(("tests/", "scripts/")):
            # Önmaga a teszt fájl
            if rel_path in self.pytest_data:
                metrics["test_passed"] = self.pytest_data[rel_path]["passed"]
                metrics["test_failed"] = self.pytest_data[rel_path]["failed"]
                metrics["test_errors"] = self.pytest_data[rel_path]["errors"]
                metrics["test_skipped"] = self.pytest_data[rel_path]["skipped"]
        else:
            # Neural_ai fájlokhoz: megkeressük a mirror test fájlt
            test_path = MirrorChecker.get_test_path(file_path)
            if test_path and test_path.exists():
                test_rel = str(test_path)
                if test_rel in self.pytest_data:
                    metrics["test_passed"] = self.pytest_data[test_rel]["passed"]
                    metrics["test_failed"] = self.pytest_data[test_rel]["failed"]
                    metrics["test_errors"] = self.pytest_data[test_rel]["errors"]
                    metrics["test_skipped"] = self.pytest_data[test_rel]["skipped"]

        return metrics

    def scan_codebase(self) -> list[Path]:
        """Rekurzívan bejárja a neural_ai/, tests/, scripts/ mappákat + projekt gyökér fájlok."""
        python_files: list[Path] = []

        # 1. Projekt gyökér fájlok (main.py, neural_ai/__init__.py)
        root_files = [
            Path("main.py"),
            Path("neural_ai/__init__.py"),
        ]

        for root_file in root_files:
            if root_file.exists():
                python_files.append(root_file)

        # 2. Mappák szkennelése (neural_ai, tests, scripts)
        scan_dirs = [Path("neural_ai"), Path("tests"), Path("scripts")]

        for scan_dir in scan_dirs:
            if not scan_dir.exists():
                continue

            for root, dirs, files in os.walk(scan_dir):
                # Kihagyott könyvtárak szűrése
                dirs[:] = [d for d in dirs if d not in self.ignored_dirs]

                for file in files:
                    if file.endswith(".py") and file not in self.ignored_files:
                        file_path = Path(root) / file
                        # Kihagyjuk a neural_ai/__init__.py-t, mert már hozzáadtuk a root_files-ban
                        if file_path != Path("neural_ai/__init__.py"):
                            python_files.append(file_path)

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

        # Dinamikus metrikák gyűjtése (ELŐSZÖR!)
        dyn_metrics = self.get_dynamic_metrics(file_path)

        # Dokumentáció ellenőrzése
        has_documentation = MirrorChecker.check_documentation(file_path)

        # Teljes FileAnalysis (dinamikus metrikákkal)
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
            coverage_stmt=dyn_metrics["coverage_stmt"],
            coverage_branch=dyn_metrics["coverage_branch"],
            lint_errors=dyn_metrics["lint_errors"],
            type_errors=dyn_metrics["type_errors"],
            pylance_errors=dyn_metrics["pylance_errors"],
            test_passed=dyn_metrics["test_passed"],
            test_failed=dyn_metrics["test_failed"],
            test_errors=dyn_metrics["test_errors"],
            test_skipped=dyn_metrics["test_skipped"],
            source_warnings=dyn_metrics["source_warnings"],
            has_documentation=has_documentation,
        )

        # Overall status és notes kiszámítása (MOST már van dinamikus metrika!)
        overall_status = StatusCalculator.calculate(temp_analysis)
        notes = StatusCalculator.generate_notes(temp_analysis)

        # Végleges FileAnalysis (frissített státusszal és notes-szal)
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
            coverage_stmt=dyn_metrics["coverage_stmt"],
            coverage_branch=dyn_metrics["coverage_branch"],
            lint_errors=dyn_metrics["lint_errors"],
            type_errors=dyn_metrics["type_errors"],
            pylance_errors=dyn_metrics["pylance_errors"],
            test_passed=dyn_metrics["test_passed"],
            test_failed=dyn_metrics["test_failed"],
            test_errors=dyn_metrics["test_errors"],
            test_skipped=dyn_metrics["test_skipped"],
            source_warnings=dyn_metrics["source_warnings"],
            has_documentation=has_documentation,
        )

    def generate(self) -> None:
        """Generálja a TASK_TREE.md és TASK_TREE.html fájlokat."""
        # 1. Dinamikus eszközök futtatása
        self.run_dynamic_tools()

        print("\n🔍 Kódbázis szkennelése...")
        files = self.scan_codebase()
        print(f"✅ {len(files)} Python fájl találva")

        print("\n📊 Fájlok elemzése...")
        analyses: list[FileAnalysis] = []
        for i, file_path in enumerate(files, 1):
            print(f"  [{i}/{len(files)}] {file_path}")
            analysis = self.analyze_file(file_path)
            analyses.append(analysis)

        # 2. Markdown generálás (összes réteg)
        print("\n📝 TASK_TREE.md generálása (összes réteg)...")
        md_generator = MarkdownGenerator(analyses)
        md_content = md_generator.generate()

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"✅ TASK_TREE.md generálva: {self.output_file}")

        # 3. HTML generálás (összes réteg)
        print("\n🌐 TASK_TREE.html generálása (összes réteg)...")
        html_generator = HTMLGenerator(analyses)
        html_content = html_generator.generate()

        with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ TASK_TREE.html generálva: {OUTPUT_HTML}")

        # Statisztika
        stats = md_generator.calculate_statistics()
        print("\n📈 Statisztika (összes fájl):")
        secure_pct = stats["secure"] / stats["total"] * 100
        warning_pct = stats["warning"] / stats["total"] * 100
        vuln_pct = stats["vulnerable"] / stats["total"] * 100
        print(f"  ✅ SECURE: {stats['secure']} ({secure_pct:.1f}%)")
        print(f"  🟡 WARNING: {stats['warning']} ({warning_pct:.1f}%)")
        print(f"  🔴 VULNERABLE: {stats['vulnerable']} ({vuln_pct:.1f}%)")
        print(f"  🔴 VULNERABLE: {stats['vulnerable']} ({vuln_pct:.1f}%)")



if __name__ == "__main__":
    generator = TaskTreeGenerator()
    generator.generate()
