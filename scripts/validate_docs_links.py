#!/usr/bin/env python3
"""Dokumentáció linkek validálása.

Ez a script ellenőrzi a dokumentációkban található linkeket:
- Relatív linkek érvényességét
- Belső kereszthivatkozásokat
- Külső linkek elérhetőségét (opcionális)
"""

import logging
import re
from pathlib import Path
from typing import List, Set, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_markdown_files() -> List[Path]:
    """Megkeresi az összes markdown fájlt a docs könyvtárban."""
    return list(Path("docs").rglob("*.md"))


def extract_links(file_path: Path) -> List[Tuple[str, int]]:
    """Kigyűjti a linkeket egy markdown fájlból.

    Args:
        file_path: A markdown fájl útvonala

    Returns:
        Lista a talált linkekről és azok sorszámáról
    """
    links = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            # Markdown linkek: [szöveg](link)
            md_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", line)
            for _, link in md_links:
                links.append((link, line_num))

            # HTML linkek: <a href="link">
            html_links = re.findall(r'<a\s+href=[\'"]([^\'"]+)[\'"]', line)
            for link in html_links:
                links.append((link, line_num))

    return links


def validate_internal_link(link: str, base_path: Path) -> bool:
    """Ellenőrzi egy belső link érvényességét.

    Args:
        link: A vizsgálandó link
        base_path: Az aktuális fájl könyvtára

    Returns:
        True ha a link érvényes, False ha nem
    """
    # Fragment linkek (#section) átugrása
    if link.startswith("#"):
        return True

    # Relatív útvonal feloldása
    target_path = (base_path / link).resolve()
    return target_path.exists()


def validate_all_links() -> bool:
    """Az összes dokumentációs link validálása.

    Returns:
        True ha minden link érvényes, False ha van érvénytelen
    """
    all_valid = True
    checked_links: Set[str] = set()

    markdown_files = find_markdown_files()

    for md_file in markdown_files:
        logger.info(f"Checking links in {md_file}")
        base_path = md_file.parent

        for link, line_num in extract_links(md_file):
            if link in checked_links:
                continue

            checked_links.add(link)

            # Külső linkek átugrása
            if link.startswith(("http://", "https://")):
                continue

            if not validate_internal_link(link, base_path):
                logger.error(f"Invalid link in {md_file}:{line_num}: {link}")
                all_valid = False

    return all_valid


def main() -> None:
    """A script fő függvénye."""
    logger.info("Starting documentation link validation...")

    if validate_all_links():
        logger.info("All links are valid!")
        exit(0)
    else:
        logger.error("Found invalid links!")
        exit(1)


if __name__ == "__main__":
    main()
