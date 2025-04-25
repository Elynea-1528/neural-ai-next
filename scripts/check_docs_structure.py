#!/usr/bin/env python3
"""Dokumentációs struktúra ellenőrzése.

Ez a script ellenőrzi, hogy a dokumentáció megfelel-e az előírt struktúrának:
- Megfelelő könyvtárszerkezet
- Kötelező fájlok megléte
- Fájlok formátuma és tartalma
"""

import logging
from pathlib import Path

import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


REQUIRED_COMPONENT_FILES = {
    "README.md": "Áttekintés és használati útmutató",
    "api.md": "API dokumentáció",
    "architecture.md": "Architektúra leírás",
    "design_spec.md": "Tervezési specifikáció",
    "development_checklist.md": "Fejlesztési checklist",
    "examples.md": "Használati példák",
    "CHANGELOG.md": "Változások követése",
}


def check_component_structure(component_path: Path) -> bool:
    """Ellenőrzi egy komponens dokumentációs struktúráját.

    Args:
        component_path: A komponens könyvtárának útvonala

    Returns:
        True ha a struktúra megfelelő, False ha nem
    """
    missing_files = []

    for required_file, description in REQUIRED_COMPONENT_FILES.items():
        if not (component_path / required_file).exists():
            missing_files.append(f"{required_file} ({description})")

    if missing_files:
        logger.error(f"Missing files in {component_path}:")
        for file in missing_files:
            logger.error(f"  - {file}")
        return False

    return True


def check_markdown_frontmatter(file_path: Path) -> bool:
    """Ellenőrzi egy markdown fájl frontmatter blokkját.

    Args:
        file_path: A markdown fájl útvonala

    Returns:
        True ha a frontmatter érvényes, False ha nem
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Frontmatter blokk keresése
        if not content.startswith("---\n"):
            return True  # Nem kötelező a frontmatter

        # Frontmatter parse-olása
        frontmatter_end = content.find("\n---\n", 4)
        if frontmatter_end == -1:
            logger.error(f"Invalid frontmatter format in {file_path}")
            return False

        frontmatter = content[4:frontmatter_end]
        yaml.safe_load(frontmatter)
        return True

    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in frontmatter of {file_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error checking frontmatter in {file_path}: {e}")
        return False


def check_markdown_headers(file_path: Path) -> bool:
    """Ellenőrzi egy markdown fájl fejléc hierarchiáját.

    Args:
        file_path: A markdown fájl útvonala

    Returns:
        True ha a fejlécek helyesek, False ha nem
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # H1 fejléc ellenőrzése
        h1_headers = [line for line in lines if line.startswith("# ")]
        if len(h1_headers) != 1:
            logger.error(f"Expected exactly one H1 header in {file_path}")
            return False

        # Fejléc hierarchia ellenőrzése
        current_level = 1
        for line in lines:
            if line.startswith("#"):
                level = len(line.split()[0])
                if level > current_level + 1:
                    logger.error(
                        f"Invalid header hierarchy in {file_path}: "
                        f"H{current_level} followed by H{level}"
                    )
                    return False
                current_level = level

        return True

    except Exception as e:
        logger.error(f"Error checking headers in {file_path}: {e}")
        return False


def check_all_components() -> bool:
    """Az összes komponens dokumentációjának ellenőrzése.

    Returns:
        True ha minden komponens dokumentációja helyes, False ha nem
    """
    components_dir = Path("docs/components")
    if not components_dir.exists():
        logger.error("Components directory not found")
        return False

    all_valid = True

    for component_dir in components_dir.iterdir():
        if not component_dir.is_dir():
            continue

        logger.info(f"Checking component: {component_dir.name}")

        # Komponens struktúra ellenőrzése
        if not check_component_structure(component_dir):
            all_valid = False
            continue

        # Markdown fájlok ellenőrzése
        for md_file in component_dir.glob("*.md"):
            if not check_markdown_frontmatter(md_file):
                all_valid = False
            if not check_markdown_headers(md_file):
                all_valid = False

    return all_valid


def main() -> None:
    """A script fő függvénye."""
    logger.info("Starting documentation structure check...")

    if check_all_components():
        logger.info("Documentation structure is valid!")
        exit(0)
    else:
        logger.error("Found documentation structure issues!")
        exit(1)


if __name__ == "__main__":
    main()
