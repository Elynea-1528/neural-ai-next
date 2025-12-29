#!/usr/bin/env python3
"""Dokumentáció generátor script a Neural AI Next projekthez.

Ez a script rekurzívan bejárja a neural_ai mappát, elemzi a Python fájlokat
AST segítségével, kinyeri a docstring-eket, és létrehozza a tükör dokumentációt
a docs/components/ mappában.
"""

import ast
import os
from pathlib import Path


class DocstringExtractor(ast.NodeVisitor):
    """AST visitor a docstring-ek kinyeréséhez."""

    def __init__(self) -> None:
        """Inicializálja a kinyerőt."""
        self.classes: dict[str, str] = {}
        self.functions: dict[str, str] = {}
        self.module_docstring: str | None = None

    def visit_Module(self, node: ast.Module) -> None:
        """Modul docstring-jének kinyerése."""
        if node.body and isinstance(node.body[0], ast.Expr):
            docstring_node = node.body[0].value
            if isinstance(docstring_node, ast.Constant) and isinstance(docstring_node.value, str):
                self.module_docstring = docstring_node.value.strip()
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Osztály docstring-jének kinyerése."""
        docstring = None
        if node.body and isinstance(node.body[0], ast.Expr):
            docstring_node = node.body[0].value
            if isinstance(docstring_node, ast.Constant) and isinstance(docstring_node.value, str):
                docstring = docstring_node.value.strip()

        self.classes[node.name] = docstring or "Nincs docstring."
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Függvény docstring-jének kinyerése."""
        docstring = None
        if node.body and isinstance(node.body[0], ast.Expr):
            docstring_node = node.body[0].value
            if isinstance(docstring_node, ast.Constant) and isinstance(docstring_node.value, str):
                docstring = docstring_node.value.strip()

        self.functions[node.name] = docstring or "Nincs docstring."
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Aszinkron függvény docstring-jének kinyerése."""
        docstring = None
        if node.body and isinstance(node.body[0], ast.Expr):
            docstring_node = node.body[0].value
            if isinstance(docstring_node, ast.Constant) and isinstance(docstring_node.value, str):
                docstring = docstring_node.value.strip()

        self.functions[node.name] = docstring or "Nincs docstring."
        self.generic_visit(node)


class DocumentationGenerator:
    """Dokumentáció generátor osztály."""

    def __init__(self, source_dir: str = "neural_ai", docs_dir: str = "docs/components") -> None:
        """Inicializálja a dokumentáció generátort.

        Args:
            source_dir: A forráskód mappa elérési útja.
            docs_dir: A dokumentáció mappa elérési útja.
        """
        self.source_dir = Path(source_dir)
        self.docs_dir = Path(docs_dir)
        self.ignored_dirs = {"__pycache__", ".pytest_cache", ".ruff_cache", ".git"}
        self.ignored_files = {"__init__.py"}

    def extract_docstrings(self, file_path: Path) -> DocstringExtractor:
        """Kinyeri a docstring-eket egy Python fájlból.

        Args:
            file_path: A Python fájl elérési útja.

        Returns:
            A kinyert docstring-ekkel feltöltött DocstringExtractor objektum.
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            extractor = DocstringExtractor()
            extractor.visit(tree)
            return extractor

        except (SyntaxError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Hiba a(z) {file_path} fájl elemzésekor: {e}")
            return DocstringExtractor()

    def generate_markdown(self, file_path: Path, extractor: DocstringExtractor) -> str:
        """Generálja a Markdown dokumentációt egy fájlhoz.

        Args:
            file_path: A forrásfájl elérési útja.
            extractor: A docstring kinyerő objektum.

        Returns:
            A generált Markdown tartalom.
        """
        relative_path = file_path.relative_to(self.source_dir)
        title = f"# {relative_path}"

        # Modul docstring
        module_doc = f"\n{extractor.module_docstring or 'Nincs modul docstring.'}\n"

        # Osztályok szekciója
        classes_section = ""
        if extractor.classes:
            classes_section = "\n## Osztályok\n\n"
            for class_name, docstring in extractor.classes.items():
                classes_section += f"### `{class_name}`\n\n"
                classes_section += f"{docstring}\n\n"

        # Függvények szekciója
        functions_section = ""
        if extractor.functions:
            functions_section = "\n## Függvények\n\n"
            for func_name, docstring in extractor.functions.items():
                functions_section += f"### `{func_name}`\n\n"
                functions_section += f"{docstring}\n\n"

        # Forráskód referencia
        source_link = f"\n---\n\n**Forrásfájl:** [`{relative_path}`](../../../{file_path})\n"

        return f"{title}\n{module_doc}{classes_section}{functions_section}{source_link}"

    def generate_directory_index(self, directory: Path, files: list[Path]) -> str:
        """Generál egy index.md fájlt egy könyvtárhoz.

        Args:
            directory: A könyvtár elérési útja.
            files: A könyvtárban található dokumentált fájlok listája.

        Returns:
            Az index Markdown tartalma.
        """
        relative_dir = directory.relative_to(self.source_dir)
        title = f"# {relative_dir} - Komponens dokumentáció\n"

        intro = f"\nEz a mappa a(z) `neural_ai{os.sep}{relative_dir}` modul dokumentációját tartalmazza.\n\n"

        files_section = "## Fájlok\n\n"
        for file in sorted(files):
            rel_file = file.relative_to(self.source_dir)
            doc_file = rel_file.with_suffix(".md")
            files_section += f"- [`{rel_file}`](./{doc_file})\n"

        return f"{title}{intro}{files_section}\n"

    def process_directory(self, directory: Path) -> None:
        """Feldolgoz egy könyvtárat és generálja a dokumentációt.

        Args:
            directory: A feldolgozandó könyvtár.
        """
        documented_files: list[Path] = []

        for item in directory.rglob("*.py"):
            if any(part in self.ignored_dirs for part in item.parts):
                continue

            if item.name in self.ignored_files:
                continue

            print(f"Feldolgozás: {item}")

            extractor = self.extract_docstrings(item)
            markdown_content = self.generate_markdown(item, extractor)

            # Tükör útvonal létrehozása
            relative_path = item.relative_to(self.source_dir)
            doc_path = self.docs_dir / relative_path.with_suffix(".md")
            doc_path.parent.mkdir(parents=True, exist_ok=True)

            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            documented_files.append(item)

        # Index fájl generálása minden alkönyvtárhoz
        for subdir in [d for d in directory.rglob("*") if d.is_dir()]:
            if any(part in self.ignored_dirs for part in subdir.parts):
                continue

            subdir_files: list[Path] = [f for f in documented_files if f.parent == subdir]
            if subdir_files:
                relative_subdir = subdir.relative_to(self.source_dir)
                index_path = self.docs_dir / relative_subdir / "index.md"
                index_path.parent.mkdir(parents=True, exist_ok=True)

                index_content = self.generate_directory_index(subdir, subdir_files)
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(index_content)

    def generate_all_documentation(self) -> None:
        """Generálja az összes dokumentációt a forráskódból."""
        print(f"Dokumentáció generálása: {self.source_dir} -> {self.docs_dir}")

        if not self.source_dir.exists():
            raise FileNotFoundError(f"A forrásmappa nem található: {self.source_dir}")

        # A docs_dir törlése és újra létrehozása a tiszta generáláshoz
        if self.docs_dir.exists():
            import shutil

            shutil.rmtree(self.docs_dir)
        self.docs_dir.mkdir(parents=True, exist_ok=True)

        # Rekurzív feldolgozás
        self.process_directory(self.source_dir)

        print(f"\n✅ Dokumentáció generálása kész! Kimeneti mappa: {self.docs_dir}")


def main() -> None:
    """Főprogram a dokumentáció generálásához."""
    generator = DocumentationGenerator()
    generator.generate_all_documentation()


if __name__ == "__main__":
    main()
