# scripts/data_reset.py

## Áttekintés

Ez a script végrehajtja az adat reset műveletet a Neural AI Next rendszerben, törölve az összes tick adatot és logokat a tiszta validáció érdekében.

**Cél:** CORE DATA PIPELINE refaktorálás támogatása, biztosítva a tiszta állapotot a rendszer érvényesítéséhez.

**Verzió:** 1.0.0

## Fő jellemzők

- **Biztonságos törlés:** Ellenőrzi a könyvtárak létezését a törlés előtt.
- **Teljes reset:** Törli a teljes `data/tick/` könyvtárat és minden fájlt/alkönyvtárat a `logs/` könyvtárban.
- **Hibakezelés:** Részletes hibaüzenetek és sikeresség visszajelzés.
- **Könyvtár előkészítés:** Automatikusan létrehozza a szükséges könyvtárakat, ha nem léteznek.

## Használat

```bash
python scripts/data_reset.py
```

### Paraméterek

Nincs parancssori paraméter, a script automatikusan végrehajtja a reset műveletet.

## Architektúra

### Fő komponensek

1. **Könyvtár ellenőrzés:** `check_directory_exists()` - Ellenőrzi a cél könyvtárak létezését.
2. **Tick adatok törlése:** `remove_tick_data()` - Teljes `data/tick/` könyvtár törlése `shutil.rmtree()` segítségével.
3. **Logok törlése:** `remove_logs()` - Minden fájl és alkönyvtár törlése a `logs/` könyvtárban.
4. **Könyvtár előkészítés:** `create_directories_if_needed()` - Szükséges könyvtárak létrehozása `pathlib.Path.mkdir()` segítségével.

### Működési logika

```python
# 1. Könyvtárak ellenőrzése és létrehozása
create_directories_if_needed()

# 2. Tick adatok törlése (ha létezik)
tick_success = remove_tick_data()

# 3. Logok törlése (ha létezik)
logs_success = remove_logs()

# 4. Eredmény riport
```

## Biztonság

- **Ellenőrzés előtti törlés:** A script csak akkor töröl, ha a könyvtárak ténylegesen léteznek.
- **Nincs visszaállítás:** A törölt adatok nem állíthatók vissza, használja óvatosan.
- **Hiba esetén kilépés:** Ha bármely törlés sikertelen, a script hibakóddal lép ki.

## Tesztelés

A scripthez tartozó tesztek a `tests/scripts/` mappában találhatók.

```bash
pytest tests/scripts/test_data_reset.py -v
```

## Függőségek

- **Standard könyvtárak:** `os`, `shutil`, `sys`, `pathlib`
- **Típus annotáció:** `typing` (Optional, List)

## Kimenet példa

```
============================================================
🗑️  ADAT RESET - Tick adatok és logok törlése
============================================================

✅ Szükséges könyvtárak ellenőrizve/létrehozva
✅ Tick adatok törölve: data/tick
✅ Logok törölve: logs/*

============================================================
✅ Adat reset sikeres! Tiszta állapot a validációhoz.
============================================================