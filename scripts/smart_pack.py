import argparse
import os
import time
from pathlib import Path

# ==========================================
# ⚙️ KONFIGURÁCIÓ
# ==========================================

PROJECT_ROOT = Path("/home/elynea/Dokumentumok/neural-ai-next")
OUTPUT_FILENAME = "neural_ai_full_context.txt"
OUTPUT_FILE = PROJECT_ROOT / OUTPUT_FILENAME

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
        # Az Ubuntu a /run/user/{UID}/gvfs alá csatol
        uid = os.getuid()
        gvfs_root = Path(f"/run/user/{uid}/gvfs")

        if not gvfs_root.exists():
            return None

        # Keressük a 'google-drive' kezdetű mappát (bármilyen email címmel)
        for item in gvfs_root.iterdir():
            if item.name.startswith("google-drive"):
                print(f"✅ Drive megtalálva: {item}")
                return item

        return None
    except Exception:
        return None


def sync_to_drive(source_file: Path):
    """Átmásolja a generált fájlt a Drive-ra (GVFS workaround)."""
    drive_root = find_drive_path()

    if not drive_root:
        print("⚠️  Google Drive nincs felcsatolva. Csak helyi mentés történt.")
        return

    dest_file = drive_root / OUTPUT_FILENAME

    print("☁️  Szinkronizálás folyamatban (Stream Mode)...")
    try:
        start_t = time.time()

        # GVFS WORKAROUND:
        # shutil.copy2 helyett kézi bináris olvasás/írás.
        # Ez nem viszi át a metadatát (időbélyeg), amit a Drive nem szeret,
        # de átviszi a tartalmat, ami nekünk kell.
        with open(source_file, "rb") as f_src:
            with open(dest_file, "wb") as f_dst:
                shutil.copyfileobj(f_src, f_dst)

        duration = time.time() - start_t
        print(f"✅ SIKER! Fájl feltöltve ide: {dest_file} ({duration:.2f}s)")

    except Exception as e:
        print(f"❌ Hiba a másoláskor: {e}")
        print("   (A helyi fájl továbbra is elérhető a projekt mappában.)")


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
