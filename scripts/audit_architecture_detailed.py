#!/usr/bin/env python3
"""Részletes Architecture Audit Script.

Ellenőrzi:
1. DDD Réteg Hierarchia (alsó → felső TILOS)
2. Modul Struktúra (interfaces/, implementations/, exceptions/, factory.py)
3. DI Pattern (konstruktor injektálás)
4. Import Szabályok (abszolút kötelező)
5. Type Safety (Pydantic, Any TILOS)
6. Mirror Testing (tests/ struktúra)
"""

import ast
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Issue:
    """Audit probléma."""

    severity: str  # "CRITICAL" | "WARNING"
    category: str  # "DDD" | "DI" | "Import" | "Type" | "Mirror" | "Structure"
    file: str
    line: int
    message: str
    suggestion: str = ""


@dataclass
class ModuleAudit:
    """Modul audit eredmény."""

    path: str
    layer: str  # "Infrastructure" | "Input" | "Persistence" | "Domain" | "Presentation"
    issues: list[Issue] = field(default_factory=list)
    has_interfaces: bool = False
    has_implementations: bool = False
    has_exceptions: bool = False
    has_factory: bool = False


class ArchitectureAuditor:
    """Architecture Audit Engine."""

    # DDD Réteg Hierarchia (0 = legalsó, 4 = legfelső)
    LAYERS = {
        "core": ("Infrastructure", 0),
        "collectors": ("Input", 1),
        "data": ("Persistence", 2),
        "processors": ("Domain", 3),
        "ui": ("Presentation", 4),
    }

    def __init__(self, project_root: Path):
        """Initialize the architecture auditor."""
        self.project_root = project_root
        self.neural_ai = project_root / "neural_ai"
        self.tests = project_root / "tests"
        self.modules: list[ModuleAudit] = []
        self.issues: list[Issue] = []

    def run(self) -> None:
        """Audit futtatása."""
        print("🔍 Architecture Audit indítása...")
        print(f"📂 Projekt: {self.project_root}")
        print()

        # 1. Modul struktúra ellenőrzés
        self._audit_module_structure()

        # 2. Python fájlok elemzése
        py_files = list(self.neural_ai.rglob("*.py"))
        print(f"📄 {len(py_files)} Python fájl elemzése...")
        print()

        for py_file in py_files:
            self._audit_file(py_file)

        # 3. Mirror Testing ellenőrzés
        self._audit_mirror_testing()

        # 4. Riport generálás
        self._generate_report()

    def _audit_module_structure(self) -> None:
        """Modul struktúra ellenőrzés (DDD Atomic Unit)."""
        print("🏗️  Modul struktúra ellenőrzés...")

        for layer_dir in self.neural_ai.iterdir():
            if not layer_dir.is_dir() or layer_dir.name.startswith("__"):
                continue

            layer_name, _ = self.LAYERS.get(layer_dir.name, ("Unknown", -1))

            # Rekurzív modul keresés
            for module_dir in layer_dir.rglob("*"):
                if not module_dir.is_dir() or module_dir.name.startswith("__"):
                    continue

                # Ellenőrizzük, hogy ez egy "modul" (van factory.py vagy interfaces/)
                has_factory = (module_dir / "factory.py").exists()
                has_interfaces = (module_dir / "interfaces").is_dir()

                if not (has_factory or has_interfaces):
                    continue

                module_audit = ModuleAudit(
                    path=str(module_dir.relative_to(self.project_root)),
                    layer=layer_name,
                )

                # Atomic Unit ellenőrzés
                module_audit.has_interfaces = has_interfaces
                module_audit.has_implementations = (module_dir / "implementations").is_dir()
                module_audit.has_exceptions = (module_dir / "exceptions").is_dir()
                module_audit.has_factory = has_factory

                # Hiányzó komponensek
                if has_factory and not has_interfaces:
                    module_audit.issues.append(
                        Issue(
                            severity="CRITICAL",
                            category="Structure",
                            file=str(module_dir.relative_to(self.project_root)),
                            line=0,
                            message="Factory.py létezik, de hiányzik az interfaces/ mappa",
                            suggestion="Hozz létre interfaces/ mappát ABC osztályokkal",
                        )
                    )

                if has_interfaces and not module_audit.has_implementations:
                    module_audit.issues.append(
                        Issue(
                            severity="WARNING",
                            category="Structure",
                            file=str(module_dir.relative_to(self.project_root)),
                            line=0,
                            message="Interfaces/ létezik, de hiányzik az implementations/ mappa",
                            suggestion="Hozz létre implementations/ mappát konkrét osztályokkal",
                        )
                    )

                if has_factory and not module_audit.has_exceptions:
                    module_audit.issues.append(
                        Issue(
                            severity="WARNING",
                            category="Structure",
                            file=str(module_dir.relative_to(self.project_root)),
                            line=0,
                            message="Hiányzik az exceptions/ mappa",
                            suggestion="Hozz létre exceptions/ mappát típusos hibákkal",
                        )
                    )

                self.modules.append(module_audit)
                self.issues.extend(module_audit.issues)

        print(f"✅ {len(self.modules)} modul ellenőrizve")
        print()

    def _audit_file(self, file_path: Path) -> None:
        """Egyetlen Python fájl audit."""
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))
        except Exception as e:
            self.issues.append(
                Issue(
                    severity="CRITICAL",
                    category="Parse",
                    file=str(file_path.relative_to(self.project_root)),
                    line=0,
                    message=f"AST parse hiba: {e}",
                )
            )
            return

        rel_path = file_path.relative_to(self.project_root)

        # 1. Import ellenőrzés
        self._check_imports(tree, rel_path)

        # 2. DDD Réteg függőség ellenőrzés
        self._check_layer_dependencies(tree, rel_path)

        # 3. DI Pattern ellenőrzés
        self._check_di_pattern(tree, rel_path)

        # 4. Type Safety ellenőrzés
        self._check_type_safety(tree, rel_path)

        # 5. Export ellenőrzés (__init__.py)
        if file_path.name == "__init__.py":
            self._check_exports(tree, rel_path)

    def _check_imports(self, tree: ast.AST, rel_path: Path) -> None:
        """Import szabályok ellenőrzése."""
        for node in ast.walk(tree):
            # Relatív import TILOS
            if isinstance(node, ast.ImportFrom):
                if node.level > 0:  # Relatív import
                    self.issues.append(
                        Issue(
                            severity="CRITICAL",
                            category="Import",
                            file=str(rel_path),
                            line=node.lineno,
                            message=f"Relatív import: {'.' * node.level}{node.module or ''}",
                            suggestion="Használj abszolút importot: from neural_ai.X.Y import Z",
                        )
                    )

    def _is_lazy_import(self, node: ast.ImportFrom, tree: ast.AST) -> bool:
        """Ellenőrzi, hogy az import lazy import-e (függvényen belül van)."""
        # Keressük meg a node szülő kontextusát
        for parent in ast.walk(tree):
            if isinstance(parent, ast.FunctionDef):
                # Ellenőrizzük, hogy a node a függvény body-jában van-e
                for stmt in ast.walk(parent):
                    if stmt is node:
                        return True
        return False

    def _is_in_type_checking_block(self, node: ast.ImportFrom, tree: ast.AST) -> bool:
        """Ellenőrzi, hogy az import TYPE_CHECKING blokkon belül van-e."""
        # Keressük meg az If node-okat
        for parent in ast.walk(tree):
            if isinstance(parent, ast.If):
                # Ellenőrizzük, hogy a test TYPE_CHECKING-e
                if isinstance(parent.test, ast.Name) and parent.test.id == "TYPE_CHECKING":
                    # Ellenőrizzük, hogy a node a body-ban van-e
                    for stmt in ast.walk(parent):
                        if stmt is node:
                            return True
        return False

    def _check_layer_dependencies(self, tree: ast.AST, rel_path: Path) -> None:
        """DDD Réteg függőség ellenőrzés (alsó → felső TILOS)."""
        # Aktuális fájl rétege
        parts = rel_path.parts
        if len(parts) < 2 or parts[0] != "neural_ai":
            return

        current_layer_key = parts[1]
        if current_layer_key not in self.LAYERS:
            return

        current_layer_name, current_level = self.LAYERS[current_layer_key]

        # Importok ellenőrzése
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("neural_ai."):
                    # Lazy import ellenőrzés (factory.py-ban engedélyezett)
                    if self._is_lazy_import(node, tree) and "factory.py" in str(rel_path):
                        continue  # Lazy import factory-ban OK

                    # TYPE_CHECKING blokk ellenőrzés (mindig engedélyezett)
                    if self._is_in_type_checking_block(node, tree):
                        continue  # TYPE_CHECKING import OK

                    imported_parts = node.module.split(".")
                    if len(imported_parts) >= 2:
                        imported_layer_key = imported_parts[1]
                        if imported_layer_key in self.LAYERS:
                            imported_layer_name, imported_level = self.LAYERS[imported_layer_key]

                            # Alsó réteg NEM hivatkozhat felső rétegre
                            if current_level < imported_level:
                                self.issues.append(
                                    Issue(
                                        severity="CRITICAL",
                                        category="DDD",
                                        file=str(rel_path),
                                        line=node.lineno,
                                        message=f"DDD megsértés: {current_layer_name} ({current_level}) → {imported_layer_name} ({imported_level})",
                                        suggestion=f"Alsó réteg ({current_layer_name}) NEM hivatkozhat felső rétegre ({imported_layer_name}). Fordítsd meg a függőséget vagy használj Dependency Injection-t.",
                                    )
                                )

    def _check_di_pattern(self, tree: ast.AST, rel_path: Path) -> None:
        """DI Pattern ellenőrzés (konstruktor injektálás)."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Keressük az __init__ metódust
                init_method = None
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                        init_method = item
                        break

                if not init_method:
                    continue

                # Ellenőrizzük, hogy van-e Service Locator pattern (TILOS)
                for stmt in ast.walk(init_method):
                    if isinstance(stmt, ast.Call):
                        # Factory.get_X() hívás az __init__-ben (Service Locator)
                        if isinstance(stmt.func, ast.Attribute):
                            if stmt.func.attr.startswith("get_"):
                                self.issues.append(
                                    Issue(
                                        severity="CRITICAL",
                                        category="DI",
                                        file=str(rel_path),
                                        line=stmt.lineno,
                                        message=f"Service Locator pattern: {node.name}.__init__ hívja a Factory.{stmt.func.attr}() metódust",
                                        suggestion="Használj konstruktor injektálást: adj át logger/config paramétereket az __init__-nek",
                                    )
                                )

    def _check_type_safety(self, tree: ast.AST, rel_path: Path) -> None:
        """Type Safety ellenőrzés (Any TILOS, Pydantic kötelező config-nál)."""
        # 1. Any típus használat
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == "Any":
                self.issues.append(
                    Issue(
                        severity="CRITICAL",
                        category="Type",
                        file=str(rel_path),
                        line=node.lineno,
                        message="Any típus használat (TILOS)",
                        suggestion="Használj konkrét típust vagy Union[X, Y] típust",
                    )
                )

        # 2. TypedDict config használat (ELAVULT)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == "TypedDict":
                        # Ellenőrizzük, hogy config-hoz kapcsolódik-e
                        if "config" in node.name.lower():
                            self.issues.append(
                                Issue(
                                    severity="CRITICAL",
                                    category="Type",
                                    file=str(rel_path),
                                    line=node.lineno,
                                    message=f"TypedDict használat config-nál: {node.name} (ELAVULT)",
                                    suggestion="Használj Pydantic BaseModel-t: class XConfig(BaseModel): ...",
                                )
                            )

    def _check_exports(self, tree: ast.AST, rel_path: Path) -> None:
        """Export ellenőrzés (__init__.py fájlokban)."""
        # Implementáció exportálás TILOS (csak Interface + Factory)
        if "implementations" in str(rel_path):
            # implementations/__init__.py ÜRES kell legyen
            for node in ast.walk(tree):
                if isinstance(node, (ast.ImportFrom, ast.Import)):
                    self.issues.append(
                        Issue(
                            severity="CRITICAL",
                            category="Structure",
                            file=str(rel_path),
                            line=node.lineno,
                            message="implementations/__init__.py NEM lehet üres! Implementáció exportálás TILOS",
                            suggestion="Töröld az összes importot ebből a fájlból. Csak a factory.py importálhatja az implementációkat.",
                        )
                    )

    def _audit_mirror_testing(self) -> None:
        """Mirror Testing ellenőrzés."""
        print("🧪 Mirror Testing ellenőrzés...")

        py_files = list(self.neural_ai.rglob("*.py"))
        missing_tests = []

        for py_file in py_files:
            # Kihagyjuk a __init__.py és test fájlokat
            if py_file.name == "__init__.py" or py_file.name.startswith("test_"):
                continue

            # Várható teszt fájl
            rel_path = py_file.relative_to(self.neural_ai)
            test_path = self.tests / "neural_ai" / rel_path.parent / f"test_{py_file.name}"

            if not test_path.exists():
                missing_tests.append(str(rel_path))
                self.issues.append(
                    Issue(
                        severity="WARNING",
                        category="Mirror",
                        file=str(rel_path),
                        line=0,
                        message=f"Hiányzó teszt fájl: {test_path.relative_to(self.project_root)}",
                        suggestion=f"Hozz létre: {test_path.relative_to(self.project_root)}",
                    )
                )

        print(f"⚠️  {len(missing_tests)} hiányzó teszt fájl")
        print()

    def _generate_report(self) -> None:
        """Riport generálás."""
        output_path = self.project_root / "docs" / "development" / "ARCHITECTURE_AUDIT_DETAILED.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Csoportosítás
        critical = [i for i in self.issues if i.severity == "CRITICAL"]
        warnings = [i for i in self.issues if i.severity == "WARNING"]

        # Kategória szerinti csoportosítás
        by_category = {}
        for issue in self.issues:
            by_category.setdefault(issue.category, []).append(issue)

        # Réteg szerinti csoportosítás
        by_layer = {}
        for issue in self.issues:
            layer = self._get_layer_from_path(issue.file)
            by_layer.setdefault(layer, []).append(issue)

        # Riport írás
        with output_path.open("w", encoding="utf-8") as f:
            f.write("# 🔍 ARCHITECTURE AUDIT REPORT (DETAILED)\n\n")
            f.write(f"**Generálva:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("**Elemző**: Roo Code (Code-New)\n")
            f.write(f"**Szkennelt fájlok:** {len(list(self.neural_ai.rglob('*.py')))}\n")
            f.write(f"**Modulok:** {len(self.modules)}\n\n")

            # Executive Summary
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- 🔴 **Kritikus problémák:** {len(critical)}\n")
            for cat, issues in by_category.items():
                crit = [i for i in issues if i.severity == "CRITICAL"]
                if crit:
                    f.write(f"  - {cat}: {len(crit)}\n")
            f.write(f"- 🟡 **Figyelmeztetések:** {len(warnings)}\n")
            for cat, issues in by_category.items():
                warn = [i for i in issues if i.severity == "WARNING"]
                if warn:
                    f.write(f"  - {cat}: {len(warn)}\n")
            f.write("\n")

            # Kritikus problémák rétegek szerint
            f.write("## 🔴 Kritikus Problémák (Rétegek szerint)\n\n")
            for layer in ["Infrastructure", "Input", "Persistence", "Domain", "Presentation"]:
                layer_issues = [i for i in by_layer.get(layer, []) if i.severity == "CRITICAL"]
                if not layer_issues:
                    continue

                f.write(f"### {layer} Layer\n\n")

                # Kategória szerint csoportosítás
                layer_by_cat = {}
                for issue in layer_issues:
                    layer_by_cat.setdefault(issue.category, []).append(issue)

                for cat, issues in layer_by_cat.items():
                    f.write(f"#### {cat} Problémák ({len(issues)} db)\n\n")
                    for issue in issues[:10]:  # Max 10 példa
                        f.write(f"**[`{issue.file}`]({issue.file}:{issue.line})**\n")
                        f.write(f"- **Probléma:** {issue.message}\n")
                        if issue.suggestion:
                            f.write(f"- **Javaslat:** {issue.suggestion}\n")
                        f.write("\n")

                    if len(issues) > 10:
                        f.write(f"*...és még {len(issues) - 10} hasonló probléma*\n\n")

            # Figyelmeztetések
            f.write("## 🟡 Figyelmeztetések\n\n")
            for cat, issues in by_category.items():
                warn = [i for i in issues if i.severity == "WARNING"]
                if not warn:
                    continue

                f.write(f"### {cat} ({len(warn)} db)\n\n")
                for issue in warn[:5]:  # Max 5 példa
                    f.write(f"- [`{issue.file}`]({issue.file}:{issue.line}): {issue.message}\n")

                if len(warn) > 5:
                    f.write(f"- *...és még {len(warn) - 5} hasonló figyelmeztetés*\n")
                f.write("\n")

            # Prioritizált javítási terv
            f.write("## 📋 Prioritizált Javítási Terv\n\n")
            f.write("### Fázis 1: Kritikus (1-3 nap)\n\n")

            # DDD megsértések
            ddd_critical = [i for i in critical if i.category == "DDD"]
            if ddd_critical:
                f.write(f"1. **DDD Réteg Függőségek** ({len(ddd_critical)} db)\n")
                f.write("   - Alsó rétegek felső rétegekre való hivatkozásainak megszüntetése\n")
                f.write("   - Dependency Injection bevezetése\n\n")

            # DI problémák
            di_critical = [i for i in critical if i.category == "DI"]
            if di_critical:
                f.write(f"2. **Dependency Injection** ({len(di_critical)} db)\n")
                f.write("   - Service Locator pattern cseréje konstruktor injektálásra\n")
                f.write("   - Factory pattern helyes használata\n\n")

            # Import problémák
            import_critical = [i for i in critical if i.category == "Import"]
            if import_critical:
                f.write(f"3. **Import Szabályok** ({len(import_critical)} db)\n")
                f.write("   - Relatív importok cseréje abszolút importokra\n")
                f.write("   - TYPE_CHECKING használata körkörös importoknál\n\n")

            f.write("### Fázis 2: Magas (3-7 nap)\n\n")

            # Type Safety
            type_critical = [i for i in critical if i.category == "Type"]
            if type_critical:
                f.write(f"1. **Type Safety** ({len(type_critical)} db)\n")
                f.write("   - Any típus eliminálása\n")
                f.write("   - TypedDict → Pydantic migráció\n\n")

            # Struktúra
            struct_critical = [i for i in critical if i.category == "Structure"]
            if struct_critical:
                f.write(f"2. **Modul Struktúra** ({len(struct_critical)} db)\n")
                f.write("   - Hiányzó interfaces/, implementations/, exceptions/ mappák létrehozása\n")
                f.write("   - Implementáció exportok megszüntetése\n\n")

            f.write("### Fázis 3: Közepes (1-2 hét)\n\n")

            # Mirror Testing
            mirror_warnings = [i for i in warnings if i.category == "Mirror"]
            if mirror_warnings:
                f.write(f"1. **Mirror Testing** ({len(mirror_warnings)} db)\n")
                f.write("   - Hiányzó teszt fájlok létrehozása\n")
                f.write("   - 100% lefedettség elérése Domain rétegben\n\n")

            # Metrikák
            f.write("## 📈 Metrikák\n\n")
            f.write("| Réteg | Fájlok | Kritikus | Figyelmeztetés | Megfelelőség |\n")
            f.write("|:------|:-------|:---------|:---------------|:-------------|\n")

            for layer in ["Infrastructure", "Input", "Persistence", "Domain", "Presentation"]:
                layer_files = len([f for f in self.neural_ai.rglob("*.py") if self._get_layer_from_path(str(f.relative_to(self.project_root))) == layer])
                layer_critical = len([i for i in by_layer.get(layer, []) if i.severity == "CRITICAL"])
                layer_warnings = len([i for i in by_layer.get(layer, []) if i.severity == "WARNING"])
                total_issues = layer_critical + layer_warnings
                compliance = max(0, 100 - (total_issues / max(layer_files, 1) * 100))
                f.write(f"| {layer} | {layer_files} | {layer_critical} | {layer_warnings} | {compliance:.1f}% |\n")

            f.write("\n")
            f.write("---\n\n")
            f.write("**Következő lépés:** Fázis 1 implementálása (DDD, DI, Import javítások)\n")

        print(f"✅ Riport generálva: {output_path}")
        print()
        print("📊 Összefoglaló:")
        print(f"   🔴 Kritikus: {len(critical)}")
        print(f"   🟡 Figyelmeztetés: {len(warnings)}")
        print(f"   📄 Riport: {output_path}")

    def _get_layer_from_path(self, path: str) -> str:
        """Réteg meghatározása fájl útvonalból."""
        parts = Path(path).parts
        if len(parts) >= 2 and parts[0] == "neural_ai":
            layer_key = parts[1]
            return self.LAYERS.get(layer_key, ("Unknown", -1))[0]
        return "Unknown"


def main() -> None:
    """Főprogram."""
    project_root = Path(__file__).parent.parent
    auditor = ArchitectureAuditor(project_root)
    auditor.run()


if __name__ == "__main__":
    main()
