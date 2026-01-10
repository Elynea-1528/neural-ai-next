#!/usr/bin/env python3
"""Archiváló szkript a projekt fő fájljainak tömörítéséhez.

Az alábbi fájlokat és mappákat tömöríti:
- neural_ai/ mappa
- docs/ mappa
- main.py
- pyproject.toml
- .vscode/settings.json
- environment.yml
- .env.example
- README.md

Formátum: ZIP (alapértelmezett) vagy RAR
A kimeneti fájl a ~/Dokumentumok mappába kerül mentésre.
"""

import os
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path


def create_zip_archive(output_path: str, files_to_archive: list) -> None:
    """ZIP archívum létrehozása."""
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_archive:
            if os.path.exists(file_path):
                if os.path.isdir(file_path):
                    # Mappa esetén rekurzív hozzáadás
                    for root, dirs, files in os.walk(file_path):
                        for file in files:
                            file_to_add = os.path.join(root, file)
                            arcname = os.path.relpath(file_to_add, start=".")
                            zipf.write(file_to_add, arcname)
                            print(f"✓ Hozzáadva: {arcname}")
                else:
                    # Fájl esetén közvetlen hozzáadás
                    arcname = (
                        os.path.basename(file_path) if file_path.startswith(".") else file_path
                    )
                    if file_path.startswith("."):
                        arcname = file_path.replace("./", "", 1)
                    zipf.write(file_path, arcname)
                    print(f"✓ Hozzáadva: {file_path}")
            else:
                print(f"⚠ Figyelmeztetés: {file_path} nem található, kihagyva")


def create_rar_archive(output_path: str, files_to_archive: list) -> None:
    """RAR archívum létrehozása (ha a rar parancs elérhető)."""
    # Ellenőrizzük, hogy a rar parancs elérhető-e
    if not shutil.which("rar"):
        raise RuntimeError(
            "A 'rar' parancs nem található. Telepítsd a következővel: sudo apt-get install rar"
        )

    # RAR parancs összeállítása
    rar_cmd = ["rar", "a", "-r", output_path]
    rar_cmd.extend(files_to_archive)

    # RAR archívum létrehozása
    result = os.system(" ".join(rar_cmd))
    if result != 0:
        raise RuntimeError(f"RAR archívum létrehozása sikertelen (visszatérési kód: {result})")

    for file_path in files_to_archive:
        if os.path.exists(file_path):
            print(f"✓ Hozzáadva: {file_path}")


def main() -> None:
    """Fő végrehajtási függvény."""
    # Archiválandó fájlok és mappák listája
    files_to_archive = [
        "neural_ai/",
        # "docs/",
        "configs/",
        # "logs/",
        # "tests/",
        "scripts/",
        "external/jforex-bridge/src/main/java/com/neuralai/bridge/NeuralBridgeStrategy.java",
        "main.py",
        "README.md",
        "pyproject.toml",
        ".vscode/settings.json",
        ".env",
        ".env.example",
        ".pre-commit-config.yaml",
    ]

    # Ellenőrizzük, hogy a fájlok léteznek-e
    missing_files = [f for f in files_to_archive if not os.path.exists(f)]
    if missing_files:
        print("⚠ Figyelmeztetés: A következő fájlok nem találhatók:")
        for f in missing_files:
            print(f"  - {f}")
        print()

    # Dátum alapú archívum név
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Alapértelmezett beállítások
    archive_format = "zip"
    output_name = f"neural-ai-next_backup_{timestamp}"

    # Parancssori argumentumok feldolgozása
    if len(sys.argv) > 1:
        if sys.argv[1] in ["zip", "rar"]:
            archive_format = sys.argv[1]
        else:
            print("Használat: python scripts/archive_project.py [zip|rar]")
            print("Alapértelmezett: zip formátum")
            sys.exit(1)

    # Kimeneti útvonal a Dokumentumok mappába
    documents_dir = Path.home() / "Dokumentumok"
    documents_dir.mkdir(exist_ok=True)  # Létrehozza ha nem létezik
    output_path = str(documents_dir / f"{output_name}.{archive_format}")

    print(f"\n{'=' * 60}")
    print(f"📦 Projekt archiválás: {archive_format.upper()} formátum")
    print(f"{'=' * 60}\n")

    try:
        if archive_format == "zip":
            create_zip_archive(output_path, files_to_archive)
        elif archive_format == "rar":
            create_rar_archive(output_path, files_to_archive)

        print(f"\n{'=' * 60}")
        print("✅ Archiválás sikeres!")
        print(f"📁 Kimeneti fájl: {output_path}")
        print(f"📍 Elérési út: {os.path.abspath(output_path)}")
        print(f"{'=' * 60}\n")

    except Exception as e:
        print(f"\n❌ Hiba történt az archiválás során: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
