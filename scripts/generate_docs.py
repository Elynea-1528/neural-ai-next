#!/usr/bin/env python3
"""Profi dokumentáció generátor a Neural AI Next projekthez.

Ez a script AST-alapú elemzéssel generál részletes, profi szintű dokumentációt:
- Google Style docstring parsing
- Függvény szignatúrák type hints-tel
- Paraméter és return type dokumentáció
- Import és dependency tracking
- Tükör struktúra: root, scripts, neural_ai mappák
"""

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Parameter:
    """Függvény paraméter reprezentáció."""

    name: str
    type_hint: str | None = None
    default: str | None = None
    description: str | None = None


@dataclass
class FunctionInfo:
    """Függvény információ."""

    name: str
    signature: str
    docstring: str | None = None
    parameters: list[Parameter] = field(default_factory=list)
    return_type: str | None = None
    return_description: str | None = None
    raises: list[tuple[str, str]] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    is_async: bool = False


@dataclass
class ClassInfo:
    """Osztály információ."""

    name: str
    docstring: str | None = None
    bases: list[str] = field(default_factory=list)
    methods: list[FunctionInfo] = field(default_factory=list)
    attributes: list[tuple[str, str | None]] = field(default_factory=list)


@dataclass
class ModuleInfo:
    """Modul információ."""

    file_path: Path
    module_docstring: str | None = None
    imports: list[str] = field(default_factory=list)
    classes: list[ClassInfo] = field(default_factory=list)
    functions: list[FunctionInfo] = field(default_factory=list)
    constants: list[tuple[str, str | None]] = field(default_factory=list)


class GoogleDocstringParser:
    """Google Style docstring parser."""

    @staticmethod
    def parse(docstring: str | None) -> dict[str, Any]:
        """Parse Google Style docstring.

        Args:
            docstring: A docstring szöveg.

        Returns:
            Dict a parsed adatokkal (description, args, returns, raises, examples).
        """
        if not docstring:
            return {
                "description": None,
                "args": {},
                "returns": None,
                "raises": [],
                "examples": [],
            }

        lines = docstring.strip().split("\n")
        result: dict[str, Any] = {
            "description": [],
            "args": {},
            "returns": None,
            "raises": [],
            "examples": [],
        }

        current_section = "description"
        current_arg = None

        for line in lines:
            line_stripped = line.strip()

            # Section headers
            if line_stripped in ["Args:", "Arguments:"]:
                current_section = "args"
                continue
            elif line_stripped in ["Returns:", "Return:"]:
                current_section = "returns"
                continue
            elif line_stripped == "Raises:":
                current_section = "raises"
                continue
            elif line_stripped in ["Examples:", "Example:"]:
                current_section = "examples"
                continue

            # Parse content
            if current_section == "description":
                if line_stripped:
                    result["description"].append(line_stripped)

            elif current_section == "args":
                # Match "param_name: description" or "param_name (type): description"
                match = re.match(r"(\w+)(?:\s*\(([^)]+)\))?\s*:\s*(.+)", line_stripped)
                if match:
                    param_name, param_type, param_desc = match.groups()
                    current_arg = param_name
                    result["args"][param_name] = {
                        "type": param_type,
                        "description": param_desc,
                    }
                elif current_arg and line_stripped:
                    # Continuation of previous arg description
                    result["args"][current_arg]["description"] += " " + line_stripped

            elif current_section == "returns":
                if line_stripped:
                    if result["returns"] is None:
                        result["returns"] = line_stripped
                    else:
                        result["returns"] += " " + line_stripped

            elif current_section == "raises":
                # Match "ExceptionType: description"
                match = re.match(r"(\w+)\s*:\s*(.+)", line_stripped)
                if match:
                    exc_type, exc_desc = match.groups()
                    result["raises"].append((exc_type, exc_desc))

            elif current_section == "examples":
                if line_stripped:
                    result["examples"].append(line)

        # Join description
        result["description"] = " ".join(result["description"]) if result["description"] else None

        return result


class ASTExtractor(ast.NodeVisitor):
    """AST-alapú kód elemző."""

    def __init__(self, file_path: Path) -> None:
        """Inicializálja az elemzőt.

        Args:
            file_path: A Python fájl elérési útja.
        """
        self.file_path = file_path
        self.module_info = ModuleInfo(file_path=file_path)
        self.current_class: ClassInfo | None = None

    def visit_Module(self, node: ast.Module) -> None:
        """Modul docstring kinyerése."""
        if node.body and isinstance(node.body[0], ast.Expr):
            docstring_node = node.body[0].value
            if isinstance(docstring_node, ast.Constant) and isinstance(docstring_node.value, str):
                self.module_info.module_docstring = docstring_node.value.strip()
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        """Import statement kinyerése."""
        for alias in node.names:
            self.module_info.imports.append(f"import {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """From import statement kinyerése."""
        module = node.module or ""
        for alias in node.names:
            self.module_info.imports.append(f"from {module} import {alias.name}")
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Osztály definíció kinyerése."""
        docstring = ast.get_docstring(node)
        bases = [self._get_name(base) for base in node.bases]

        class_info = ClassInfo(
            name=node.name,
            docstring=docstring,
            bases=bases,
        )

        self.current_class = class_info
        self.generic_visit(node)
        self.current_class = None

        self.module_info.classes.append(class_info)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Függvény definíció kinyerése."""
        func_info = self._extract_function(node, is_async=False)

        if self.current_class:
            self.current_class.methods.append(func_info)
        else:
            self.module_info.functions.append(func_info)

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Aszinkron függvény definíció kinyerése."""
        func_info = self._extract_function(node, is_async=True)

        if self.current_class:
            self.current_class.methods.append(func_info)
        else:
            self.module_info.functions.append(func_info)

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Konstans/változó kinyerése (modul szintű)."""
        if self.current_class is None:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    value_str = ast.unparse(node.value) if hasattr(ast, "unparse") else None
                    self.module_info.constants.append((target.id, value_str))
        self.generic_visit(node)

    def _extract_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_async: bool
    ) -> FunctionInfo:
        """Függvény információ kinyerése."""
        docstring = ast.get_docstring(node)
        parsed_doc = GoogleDocstringParser.parse(docstring)

        # Paraméterek
        parameters: list[Parameter] = []
        for arg in node.args.args:
            param_name = arg.arg
            type_hint = self._get_annotation(arg.annotation)
            default = None

            # Default értékek
            defaults_offset = len(node.args.args) - len(node.args.defaults)
            arg_index = node.args.args.index(arg)
            if arg_index >= defaults_offset:
                default_node = node.args.defaults[arg_index - defaults_offset]
                default = ast.unparse(default_node) if hasattr(ast, "unparse") else None

            # Docstring leírás
            description = None
            if param_name in parsed_doc["args"]:
                description = parsed_doc["args"][param_name]["description"]

            parameters.append(
                Parameter(
                    name=param_name,
                    type_hint=type_hint,
                    default=default,
                    description=description,
                )
            )

        # Return type
        return_type = self._get_annotation(node.returns)

        # Signature
        signature = self._build_signature(node.name, parameters, return_type, is_async)

        return FunctionInfo(
            name=node.name,
            signature=signature,
            docstring=parsed_doc["description"],
            parameters=parameters,
            return_type=return_type,
            return_description=parsed_doc["returns"],
            raises=parsed_doc["raises"],
            examples=parsed_doc["examples"],
            is_async=is_async,
        )

    def _get_annotation(self, annotation: ast.expr | None) -> str | None:
        """Type annotation string kinyerése."""
        if annotation is None:
            return None
        if hasattr(ast, "unparse"):
            return ast.unparse(annotation)
        return None

    def _get_name(self, node: ast.expr) -> str:
        """Node név kinyerése."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif hasattr(ast, "unparse"):
            return ast.unparse(node)
        return "Unknown"

    def _build_signature(
        self,
        name: str,
        parameters: list[Parameter],
        return_type: str | None,
        is_async: bool,
    ) -> str:
        """Függvény szignatúra építése."""
        prefix = "async def" if is_async else "def"
        params_str = ", ".join(
            f"{p.name}: {p.type_hint}" + (f" = {p.default}" if p.default else "")
            if p.type_hint
            else p.name + (f" = {p.default}" if p.default else "")
            for p in parameters
        )
        return_str = f" -> {return_type}" if return_type else ""
        return f"{prefix} {name}({params_str}){return_str}"


class MarkdownBuilder:
    """Profi Markdown dokumentáció építő."""

    @staticmethod
    def build(module_info: ModuleInfo) -> str:
        """Markdown dokumentáció építése.

        Args:
            module_info: A modul információ.

        Returns:
            A generált Markdown tartalom.
        """
        # Teszt fájl detektálás
        is_test_file = module_info.file_path.parts[0] == "tests"

        if is_test_file:
            return MarkdownBuilder._build_test_file(module_info)
        else:
            return MarkdownBuilder._build_source_file(module_info)

    @staticmethod
    def _build_source_file(module_info: ModuleInfo) -> str:
        """Forrás fájl dokumentáció építése (eredeti logika)."""
        sections: list[str] = []

        # Header
        relative_path = module_info.file_path
        sections.append(f"# {relative_path}\n")

        # Module docstring
        if module_info.module_docstring:
            sections.append(f"{module_info.module_docstring}\n")

        # Imports
        if module_info.imports:
            sections.append("## Importok\n")
            sections.append("```python")
            sections.append("\n".join(module_info.imports[:10]))  # Max 10 import
            if len(module_info.imports) > 10:
                sections.append(f"# ... és még {len(module_info.imports) - 10} import")
            sections.append("```\n")

        # Constants
        if module_info.constants:
            sections.append("## Konstansok\n")
            for const_name, const_value in module_info.constants:
                sections.append(f"- **`{const_name}`**")
                if const_value:
                    sections.append(f": `{const_value}`")
                sections.append("\n")

        # Classes
        for class_info in module_info.classes:
            sections.append(MarkdownBuilder._build_class(class_info))

        # Functions
        for func_info in module_info.functions:
            sections.append(MarkdownBuilder._build_function(func_info))

        # Footer
        sections.append("---\n")
        sections.append(f"**Forrásfájl:** [`{relative_path}`](../../{relative_path})\n")

        return "\n".join(sections)

    @staticmethod
    def _build_test_file(module_info: ModuleInfo) -> str:
        """Teszt fájl specifikus dokumentáció."""
        sections: list[str] = []

        # Header
        sections.append(f"# 🧪 Teszt: {module_info.file_path}\n")

        # Tesztelt modul
        tested_module = MarkdownBuilder._get_tested_module(module_info.file_path)
        sections.append(f"**Tesztelt modul:** [`{tested_module}`](../../{tested_module})\n")

        # Module docstring
        if module_info.module_docstring:
            sections.append(f"{module_info.module_docstring}\n")

        # Teszt osztályok
        for class_info in module_info.classes:
            sections.append(f"## Teszt Osztály: `{class_info.name}`\n")

            if class_info.docstring:
                sections.append(f"{class_info.docstring}\n")

            # Teszt metódusok
            for method in class_info.methods:
                if method.name.startswith("test_"):
                    sections.append(f"### ✓ `{method.name}()`\n")
                    if method.docstring:
                        sections.append(f"{method.docstring}\n")

        # Teszt függvények (osztályon kívül)
        test_functions = [f for f in module_info.functions if f.name.startswith("test_")]
        if test_functions:
            sections.append("## Teszt Függvények\n")
            for func in test_functions:
                sections.append(f"### ✓ `{func.name}()`\n")
                if func.docstring:
                    sections.append(f"{func.docstring}\n")

        # Footer
        sections.append("---\n")
        sections.append(
            f"**Teszt fájl:** "
            f"[`{module_info.file_path}`](../../{module_info.file_path})\n"
        )
        sections.append(
            f"**Tesztelt modul:** [`{tested_module}`](../../{tested_module})\n"
        )

        return "\n".join(sections)

    @staticmethod
    def _get_tested_module(test_path: Path) -> Path:
        """Tesztelt modul útvonal kiszámítása."""
        # tests/neural_ai/core/config/test_factory.py
        # -> neural_ai/core/config/factory.py
        parts = list(test_path.parts)
        if parts[0] == "tests":
            parts = parts[1:]  # Eltávolítjuk a "tests/" prefix-et

        # test_factory.py -> factory.py
        filename = parts[-1].replace("test_", "")
        parts[-1] = filename

        return Path(*parts)

    @staticmethod
    def _build_class(class_info: ClassInfo) -> str:
        """Osztály dokumentáció építése."""
        sections: list[str] = []

        # Class header
        bases_str = f"({', '.join(class_info.bases)})" if class_info.bases else ""
        sections.append(f"## Osztály: `{class_info.name}{bases_str}`\n")

        # Docstring
        if class_info.docstring:
            sections.append(f"{class_info.docstring}\n")

        # Methods
        if class_info.methods:
            sections.append("### Metódusok\n")
            for method in class_info.methods:
                sections.append(MarkdownBuilder._build_function(method, indent=True))

        return "\n".join(sections)

    @staticmethod
    def _build_function(func_info: FunctionInfo, indent: bool = False) -> str:
        """Függvény dokumentáció építése."""
        sections: list[str] = []
        prefix = "####" if indent else "###"

        # Function header
        sections.append(f"{prefix} `{func_info.name}()`\n")

        # Signature
        sections.append("```python")
        sections.append(func_info.signature)
        sections.append("```\n")

        # Docstring
        if func_info.docstring:
            sections.append(f"{func_info.docstring}\n")

        # Parameters
        if func_info.parameters:
            sections.append("**Paraméterek:**\n")
            for param in func_info.parameters:
                param_line = f"- **`{param.name}`**"
                if param.type_hint:
                    param_line += f" (`{param.type_hint}`)"
                if param.default:
                    param_line += f" = `{param.default}`"
                if param.description:
                    param_line += f": {param.description}"
                sections.append(param_line)
            sections.append("")

        # Returns
        if func_info.return_type or func_info.return_description:
            sections.append("**Visszatérési érték:**\n")
            if func_info.return_type:
                sections.append(f"- Típus: `{func_info.return_type}`")
            if func_info.return_description:
                sections.append(f"- {func_info.return_description}")
            sections.append("")

        # Raises
        if func_info.raises:
            sections.append("**Kivételek:**\n")
            for exc_type, exc_desc in func_info.raises:
                sections.append(f"- **`{exc_type}`**: {exc_desc}")
            sections.append("")

        # Examples
        if func_info.examples:
            sections.append("**Példák:**\n")
            sections.append("```python")
            sections.append("\n".join(func_info.examples))
            sections.append("```\n")

        return "\n".join(sections)


class MirrorManager:
    """Tükör struktúra kezelő (root, scripts, neural_ai)."""

    @staticmethod
    def get_doc_path(source_path: Path) -> Path:
        """Dokumentáció útvonal kiszámítása.

        Args:
            source_path: A forrásfájl elérési útja.

        Returns:
            A dokumentáció fájl elérési útja.
        """
        parts = source_path.parts

        # Root fájlok (main.py)
        if len(parts) == 1 and parts[0].endswith(".py"):
            return Path("docs/components") / source_path.with_suffix(".md")

        # scripts/ mappában
        if parts[0] == "scripts":
            return Path("docs/components") / source_path.with_suffix(".md")

        # tests/ mappában
        if parts[0] == "tests":
            return Path("docs/components") / source_path.with_suffix(".md")

        # neural_ai/ mappában
        if parts[0] == "neural_ai":
            return Path("docs/components") / source_path.with_suffix(".md")

        # Egyéb
        return Path("docs/components") / source_path.with_suffix(".md")


class DocumentationGenerator:
    """Profi dokumentáció generátor."""

    def __init__(
        self,
        source_dirs: list[str] | None = None,
        docs_dir: str = "docs/components",
    ) -> None:
        """Inicializálja a generátort.

        Args:
            source_dirs: A forráskód mappák listája.
            docs_dir: A dokumentáció mappa elérési útja.
        """
        default_dirs = ["neural_ai", "scripts", "tests", "."]
        self.source_dirs = [Path(d) for d in (source_dirs or default_dirs)]
        self.docs_dir = Path(docs_dir)
        self.ignored_dirs = {"__pycache__", ".pytest_cache", ".ruff_cache", ".git", ".venv", "venv"}
        self.ignored_files: set[str] = set()  # Üres - minden fájlt dokumentálunk

    def extract_module_info(self, file_path: Path) -> ModuleInfo | None:
        """Modul információ kinyerése.

        Args:
            file_path: A Python fájl elérési útja.

        Returns:
            A kinyert modul információ vagy None hiba esetén.
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            extractor = ASTExtractor(file_path)
            extractor.visit(tree)
            return extractor.module_info

        except (SyntaxError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Hiba a(z) {file_path} fájl elemzésekor: {e}")
            return None

    def generate_documentation(self, file_path: Path) -> None:
        """Dokumentáció generálása egy fájlhoz.

        Args:
            file_path: A forrásfájl elérési útja.
        """
        print(f"Feldolgozás: {file_path}")

        module_info = self.extract_module_info(file_path)
        if module_info is None:
            return

        markdown_content = MarkdownBuilder.build(module_info)

        # Tükör útvonal
        doc_path = MirrorManager.get_doc_path(file_path)
        doc_path.parent.mkdir(parents=True, exist_ok=True)

        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

    def generate_all(self) -> None:
        """Összes dokumentáció generálása."""
        print(
            f"Dokumentáció generálása: "
            f"{', '.join(str(d) for d in self.source_dirs)} -> {self.docs_dir}"
        )

        # Docs dir tisztítása
        if self.docs_dir.exists():
            import shutil

            shutil.rmtree(self.docs_dir)
        self.docs_dir.mkdir(parents=True, exist_ok=True)

        # Fájlok feldolgozása
        for source_dir in self.source_dirs:
            if not source_dir.exists():
                print(f"Figyelmeztetés: {source_dir} nem található, kihagyva.")
                continue

            # Root fájlok (main.py)
            if source_dir == Path("."):
                for file in source_dir.glob("*.py"):
                    if file.name not in self.ignored_files:
                        self.generate_documentation(file)
            else:
                # Rekurzív feldolgozás
                for file in source_dir.rglob("*.py"):
                    if any(part in self.ignored_dirs for part in file.parts):
                        continue
                    if file.name in self.ignored_files:
                        continue
                    self.generate_documentation(file)

        print(f"\n✅ Dokumentáció generálása kész! Kimeneti mappa: {self.docs_dir}")


def main() -> None:
    """Főprogram."""
    generator = DocumentationGenerator()
    generator.generate_all()


if __name__ == "__main__":
    main()
