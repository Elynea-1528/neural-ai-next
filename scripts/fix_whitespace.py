#!/usr/bin/env python3
"""Whitespace javító script.

- Sorvégi whitespace-ek eltávolítása
- Üres sorok whitespace karaktereinek eltávolítása
- Fájl végi üres sor biztosítása
"""

import sys
from pathlib import Path


def fix_whitespace(file_path: Path) -> None:
    """Whitespace-ek javítása egy fájlban.

    Args:
        file_path: A javítandó fájl útvonala
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Sorvégi whitespace-ek és üres sorok javítása
    fixed_lines = [line.rstrip() + "\n" for line in lines]

    # Üres sorok whitespace-ek nélkül
    fixed_lines = ["" + "\n" if line.strip() == "" else line for line in fixed_lines]

    # Fájl végi üres sor biztosítása
    if fixed_lines and not fixed_lines[-1].endswith("\n"):
        fixed_lines[-1] += "\n"
    if not fixed_lines or fixed_lines[-1] != "\n":
        fixed_lines.append("\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)


def main() -> None:
    """A script fő függvénye."""
    if len(sys.argv) < 2:
        print("Usage: fix_whitespace.py <file1> [file2 ...]")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        path = Path(file_path)
        if path.exists():
            print(f"Fixing whitespace in {path}")
            fix_whitespace(path)
        else:
            print(f"File not found: {path}")


if __name__ == "__main__":
    main()
