#!/usr/bin/env python3
"""TASK_TREE.md/html Generátor V2 - Moduláris Újraírás.

Architektúra: Strategy + Command Pattern
Futtatási Módok:
  --full      : Teljes analízis (QA + Coverage + Static) ~11-15 perc
  --quick     : Gyors mód (csak AST + cache) ~30sec
  --qa        : Csak QA eszközök (Ruff, Mypy, Pyright) ~2 perc
  --coverage  : Csak Coverage + Pytest ~11-15 perc
  --test      : Csak Pytest (QA/Coverage skip) ~5-8 perc

Használat:
  python scripts/generate_v2.py --full
  python scripts/generate_v2.py --quick
  python scripts/generate_v2.py --full --force-refresh
"""

import argparse
import ast
import hashlib
import html
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, Protocol

# ============================================================================
# 1. MODELL RÉTEG (Data Models)
# ============================================================================


@dataclass
class FileMetrics:
    """Egyetlen fájl metrikái."""

    path: Path
    relative_path: str
    config_status: Literal["✅ OK", "🔴 TYPED_DICT", "⚪ N/A"]
    logger_status: Literal["✅ OK", "⚠️ UNUSED", "🔴 MISSING", "⚪ N/A"]
    test_file_exists: bool
    coverage_stmt: float = -1.0
    coverage_branch: float = -1.0
    lint_errors: int = 0
    type_errors: int = 0
    test_passed: int = 0
    test_failed: int = 0

    def get_status_emoji(self) -> str:
        """Színkód kalkulálás (🔴/🟡/🟢/✅)."""
        if self.coverage_stmt < 0:
            if self.lint_errors > 0 or self.type_errors > 0:
                return "🔴"
            return "🟡"

        if self.coverage_stmt >= 100.0 and self.coverage_branch >= 100.0:
            if self.lint_errors == 0 and self.type_errors == 0:
                return "✅"
        if self.coverage_stmt >= 80.0:
            return "🟢"
        if self.coverage_stmt >= 50.0:
            return "🟡"
        return "🔴"


@dataclass
class ProjectReport:
    """Teljes projekt jelentés."""

    files: list[FileMetrics]
    generated_at: datetime
    mode: str
    summary: dict[str, Any] = field(default_factory=dict)  # pyright: ignore[reportUnknownVariableType]


# ============================================================================
# 2. CACHE MANAGER
# ============================================================================


class CacheManager:
    """Fájl hash alapú cache kezelés."""

    def __init__(self, cache_file: Path = Path(".cache/generate_cache.json")):
        """Cache manager inicializálása."""
        self.cache_file = cache_file
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache: dict[str, Any] = self._load_cache()

    def _load_cache(self) -> dict[str, Any]:
        if self.cache_file.exists():
            try:
                content: dict[str, Any] = json.loads(self.cache_file.read_text())
                return content
            except Exception:
                return {}
        return {}

    def save_cache(self) -> None:
        """Cache mentése fájlba."""
        self.cache_file.write_text(json.dumps(self.cache, indent=2))

    def get_file_hash(self, path: Path) -> str:
        """Fájl hash számítása."""
        try:
            content = path.read_bytes()
            return hashlib.sha256(content).hexdigest()
        except Exception:
            return ""

    def is_cached(self, path: Path) -> bool:
        """Ellenőrzi, hogy a fájl cache-ben van-e."""
        file_hash = self.get_file_hash(path)
        cached_entry = self.cache.get(str(path), {})
        cached_hash: str = cached_entry.get("hash", "") if isinstance(cached_entry, dict) else ""  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
        return file_hash == cached_hash  # pyright: ignore[reportUnknownVariableType]

    def update_cache(self, path: Path, metrics: FileMetrics) -> None:
        """Cache frissítése új metrikákkal."""
        file_hash = self.get_file_hash(path)
        self.cache[str(path)] = {
            "hash": file_hash,
            "metrics": {
                "config_status": metrics.config_status,
                "logger_status": metrics.logger_status,
                "test_file_exists": metrics.test_file_exists,
            },
        }

    def get_cached_metrics(self, path: Path) -> dict[str, Any] | None:
        """Cache-ből metrikák lekérdezése."""
        if self.is_cached(path):
            entry = self.cache.get(str(path), {})
            if isinstance(entry, dict):
                metrics = entry.get("metrics")  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                if isinstance(metrics, dict):
                    return metrics  # pyright: ignore[reportUnknownVariableType]
        return None


# ============================================================================
# 3. SZOLGÁLTATÁS RÉTEG (Strategy Pattern)
# ============================================================================


class StaticAnalyzer:
    """AST-based statikus analízis."""

    def __init__(self, cache_manager: CacheManager, root_dir: Path):
        """StaticAnalyzer inicializálása."""
        self.cache_manager = cache_manager
        self.root_dir = root_dir
        self.tests_dir = root_dir / "tests"

    def analyze_file(self, path: Path) -> FileMetrics:
        """Egyetlen fájl elemzése."""
        rel_path = str(path.relative_to(self.root_dir))

        cached = self.cache_manager.get_cached_metrics(path)
        if cached:
            return FileMetrics(
                path=path,
                relative_path=rel_path,
                config_status=cached["config_status"],
                logger_status=cached["logger_status"],
                test_file_exists=cached["test_file_exists"],
            )

        try:
            tree = ast.parse(path.read_text(), filename=str(path))
        except Exception:
            return FileMetrics(
                path=path,
                relative_path=rel_path,
                config_status="⚪ N/A",
                logger_status="⚪ N/A",
                test_file_exists=False,
            )

        config_status = self._analyze_config(tree)
        logger_status = self._analyze_logger(tree)
        test_file_exists = self._check_test_file(path)

        metrics = FileMetrics(
            path=path,
            relative_path=rel_path,
            config_status=config_status,
            logger_status=logger_status,
            test_file_exists=test_file_exists,
        )

        self.cache_manager.update_cache(path, metrics)
        return metrics

    def _analyze_config(
        self, tree: ast.AST
    ) -> Literal["✅ OK", "🔴 TYPED_DICT", "⚪ N/A"]:
        has_typed_dict = False
        has_pydantic = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if "TypedDict" in alias.name:
                        has_typed_dict = True
                    if "pydantic" in alias.name or "BaseModel" in alias.name:
                        has_pydantic = True
            elif isinstance(node, ast.ImportFrom):
                if node.module and "typing" in node.module:
                    for alias in node.names:
                        if alias.name == "TypedDict":
                            has_typed_dict = True
                if node.module and "pydantic" in node.module:
                    has_pydantic = True

        if has_typed_dict:
            return "🔴 TYPED_DICT"
        if has_pydantic:
            return "✅ OK"
        return "⚪ N/A"

    def _analyze_logger(
        self, tree: ast.AST
    ) -> Literal["✅ OK", "⚠️ UNUSED", "🔴 MISSING", "⚪ N/A"]:
        has_logger_import = False
        has_logger_usage = False

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and "logger" in node.module:
                    has_logger_import = True
            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id == "logger":
                    has_logger_usage = True

        if not has_logger_import:
            return "⚪ N/A"
        if has_logger_import and not has_logger_usage:
            return "⚠️ UNUSED"
        if has_logger_import and has_logger_usage:
            return "✅ OK"
        return "🔴 MISSING"

    def _check_test_file(self, path: Path) -> bool:
        """Teszt fájl keresése a test_<parent>_<file> konvenció szerint."""
        rel_path = path.relative_to(self.root_dir)
        file_stem = rel_path.stem  # neural_ai/core/base/factory.py -> "factory"
        dir_parts = rel_path.parent.parts  # ("neural_ai", "core", "base")

        # 1. Mirror Rule (test_factory.py) - egyedi név
        test_path = self.tests_dir / rel_path.parent / f"test_{rel_path.name}"
        if test_path.exists():
            return True

        # 2. test_<parent>_<file> konvenció (test_base_factory.py)
        if dir_parts:
            parent_name = dir_parts[-1]  # "base"
            alt_test_name = f"test_{parent_name}_{file_stem}.py"
            alt_test_path = self.tests_dir / rel_path.parent / alt_test_name
            if alt_test_path.exists():
                return True

        return False

    def analyze_all(self, files: list[Path]) -> list[FileMetrics]:
        """Több fájl párhuzamos elemzése."""
        print(f"📊 Statikus analízis: {len(files)} fájl...")

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(self.analyze_file, f): f for f in files}
            results = []

            for future in as_completed(futures):
                try:
                    results.append(future.result())  # pyright: ignore[reportUnknownMemberType]
                except Exception as e:
                    print(f"⚠️ Hiba: {futures[future]}: {e}")

        return results  # pyright: ignore[reportUnknownVariableType]


class QARunner:
    """Ruff + Mypy + Pyright párhuzamos futtatás."""

    def __init__(self, root_dir: Path):
        """QARunner inicializálása."""
        self.root_dir = root_dir
        self.conda_bin = Path.home() / "miniconda3/envs/neural-ai-next/bin"

    def run(self) -> dict[str, Any]:
        """QA eszközök párhuzamos futtatása."""
        print("🔍 QA eszközök futtatása...")

        results = {}
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self._run_ruff): "ruff",
                executor.submit(self._run_mypy): "mypy",
                executor.submit(self._run_pyright): "pyright",
            }

            for future in as_completed(futures):
                tool_name = futures[future]
                try:
                    results[tool_name] = future.result()
                    print(f"  ✅ {tool_name.capitalize()} kész")
                except Exception as e:
                    results[tool_name] = {"error": str(e)}
                    print(f"  ❌ {tool_name.capitalize()} hiba: {e}")

        return results  # pyright: ignore[reportUnknownVariableType]

    def _run_ruff(self) -> dict[str, Any]:
        cmd = [str(self.conda_bin / "ruff"), "check", ".", "--output-format=json"]
        result = subprocess.run(
            cmd, cwd=self.root_dir, capture_output=True, text=True, timeout=120
        )

        try:
            data: list[Any] = json.loads(result.stdout) if result.stdout else []  # pyright: ignore[reportUnknownVariableType]
            return {"errors": len(data), "details": data}  # pyright: ignore[reportUnknownArgumentType]
        except json.JSONDecodeError:
            return {"errors": 0, "details": []}

    def _run_mypy(self) -> dict[str, Any]:
        cmd = [str(self.conda_bin / "mypy"), "neural_ai", "--no-error-summary"]
        result = subprocess.run(
            cmd, cwd=self.root_dir, capture_output=True, text=True, timeout=120
        )

        errors = result.stdout.count("error:")
        return {"errors": errors, "output": result.stdout}

    def _run_pyright(self) -> dict[str, Any]:
        cmd = [str(self.conda_bin / "pyright"), "neural_ai"]
        result = subprocess.run(
            cmd, cwd=self.root_dir, capture_output=True, text=True, timeout=120
        )

        errors = result.stdout.count("error")
        return {"errors": errors, "output": result.stdout}


class CoverageRunner:
    """Coverage + Pytest szekvenciális futtatás."""

    def __init__(self, root_dir: Path):
        """CoverageRunner inicializálása."""
        self.root_dir = root_dir
        self.conda_bin = Path.home() / "miniconda3/envs/neural-ai-next/bin"

    def run(self) -> dict[str, Any]:
        """Coverage + Pytest futtatása szekvenciálisan."""
        print("📊 Coverage + Pytest futtatása (szekvenciális)...")

        cmd = [
            str(self.conda_bin / "coverage"),
            "run",
            "-m",
            "pytest",
            "tests/",
            "-p",
            "no:xdist",
            "-v",
        ]

        result = subprocess.run(
            cmd, cwd=self.root_dir, capture_output=True, text=True, timeout=900
        )

        subprocess.run(
            [str(self.conda_bin / "coverage"), "json"],
            cwd=self.root_dir,
            capture_output=True,
            timeout=60,
        )

        coverage_file = self.root_dir / "coverage.json"
        coverage_data = {}
        if coverage_file.exists():
            try:
                coverage_data = json.loads(coverage_file.read_text())
            except Exception:
                pass

        return {
            "coverage": coverage_data,
            "pytest_output": result.stdout,
            "exit_code": result.returncode,
        }


class TestRunner:
    """Csak Pytest (gyors, párhuzamos)."""

    def __init__(self, root_dir: Path):
        """TestRunner inicializálása."""
        self.root_dir = root_dir
        self.conda_bin = Path.home() / "miniconda3/envs/neural-ai-next/bin"

    def run(self) -> dict[str, Any]:
        """Pytest futtatása párhuzamosan."""
        print("🧪 Pytest futtatása (párhuzamos)...")

        cmd = [
            str(self.conda_bin / "pytest"),
            "tests/",
            "-n",
            "auto",
            "-v",
            "--tb=short",
        ]

        result = subprocess.run(
            cmd, cwd=self.root_dir, capture_output=True, text=True, timeout=600
        )

        passed = result.stdout.count(" PASSED")
        failed = result.stdout.count(" FAILED")

        return {
            "passed": passed,
            "failed": failed,
            "output": result.stdout,
            "exit_code": result.returncode,
        }


class ReportGenerator:
    """Markdown + HTML generálás táblázatos formátummal."""

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

    def __init__(self, root_dir: Path):
        """ReportGenerator inicializálása."""
        self.root_dir = root_dir

    def _group_by_layer(self, files: list[Any]) -> dict[str, list[Any]]:
        """Csoportosítja a fájlokat réteg szerint."""
        grouped: dict[str, list[Any]] = {layer: [] for layer in self.LAYER_MAPPING.keys()}

        for file_metric in files:
            parts = Path(file_metric.relative_path).parts

            if len(parts) == 1 or (
                len(parts) == 2 and parts[0] == "neural_ai" and parts[1] == "__init__.py"
            ):
                grouped["root"].append(file_metric)
            elif len(parts) > 0:
                first_part = parts[0]
                if first_part == "neural_ai" and len(parts) > 1:
                    if parts[1] in self.LAYER_MAPPING:
                        grouped[parts[1]].append(file_metric)
                elif first_part in self.LAYER_MAPPING:
                    grouped[first_part].append(file_metric)

        return grouped

    def generate_md(self, report: ProjectReport) -> str:
        """Generálja a Markdown táblázatos formátumot (generate.py MarkdownGenerator alapján)."""
        stats = self._calculate_stats(report.files)
        from datetime import UTC
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

        grouped = self._group_by_layer(report.files)

        content = f"""# 🌳 NEURAL AI NEXT - TASK TREE

**Generálva:** {now}
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
**Fájlok száma:** {stats["total"]}

## 📊 Statisztika

- ✅ **PERFECT:** {stats["perfect"]} ({stats["perfect"] / stats["total"] * 100:.1f}%)
- 🟢 **STABLE:** {stats["stable"]} ({stats["stable"] / stats["total"] * 100:.1f}%)
- 🟡 **WIP:** {stats["wip"]} ({stats["wip"] / stats["total"] * 100:.1f}%)
- 🔴 **CRITICAL:** {stats["critical"]} ({stats["critical"] / stats["total"] * 100:.1f}%)

---
"""

        for layer in self.LAYER_MAPPING.keys():
            if layer in grouped and grouped[layer]:
                content += self._create_markdown_table(layer, grouped[layer])

        return content

    def _create_markdown_table(self, layer: str, files: list[Any]) -> str:
        """Létrehoz egy Markdown táblázatot egy réteghez (MarkdownGenerator alapján)."""
        if not files:
            return ""

        num, name, path = self.LAYER_MAPPING[layer]
        table = f"\n## {num}. {name} Layer (`{path}`)\n\n"

        if layer == "scripts":
            table += (
                "| Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip/Warn | "
                "Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | "
                "Config | Logger | Dokumentálva | Teendők |\n"
            )
            table += (
                "|:-----|:--------|:----------|:-------------------|"
                ":---------------------|:------------------|:---------|"
                ":-------|:-------|:-------------|:--------|\n"
            )
        elif layer == "tests":
            table += (
                "| Fájl | Státusz | Pass/Fail/Err/Skip/Warn | "
                "Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | "
                "Dokumentálva | Teendők |\n"
            )
            table += (
                "|:-----|:--------|:-------------------|"
                ":---------------------|:------------------|:---------|"
                ":-------------|:--------|\n"
            )
        else:
            table += (
                "| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip/Warn | "
                "Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | "
                "Config | Logger | Dokumentálva | Teendők |\n"
            )
            table += (
                "|:-------------|:--------|:----------|:-------------------|"
                ":---------------------|:------------------|:---------|"
                ":-------|:-------|:-------------|:--------|\n"
            )

        for file in sorted(files, key=lambda x: x.relative_path):
            short_path = file.relative_path

            test_pair = "✅ FOUND" if file.test_file_exists else "❌ MISSING"

            test_results = "-"
            if file.test_passed > 0 or file.test_failed > 0:
                test_results = f"**{file.test_passed}**/{file.test_failed}/0/0/0"

            coverage = "N/A"
            if file.coverage_stmt >= 0:
                coverage = f"{file.coverage_stmt:.0f}% / {file.coverage_branch:.0f}%"

            lint_mypy = f"{file.lint_errors} / {file.type_errors} / 0"
            status = file.get_status_emoji()

            if layer == "scripts":
                table += (
                    f"| `{short_path}` | {status} | {test_pair} | "
                    f"{test_results} | {coverage} | {lint_mypy} | "
                    f"- | {file.config_status} | {file.logger_status} | "
                    f"❌ | - |\n"
                )
            elif layer == "tests":
                table += (
                    f"| `{short_path}` | {status} | "
                    f"{test_results} | {coverage} | {lint_mypy} | "
                    f"- | ❌ | - |\n"
                )
            else:
                table += (
                    f"| `{short_path}` | {status} | {test_pair} | "
                    f"{test_results} | {coverage} | {lint_mypy} | "
                    f"- | {file.config_status} | {file.logger_status} | "
                    f"❌ | - |\n"
                )

        return table

    def generate_html(self, report: ProjectReport) -> str:
        """Generálja a HTML Dashboard formátumot (generate.py HTMLGenerator alapján)."""
        stats = self._calculate_stats(report.files)
        from datetime import UTC
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

        grouped = self._group_by_layer(report.files)

        secure_pct = (stats["perfect"] / stats["total"] * 100) if stats["total"] > 0 else 0
        warning_pct = (stats["wip"] / stats["total"] * 100) if stats["total"] > 0 else 0
        critical_pct = (stats["critical"] / stats["total"] * 100) if stats["total"] > 0 else 0

        html_output = f"""<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neural AI Next - Task Tree Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet">
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
        }}
        .meta {{
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.6;
        }}
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
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        .stat-label {{
            color: #94a3b8;
            font-size: 0.875rem;
            text-transform: uppercase;
        }}
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
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
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
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        }}
        td {{
            padding: 1rem 1.25rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.05);
            font-size: 0.9rem;
        }}
        .file-path {{
            font-family: 'SF Mono', monospace;
            color: #93c5fd;
            font-size: 0.875rem;
        }}
        .status-badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.375rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .status-perfect {{ background: rgba(16, 185, 129, 0.15); color: #10b981; }}
        .status-stable {{ background: rgba(34, 197, 94, 0.15); color: #22c55e; }}
        .status-wip {{ background: rgba(245, 158, 11, 0.15); color: #f59e0b; }}
        .status-critical {{ background: rgba(239, 68, 68, 0.15); color: #ef4444; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>⚡ Neural AI Next - Task Tree Dashboard</h1>
            <div class="meta">
                <strong>Generálva:</strong> {now} &nbsp;|&nbsp;
                <strong>Módszer:</strong> Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
                &nbsp;|&nbsp;
                <strong>Fájlok:</strong> {stats["total"]}
            </div>
        </div>
    </div>

    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" style="color: #10b981;">✓</div>
                <div class="stat-label">Perfect</div>
                <div style="font-size: 1.5rem; margin-top: 0.5rem; color: #10b981;">
                    {stats["perfect"]}
                </div>
                <div style="color: #94a3b8; margin-top: 0.25rem;">{secure_pct:.1f}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #22c55e;">◉</div>
                <div class="stat-label">Stable</div>
                <div style="font-size: 1.5rem; margin-top: 0.5rem; color: #22c55e;">
                    {stats["stable"]}
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #f59e0b;">⚠</div>
                <div class="stat-label">WIP</div>
                <div style="font-size: 1.5rem; margin-top: 0.5rem; color: #f59e0b;">
                    {stats["wip"]}
                </div>
                <div style="color: #94a3b8; margin-top: 0.25rem;">{warning_pct:.1f}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #ef4444;">✕</div>
                <div class="stat-label">Critical</div>
                <div style="font-size: 1.5rem; margin-top: 0.5rem; color: #ef4444;">
                    {stats["critical"]}
                </div>
                <div style="color: #94a3b8; margin-top: 0.25rem;">{critical_pct:.1f}%</div>
            </div>
        </div>
"""

        for layer in self.LAYER_MAPPING.keys():
            if layer in grouped and grouped[layer]:
                html_output += self._create_html_table(layer, grouped[layer])

        html_output += """
    </div>
</body>
</html>"""
        return html_output

    def _create_html_table(self, layer: str, files: list[Any]) -> str:
        """Létrehoz egy HTML táblázatot egy réteghez (HTMLGenerator alapján)."""
        if not files:
            return ""

        num, name, path = self.LAYER_MAPPING[layer]

        layer_icons = {
            "root": "🏠", "core": "⚙️", "collectors": "📡",
            "data": "💾", "processors": "🧠", "ui": "🎨",
            "tests": "🧪", "scripts": "📜",
        }
        icon = layer_icons.get(layer, "📦")

        html_output = f"""
            <div class="layer">
                <div class="layer-title">
                    {icon} {num}. {name} Layer
                    <span style="opacity: 0.6; font-size: 0.9rem;">({path})</span>
                </div>
                <table>
                    <thead>
                        <tr>"""

        if layer == "scripts":
            html_output += """
                            <th>Fájl</th>
                            <th>Státusz</th>
                            <th>Teszt Pár</th>
                            <th>Pass/Fail/Err/Skip/Warn</th>
                            <th>Coverage (Stmt/Brch)</th>
                            <th>Lint/Mypy/Pylance</th>
                            <th>Src Warn</th>
                            <th>Config</th>
                            <th>Logger</th>
                            <th>Dokumentálva</th>
                            <th>Teendők</th>"""
        elif layer == "tests":
            html_output += """
                            <th>Fájl</th>
                            <th>Státusz</th>
                            <th>Pass/Fail/Err/Skip/Warn</th>
                            <th>Coverage (Stmt/Brch)</th>
                            <th>Lint/Mypy/Pylance</th>
                            <th>Src Warn</th>
                            <th>Dokumentálva</th>
                            <th>Teendők</th>"""
        else:
            html_output += """
                            <th>Modul / Fájl</th>
                            <th>Státusz</th>
                            <th>Teszt Pár</th>
                            <th>Pass/Fail/Err/Skip/Warn</th>
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
            short_path = html.escape(file.relative_path)

            status_emoji = file.get_status_emoji()
            if status_emoji == "✅":
                status_badge = '<span class="status-badge status-perfect">✓ PERFECT</span>'
            elif status_emoji == "🟢":
                status_badge = '<span class="status-badge status-stable">◉ STABLE</span>'
            elif status_emoji == "🟡":
                status_badge = '<span class="status-badge status-wip">⚠ WIP</span>'
            else:
                status_badge = '<span class="status-badge status-critical">✕ CRITICAL</span>'

            test_results = "-"
            if file.test_passed > 0 or file.test_failed > 0:
                test_results = (
                    f"<span style='color: #10b981;'>{file.test_passed}</span>"
                    f"/{file.test_failed}/0/0/0"
                )

            coverage = "N/A"
            if file.coverage_stmt >= 0:
                cov_class = "color: #10b981;" if file.coverage_stmt >= 80 else "color: #ef4444;"
                coverage = (
                    f"<span style='{cov_class}'>{file.coverage_stmt:.0f}%</span>"
                    f" / {file.coverage_branch:.0f}%"
                )

            lint_mypy = f"{file.lint_errors} / {file.type_errors} / 0"
            test_pair = (
                '<span style="color: #10b981;">✓ FOUND</span>'
                if file.test_file_exists
                else '<span style="color: #ef4444;">✕ MISSING</span>'
            )

            if layer == "scripts":
                html_output += f"""
                        <tr>
                            <td class="file-path">{short_path}</td>
                            <td>{status_badge}</td>
                            <td>{test_pair}</td>
                            <td>{test_results}</td>
                            <td>{coverage}</td>
                            <td>{lint_mypy}</td>
                            <td>-</td>
                            <td>{file.config_status}</td>
                            <td>{file.logger_status}</td>
                            <td>❌</td>
                            <td>-</td>
                        </tr>
    """
            elif layer == "tests":
                html_output += f"""
                        <tr>
                            <td class="file-path">{short_path}</td>
                            <td>{status_badge}</td>
                            <td>{test_results}</td>
                            <td>{coverage}</td>
                            <td>{lint_mypy}</td>
                            <td>-</td>
                            <td>❌</td>
                            <td>-</td>
                        </tr>
    """
            else:
                html_output += f"""
                        <tr>
                            <td class="file-path">{short_path}</td>
                            <td>{status_badge}</td>
                            <td>{test_pair}</td>
                            <td>{test_results}</td>
                            <td>{coverage}</td>
                            <td>{lint_mypy}</td>
                            <td>-</td>
                            <td>{file.config_status}</td>
                            <td>{file.logger_status}</td>
                            <td>❌</td>
                            <td>-</td>
                        </tr>
    """

        html_output += """
                    </tbody>
                </table>
            </div>
    """
        return html_output

    def _calculate_stats(self, files: list[Any]) -> dict[str, int]:
        """Statisztikákat számol."""
        stats = {
            "total": len(files),
            "perfect": 0,
            "stable": 0,
            "wip": 0,
            "critical": 0,
        }

        for file in files:
            emoji = file.get_status_emoji()
            if emoji == "✅":
                stats["perfect"] += 1
            elif emoji == "🟢":
                stats["stable"] += 1
            elif emoji == "🟡":
                stats["wip"] += 1
            else:
                stats["critical"] += 1

        return stats


# ============================================================================
# 4. VEZÉRLŐ RÉTEG (Command Pattern)
# ============================================================================


class CommandProtocol(Protocol):
    """Command interfész."""

    def execute(self) -> ProjectReport:
        """Parancs végrehajtása."""
        ...


class FullCommand:
    """--full: QA + Coverage + Static."""

    def __init__(self, root_dir: Path, force_refresh: bool = False):
        """FullCommand inicializálása."""
        self.root_dir = root_dir
        self.force_refresh = force_refresh
        self.cache_manager = CacheManager()

    def execute(self) -> ProjectReport:
        """Teljes analízis futtatása."""
        print("🚀 FULL MODE: QA + Coverage + Static...")

        files = self._collect_files()
        static_analyzer = StaticAnalyzer(self.cache_manager, self.root_dir)
        metrics = static_analyzer.analyze_all(files)

        qa_runner = QARunner(self.root_dir)
        qa_results = qa_runner.run()

        cov_runner = CoverageRunner(self.root_dir)
        cov_results = cov_runner.run()

        self._merge_qa_results(metrics, qa_results)
        self._merge_coverage_results(metrics, cov_results)

        self.cache_manager.save_cache()

        return ProjectReport(
            files=metrics,
            generated_at=datetime.now(),
            mode="full",
            summary={"qa": qa_results, "coverage": cov_results},
        )

    def _collect_files(self) -> list[Path]:
        files: list[Path] = []
        for pattern in ["neural_ai/**/*.py", "scripts/**/*.py"]:
            files.extend(self.root_dir.glob(pattern))
        return [f for f in files if "__pycache__" not in str(f)]

    def _merge_qa_results(
        self, metrics: list[FileMetrics], qa_results: dict[str, Any]
    ) -> None:
        """QA eredmények (Ruff, Mypy, Pyright) fájlonkénti hozzárendelése."""
        # Ruff: fájlonkénti hibák JSON-ből
        ruff_files = qa_results.get("ruff", {}).get("files", {})
        ruff_by_path = {}
        for item in ruff_files:
            file_path = str(Path(item.get("filename", "")).relative_to(self.root_dir))
            ruff_by_path[file_path] = ruff_by_path.get(file_path, 0) + 1

        for fm in metrics:
            rel_path = str(fm.relative_path)
            # Ruff: fájlonkénti érték
            fm.lint_errors = ruff_by_path.get(rel_path, 0)
            # Mypy/Pyright: 0 ha nincs fájlonkénti adat
            fm.type_errors = 0

    def _merge_coverage_results(
        self, metrics: list[FileMetrics], cov_results: dict[str, Any]
    ) -> None:
        """Coverage adatok fájlonkénti hozzárendelése."""
        coverage_data = cov_results.get("coverage", {}).get("files", {})

        for fm in metrics:
            # 1. Próbáld meg az abszolút útvonallal
            file_key = str(fm.path)
            if file_key in coverage_data:
                file_cov = coverage_data[file_key].get("summary", {})
                fm.coverage_stmt = file_cov.get("percent_covered", 0.0)
                fm.coverage_branch = file_cov.get("branch_percent_covered", 0.0)
                continue

            # 2. Próbáld meg a relatív útvonallal
            rel_key = str(fm.relative_path)
            if rel_key in coverage_data:
                file_cov = coverage_data[rel_key].get("summary", {})
                fm.coverage_stmt = file_cov.get("percent_covered", 0.0)
                fm.coverage_branch = file_cov.get("branch_percent_covered", 0.0)
                continue

            # 3. Ha nincs adat, maradjon 0.0
            fm.coverage_stmt = 0.0
            fm.coverage_branch = 0.0


class QuickCommand:
    """--quick: Csak AST + cache."""

    def __init__(self, root_dir: Path):
        """QuickCommand inicializálása."""
        self.root_dir = root_dir
        self.cache_manager = CacheManager()

    def execute(self) -> ProjectReport:
        """Gyors analízis futtatása."""
        print("⚡ QUICK MODE: Csak AST...")

        files = self._collect_files()
        static_analyzer = StaticAnalyzer(self.cache_manager, self.root_dir)
        metrics = static_analyzer.analyze_all(files)

        self.cache_manager.save_cache()

        return ProjectReport(files=metrics, generated_at=datetime.now(), mode="quick")

    def _collect_files(self) -> list[Path]:
        files: list[Path] = []
        for pattern in ["neural_ai/**/*.py", "scripts/**/*.py"]:
            files.extend(self.root_dir.glob(pattern))
        return [f for f in files if "__pycache__" not in str(f)]


class QAOnlyCommand:
    """--qa: Csak QA eszközök."""

    def __init__(self, root_dir: Path):
        """QAOnlyCommand inicializálása."""
        self.root_dir = root_dir
        self.cache_manager = CacheManager()

    def execute(self) -> ProjectReport:
        """QA eszközök futtatása."""
        print("🔍 QA MODE...")

        files = self._collect_files()
        static_analyzer = StaticAnalyzer(self.cache_manager, self.root_dir)
        metrics = static_analyzer.analyze_all(files)

        qa_runner = QARunner(self.root_dir)
        qa_results = qa_runner.run()

        self._merge_qa_results(metrics, qa_results)
        self.cache_manager.save_cache()

        return ProjectReport(
            files=metrics,
            generated_at=datetime.now(),
            mode="qa",
            summary={"qa": qa_results},
        )

    def _collect_files(self) -> list[Path]:
        files: list[Path] = []
        for pattern in ["neural_ai/**/*.py", "scripts/**/*.py"]:
            files.extend(self.root_dir.glob(pattern))
        return [f for f in files if "__pycache__" not in str(f)]

    def _merge_qa_results(
        self, metrics: list[FileMetrics], qa_results: dict[str, Any]
    ) -> None:
        """QA eredmények (Ruff, Mypy, Pyright) fájlonkénti hozzárendelése."""
        # Ruff: fájlonkénti hibák JSON-ből
        ruff_files = qa_results.get("ruff", {}).get("files", {})
        ruff_by_path = {}
        for item in ruff_files:
            file_path = str(Path(item.get("filename", "")).relative_to(self.root_dir))
            ruff_by_path[file_path] = ruff_by_path.get(file_path, 0) + 1

        for fm in metrics:
            rel_path = str(fm.relative_path)
            # Ruff: fájlonkénti érték
            fm.lint_errors = ruff_by_path.get(rel_path, 0)
            # Mypy/Pyright: 0 ha nincs fájlonkénti adat
            fm.type_errors = 0


class CoverageOnlyCommand:
    """--coverage: Csak Coverage + Pytest."""

    def __init__(self, root_dir: Path):
        """CoverageOnlyCommand inicializálása."""
        self.root_dir = root_dir
        self.cache_manager = CacheManager()

    def execute(self) -> ProjectReport:
        """Coverage analízis futtatása."""
        print("📊 COVERAGE MODE...")

        files = self._collect_files()
        static_analyzer = StaticAnalyzer(self.cache_manager, self.root_dir)
        metrics = static_analyzer.analyze_all(files)

        cov_runner = CoverageRunner(self.root_dir)
        cov_results = cov_runner.run()

        self._merge_coverage_results(metrics, cov_results)
        self.cache_manager.save_cache()

        return ProjectReport(
            files=metrics,
            generated_at=datetime.now(),
            mode="coverage",
            summary={"coverage": cov_results},
        )

    def _collect_files(self) -> list[Path]:
        files: list[Path] = []
        for pattern in ["neural_ai/**/*.py", "scripts/**/*.py"]:
            files.extend(self.root_dir.glob(pattern))
        return [f for f in files if "__pycache__" not in str(f)]

    def _merge_coverage_results(
        self, metrics: list[FileMetrics], cov_results: dict[str, Any]
    ) -> None:
        """Coverage adatok fájlonkénti hozzárendelése."""
        coverage_data = cov_results.get("coverage", {}).get("files", {})

        for fm in metrics:
            # 1. Próbáld meg az abszolút útvonallal
            file_key = str(fm.path)
            if file_key in coverage_data:
                file_cov = coverage_data[file_key].get("summary", {})
                fm.coverage_stmt = file_cov.get("percent_covered", 0.0)
                fm.coverage_branch = file_cov.get("branch_percent_covered", 0.0)
                continue

            # 2. Próbáld meg a relatív útvonallal
            rel_key = str(fm.relative_path)
            if rel_key in coverage_data:
                file_cov = coverage_data[rel_key].get("summary", {})
                fm.coverage_stmt = file_cov.get("percent_covered", 0.0)
                fm.coverage_branch = file_cov.get("branch_percent_covered", 0.0)
                continue

            # 3. Ha nincs adat, maradjon 0.0
            fm.coverage_stmt = 0.0
            fm.coverage_branch = 0.0


class TestOnlyCommand:
    """--test: Csak Pytest."""

    def __init__(self, root_dir: Path):
        """TestOnlyCommand inicializálása."""
        self.root_dir = root_dir
        self.cache_manager = CacheManager()

    def execute(self) -> ProjectReport:
        """Pytest futtatása."""
        print("🧪 TEST MODE...")

        files = self._collect_files()
        static_analyzer = StaticAnalyzer(self.cache_manager, self.root_dir)
        metrics = static_analyzer.analyze_all(files)

        test_runner = TestRunner(self.root_dir)
        test_results = test_runner.run()

        self.cache_manager.save_cache()

        return ProjectReport(
            files=metrics,
            generated_at=datetime.now(),
            mode="test",
            summary={"test": test_results},
        )

    def _collect_files(self) -> list[Path]:
        files: list[Path] = []
        for pattern in ["neural_ai/**/*.py", "scripts/**/*.py"]:
            files.extend(self.root_dir.glob(pattern))
        return [f for f in files if "__pycache__" not in str(f)]


# ============================================================================
# 5. CLI INTERFACE & MAIN
# ============================================================================


def main() -> int:
    """Főprogram belépési pont."""
    parser = argparse.ArgumentParser(description="TASK_TREE Generátor V2")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--full", action="store_true", help="Teljes analízis")
    group.add_argument("--quick", action="store_true", help="Gyors mód")
    group.add_argument("--qa", action="store_true", help="Csak QA")
    group.add_argument("--coverage", action="store_true", help="Csak Coverage")
    group.add_argument("--test", action="store_true", help="Csak Test")

    parser.add_argument("--force-refresh", action="store_true", help="Cache törlés")

    args = parser.parse_args()

    root_dir = Path.cwd()
    output_md = root_dir / "docs/development/TASK_TREE.md"
    output_html = root_dir / "docs/development/TASK_TREE.html"

    if args.force_refresh:
        cache_file = Path(".cache/generate_cache.json")
        if cache_file.exists():
            cache_file.unlink()
            print("🗑️ Cache törölve")

    try:
        command: CommandProtocol
        if args.full:
            command = FullCommand(root_dir, args.force_refresh)
        elif args.quick:
            command = QuickCommand(root_dir)
        elif args.qa:
            command = QAOnlyCommand(root_dir)
        elif args.coverage:
            command = CoverageOnlyCommand(root_dir)
        else:
            command = TestOnlyCommand(root_dir)

        report = command.execute()

        generator = ReportGenerator(root_dir)
        md_content = generator.generate_md(report)
        html_content = generator.generate_html(report)

        output_md.write_text(md_content)
        output_html.write_text(html_content)

        print("\n✅ Generálás kész!")
        print(f"   MD: {output_md}")
        print(f"   HTML: {output_html}")

        return 0

    except Exception as e:
        print(f"\n❌ Hiba: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
