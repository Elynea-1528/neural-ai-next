import argparse
import os
import subprocess
import time
from pathlib import Path

# ==========================================
# ⚙️ KONFIGURÁCIÓ
# ==========================================

PROJECT_ROOT = Path("/home/elynea/Dokumentumok/neural-ai-next")
OUTPUT_FILENAME = "neural_ai_full_context.txt"
OUTPUT_FILE = PROJECT_ROOT / OUTPUT_FILENAME

# ITT A LÉNYEG: A mappa neve a képről!
DRIVE_SUBFOLDER = "Google AI Studio"

# Mit vegyünk bele (Full mód)
INCLUDE_DIRS = ["neural_ai", "scripts", "configs", "docs", "external"]
INCLUDE_FILES = ["pyproject.toml", "main.py", "README.md", ".gitignore"]

# Mit hagyjunk ki (Zajszűrés)
IGNORE_PATTERNS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".git",
    ".vscode",
    "venv",
    "env",
    "data",
    "logs",
    "htmlcov",
    "build",
    ".gradle",
    "gradle",
    "node_modules",
    "docs/components",  # Generált API doksi felesleges
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
}

# ==========================================
# ☁️ DRIVE SZINKRONIZÁCIÓ (UBUNTU GVFS)
# ==========================================


def find_drive_path():
    """Megkeresi az Ubuntu által felcsatolt Google Drive útvonalat."""
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
                else:
                    print(f"ℹ️  Drive megvan, de a '{DRIVE_SUBFOLDER}' mappa nem található benne.")
                    print(f"   Próbáljuk a gyökérbe: {item}")
                    return item

        return None
    except Exception:
        return None


def sync_to_drive(source_file: Path):
    """Átmásolja a fájlt a Linux 'cp' parancsával (GVFS Workaround)."""
    dest_folder = find_drive_path()

    if not dest_folder:
        print("⚠️  Google Drive nincs felcsatolva. Csak helyi mentés történt.")
        return

    dest_file = dest_folder / OUTPUT_FILENAME

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
        print(f"❌ Kritikus hiba: {e}")


# ==========================================
# 📦 CSOMAGOLÓ LOGIKA
# ==========================================


def is_ignored(path):
    if path.name.startswith("."):
        return True
    if path.suffix.lower() in IGNORE_PATTERNS:
        return True
    for part in path.parts:
        if part in IGNORE_PATTERNS:
            return True
    return False


def pack_project(mode="full"):
    print(f"📦 Context generálása ({mode} mód)...")

    # Fájlok gyűjtése
    all_files = []
    for f in INCLUDE_FILES:
        all_files.append(PROJECT_ROOT / f)
    for d in INCLUDE_DIRS:
        all_files.extend((PROJECT_ROOT / d).rglob("*"))

    unique_files = sorted(list(set(all_files)))
    count = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"=== NEURAL AI NEXT CONTEXT ({mode.upper()}) ===\n")
        out.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for path in unique_files:
            if path.is_file() and not is_ignored(path):
                if path.name == OUTPUT_FILENAME or "pack" in path.name:
                    continue
                try:
                    rel = path.relative_to(PROJECT_ROOT)
                    content = path.read_text(encoding="utf-8", errors="ignore")
                    out.write(f"\n{'=' * 50}\nFILE: {rel}\n{'=' * 50}\n{content}\n")
                    count += 1
                except:
                    pass

    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"📄 Helyi fájl kész: {count} fájl ({size_mb:.2f} MB)")

    # AUTO SYNC
    sync_to_drive(OUTPUT_FILE)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", default="full", nargs="?")
    args = parser.parse_args()
    pack_project(args.mode)
