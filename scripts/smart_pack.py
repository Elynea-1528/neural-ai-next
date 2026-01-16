#!/usr/bin/env python3
"""Smart Context Packer & Drive Sync.

Ez a szkript összegyűjti a projekt releváns forráskódjait egyetlen
Markdown/Text fájlba a LLM kontextus számára, és automatikusan
szinkronizálja a Google Drive-ra (Linux GVFS támogatással).
"""

import argparse
import os
import subprocess
import time
from pathlib import Path

# ==========================================
# ⚙️ KONFIGURÁCIÓ
# ==========================================

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
OUTPUT_FILENAME_TXT = "neural_ai_full_context.txt"
OUTPUT_FILE_TXT = PROJECT_ROOT / OUTPUT_FILENAME_TXT
OUTPUT_FILENAME_MD = "neural_ai_full_context.md"
OUTPUT_FILE_MD = PROJECT_ROOT / OUTPUT_FILENAME_MD

# Google Drive mappa neve
DRIVE_SUBFOLDER = "Google AI Studio"

# Mit vegyünk bele (Full mód)
INCLUDE_DIRS = ["neural_ai", "scripts", "configs", "docs", "external", "tests"]
INCLUDE_FILES = ["pyproject.toml", "main.py", "README.md", ".gitignore", ".vscode/settings.json"]

# Mit hagyjunk ki (Zajszűrés)
IGNORE_EXTENSIONS: set[str] = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".parquet",
    ".csv",
    ".db",
    ".sqlite",
    ".h5",
    ".pt",
    ".pth",
    ".png",
    ".jpg",
    ".zip",
    ".jar",
    ".class",
    ".lock",
    ".DS_Store",
    ".txt",
    ".log",
}

IGNORE_DIRS: set[str] = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".git",
    "venv",
    "env",
    "data",
    "logs",
    "htmlcov",
    "build",
    ".gradle",
    "gradle",
    "node_modules",
    "docs/components",  # Generált API doksi felesleges contextnek
}

# Fájlok, amiket ne csomagoljunk be (kimenetek)
IGNORE_FILES: set[str] = {
    OUTPUT_FILENAME_TXT,
    OUTPUT_FILENAME_MD,
    "smart_pack.py",  # Önmagát ne
}


# ==========================================
# ☁️ DRIVE SZINKRONIZÁCIÓ (UBUNTU GVFS)
# ==========================================


def find_drive_path() -> Path | None:
    """Megkeresi az Ubuntu által felcsatolt Google Drive útvonalat.

    Returns:
        Path | None: A célmappa útvonala, vagy None ha nem található.
    """
    try:
        uid = os.getuid()
        gvfs_root = Path(f"/run/user/{uid}/gvfs")

        if not gvfs_root.exists():
            return None

        for item in gvfs_root.iterdir():
            if item.name.startswith("google-drive"):
                # Ellenőrizzük, hogy létezik-e benne a célmappa
                target = item / DRIVE_SUBFOLDER
                if target.exists():
                    print(f"✅ Drive és célmappa megtalálva: {target}")
                    return target

                print(f"ℹ️  Drive megvan, de a '{DRIVE_SUBFOLDER}' mappa hiányzik.")
                print(f"   Használom a gyökeret: {item}")
                return item

        return None
    except Exception as e:
        print(f"⚠️ Hiba a Drive keresésekor: {e}")
        return None


def sync_to_drive(source_file: Path) -> None:
    """Átmásolja a fájlt a Linux 'cp' parancsával (GVFS Workaround).

    Args:
        source_file: A forrásfájl útvonala.
    """
    dest_folder = find_drive_path()

    if not dest_folder:
        print("⚠️  Google Drive nincs felcsatolva. Csak helyi mentés történt.")
        return

    dest_file = dest_folder / source_file.name

    print(f"☁️  Szinkronizálás (Linux cp): {dest_file} ...")

    try:
        start_t = time.time()

        # A MÁGIKUS MEGOLDÁS: Rendszerparancs hívása
        # A 'cp' nem dob hibát az attribútumok miatt GVFS-en
        cmd = ["cp", str(source_file), str(dest_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            duration = time.time() - start_t
            print(f"✅ SIKER! Fájl feltöltve ({duration:.2f}s).")
        else:
            print(f"❌ Hiba a másoláskor (cp exit code {result.returncode}):")
            print(result.stderr)

    except Exception as e:
        print(f"❌ Kritikus hiba szinkronizáláskor: {e}")


# ==========================================
# 📦 CSOMAGOLÓ LOGIKA
# ==========================================


def is_ignored(path: Path) -> bool:
    """Eldönti, hogy egy fájl kihagyandó-e.

    Args:
        path: A vizsgált fájl útvonala.

    Returns:
        bool: True ha ki kell hagyni.
    """
    # 1. Kiterjesztés ellenőrzés
    if path.suffix.lower() in IGNORE_EXTENSIONS:
        return True

    # 2. Rejtett fájl ellenőrzés
    if path.name.startswith("."):
        return True

    # 3. Kimeneti fájlok kizárása
    if path.name in IGNORE_FILES:
        return True

    # 4. Útvonal alapú szűrés (Path parts használatával a string match helyett)
    try:
        # A projekt gyökeréhez viszonyított relatív útvonal
        rel_path = path.relative_to(PROJECT_ROOT)

        # Ellenőrizzük, hogy az útvonal bármely része (mappa) tiltólistás-e
        # Ez pontosabb, mint a string 'in', mert pl. a "data_loader.py" nem akad fenn a "data" tiltáson
        for part in rel_path.parts:
            if part in IGNORE_DIRS:
                return True

            # Speciális esetek (pl. docs/components)
            if f"{part}/" in str(rel_path):  # Részleges útvonal check
                for ignore in IGNORE_DIRS:
                    if ignore in str(rel_path):
                        return True

    except ValueError:
        return True

    return False


def pack_project(mode: str = "full") -> None:
    """Projekt csomagolása.

    Args:
        mode: Csomagolási mód (jelenleg csak 'full' támogatott).
    """
    print(f"📦 Context generálása ({mode} mód)...")

    # Fájlok gyűjtése
    all_files: list[Path] = []

    # 1. Kiemelt fájlok
    for f in INCLUDE_FILES:
        path = PROJECT_ROOT / f
        if path.exists():
            all_files.append(path)

    # 2. Mappák rekurzívan
    for d in INCLUDE_DIRS:
        dir_path = PROJECT_ROOT / d
        if dir_path.exists():
            all_files.extend(dir_path.rglob("*"))

    # Egyedi lista, rendezve
    unique_files = sorted(list(set(all_files)))
    count = 0

    try:
        with (
            open(OUTPUT_FILE_TXT, "w", encoding="utf-8") as out_txt,
            open(OUTPUT_FILE_MD, "w", encoding="utf-8") as out_md,
        ):
            # Header írása
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            header_txt = f"=== NEURAL AI NEXT CONTEXT ({mode.upper()}) ===\n"
            header_txt += f"Generated: {timestamp}\n\n"
            out_txt.write(header_txt)

            header_md = f"# NEURAL AI NEXT CONTEXT ({mode.upper()})\n"
            header_md += f"*Generated: {timestamp}*\n\n"
            out_md.write(header_md)

            for path in unique_files:
                if path.is_file() and not is_ignored(path):
                    try:
                        rel = path.relative_to(PROJECT_ROOT)
                        content = path.read_text(encoding="utf-8", errors="ignore")

                        # Write to TXT file
                        out_txt.write(f"\n{'=' * 50}\nFILE: {rel}\n{'=' * 50}\n{content}\n")

                        # Write to MD file
                        # Nyelv detektálás kiterjesztésből
                        ext = path.suffix[1:] if path.suffix else "text"
                        # Mapping specifikus kiterjesztésekhez
                        if ext == "mq5" or ext == "mqh":
                            ext = "cpp"

                        out_md.write(f"## `FILE: {rel}`\n\n")
                        out_md.write(f"```{ext}\n")
                        out_md.write(content)
                        out_md.write("\n```\n\n")

                        count += 1
                        print(f"  + {rel}")
                    except Exception as e:
                        print(f"⚠️  Hiba a(z) '{path}' feldolgozása közben: {e}")

        # Statisztika
        if OUTPUT_FILE_TXT.exists():
            size_mb_txt = os.path.getsize(OUTPUT_FILE_TXT) / (1024 * 1024)
            print(f"📄 TXT kész: {count} fájl ({size_mb_txt:.2f} MB) -> {OUTPUT_FILE_TXT}")

        if OUTPUT_FILE_MD.exists():
            size_mb_md = os.path.getsize(OUTPUT_FILE_MD) / (1024 * 1024)
            print(f"📄 MD kész:  {count} fájl ({size_mb_md:.2f} MB) -> {OUTPUT_FILE_MD}")

        # AUTO SYNC
        sync_to_drive(OUTPUT_FILE_TXT)
        sync_to_drive(OUTPUT_FILE_MD)

    except Exception as e:
        print(f"❌ Végzetes hiba a csomagolás során: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", default="full", nargs="?", help="Csomagolási mód")
    args = parser.parse_args()
    pack_project(args.mode)
