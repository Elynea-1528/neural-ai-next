#!/usr/bin/env python3
"""Fixture Scope Deprecation Warning Fix Script.

Automatikusan javítja az implicit fixture scope warningokat a tests/ mappában.
Pytest 8.0+ verziótól kötelező explicit scope megadás.

Usage:
    python scripts/fix_fixture_scope.py [--dry-run] [--verbose]
"""

import re
import sys
from pathlib import Path


def fix_fixture_scope(
    file_path: Path, dry_run: bool = False, verbose: bool = False
) -> tuple[bool, int]:
    """Javítja az implicit fixture scope-ot egy fájlban.

    Args:
        file_path: Teszt fájl útvonal
        dry_run: Ha True, csak szimulálja a változtatásokat
        verbose: Ha True, részletes kimenet

    Returns:
        Tuple (módosítva volt-e, javítások száma)
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        # Regex pattern: @pytest.fixture (scope nélkül)
        # Matches:
        #   @pytest.fixture
        #   @pytest.fixture()
        # Does NOT match:
        #   @pytest.fixture(scope=...)
        #   @pytest.fixture(autouse=True, scope=...)
        pattern = re.compile(
            r'^(\s*)@pytest\.fixture(\(\s*\))?\s*$',
            re.MULTILINE
        )

        def replacement(match: re.Match[str]) -> str:
            """Replacement függvény: scope="function" hozzáadása."""
            indent = match.group(1)
            return f'{indent}@pytest.fixture(scope="function")'

        # Pattern alkalmazása
        modified_content = pattern.sub(replacement, content)
        fixes_count = len(pattern.findall(content))

        if modified_content == original_content:
            return False, 0

        if not dry_run:
            file_path.write_text(modified_content, encoding="utf-8")
            if verbose:
                print(f"✅ {file_path}: {fixes_count} fixture javítva")
        else:
            if verbose:
                print(f"🔍 [DRY-RUN] {file_path}: {fixes_count} fixture javítható")

        return True, fixes_count

    except Exception as e:
        print(f"❌ HIBA: {file_path}: {e}", file=sys.stderr)
        return False, 0


def find_test_files(base_path: Path) -> list[Path]:
    """Teszt fájlok keresése a tests/ mappában.

    Args:
        base_path: Projekt root útvonal

    Returns:
        Teszt fájlok listája
    """
    tests_dir = base_path / "tests"
    if not tests_dir.exists():
        raise FileNotFoundError(f"tests/ mappa nem található: {tests_dir}")

    return sorted(tests_dir.rglob("*.py"))


def main() -> int:
    """Fő végrehajtási logika."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Fixture scope deprecation warning fix script"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Szimulálja a változtatásokat (nem ír fájlokat)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Részletes kimenet"
    )
    args = parser.parse_args()

    # Projekt root detektálás
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent

    print(f"🔍 Teszt fájlok keresése: {project_root / 'tests'}")

    try:
        test_files = find_test_files(project_root)
        print(f"📋 {len(test_files)} teszt fájl található")

        if args.dry_run:
            print("⚠️  DRY-RUN MÓD - Nem módosít fájlokat")

        total_files_modified = 0
        total_fixtures_fixed = 0

        for test_file in test_files:
            modified, fixes = fix_fixture_scope(
                test_file,
                dry_run=args.dry_run,
                verbose=args.verbose
            )
            if modified:
                total_files_modified += 1
                total_fixtures_fixed += fixes

        print()
        print("=" * 60)
        print("✅ Kész!")
        print(f"   Módosított fájlok: {total_files_modified}")
        print(f"   Javított fixturek: {total_fixtures_fixed}")
        print("=" * 60)

        if args.dry_run:
            print()
            print("💡 Élesítéshez futtasd újra --dry-run nélkül:")
            print("   python scripts/fix_fixture_scope.py")

        return 0

    except Exception as e:
        print(f"❌ KRITIKUS HIBA: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
