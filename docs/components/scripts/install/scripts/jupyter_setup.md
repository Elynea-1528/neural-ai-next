# Jupyter Setup Script

## Áttekintés

A `jupyter_setup.py` script a Neural AI Next projekthez tartozó Jupyter kernel konfigurációt hozza létre. A script lehetővé teszi a Jupyter notebook-ok használatát a projekten belül, beleértve a Kaggle GPU környezet használatát is.

## Funkciók

### 1. Kernel Létrehozása

A `create_kernel()` függvény létrehozza a "neural-ai-next" nevű Jupyter kernel-t a következő jellemzőkkel:

- **Kernel név:** `neural-ai-next`
- **Display name:** "Neural AI Next"
- **Programnyelv:** Python
- **Környezeti változók:**
  - `PYTHONPATH`: A projekt gyökérkönyvtára
  - `CUDA_VISIBLE_DEVICES`: "0" (első CUDA eszköz használata)

A kernel konfiguráció a következő helyeken kerül elhelyezésre:
- `~/.local/share/jupyter/kernels/`
- `~/.jupyter/kernels/`

### 2. Kaggle Template Létrehozása

A `create_kaggle_template()` függvény létrehoz egy Kaggle notebook template-et (`kaggle_template.ipynb`), amely tartalmazza a szükséges importokat és alapvető beállításokat a Neural AI Next használatához Kaggle környezetben.

A template tartalmazza:
- A projekt elérési útjának hozzáadását
- Alapvető importokat (`CoreComponentFactory`, `MT5Collector`, `torch`)
- CUDA elérhetőség ellenőrzését

## Használat

### Futtatás

```bash
python scripts/install/scripts/jupyter_setup.py
```

### JupyterLab indítása

```bash
jupyter lab
```

### Kernel kiválasztása

A JupyterLab-ben:
1. Nyisd meg a notebook-ot
2. Menü: `Kernel -> Change Kernel -> Neural AI Next`

### Kaggle használata

1. Töltsd fel a `kaggle_template.ipynb` fájlt a Kaggle környezetbe
2. A template automatikusan konfigurálja a projekt elérési utat
3. Használhatod a Neural AI Next komponenseket

## Függvények

### `create_kernel() -> bool`

Létrehozza a Neural AI Next Jupyter kernel-t.

**Returns:**
- `bool`: True ha sikeres, False ha sikertelen

### `create_kaggle_template() -> bool`

Létrehozza a Kaggle notebook template-et.

**Returns:**
- `bool`: True ha sikeres, False ha sikertelen

### `main() -> None`

Fő belépési pont a Jupyter kernel konfigurációhoz. Koordinálja a kernel létrehozását és a template generálását, majd kiírja a használati utasításokat.

## Fájlok

- **Forrás:** `scripts/install/scripts/jupyter_setup.py`
- **Dokumentáció:** `docs/components/scripts/install/scripts/jupyter_setup.md`
- **Teszt:** `tests/scripts/install/scripts/test_jupyter_setup.py`

## Függőségek

- `json`: Konfigurációs fájlok kezeléséhez
- `subprocess`: Kernel telepítéséhez
- `sys`: Rendszer specifikus információkhoz
- `pathlib`: Fájlútkezeléshez
- `typing`: Típus hint-ekhez

## Hibakezelés

A script a következő hibákat kezeli:
- Ha nem található Jupyter kernel könyvtár, hibát jelez
- Ha a kernel telepítése nem sikerül, figyelmeztetést ad ki, de a konfiguráció létrejön

## Jellemzők

- Automatikus kernel könyvtár detektálás
- Kaggle kompatibilitás
- CUDA támogatás
- Debug mód engedélyezése
- Magyar nyelvű kimenetek

## Kapcsolódó Dokumentáció

- [Telepítési útmutató](../../../INSTALLATION_GUIDE.md)
- [Fejlesztői dokumentáció](../../../development/implementation_guide.md)
