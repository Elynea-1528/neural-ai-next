# compile_mql.sh - MQL5 Fordító Script

## Áttekintés

Az `compile_mql.sh` egy bash shell script, amely MQL5 fájlokat fordít le Wine segítségével Linux operációs rendszer alatt. A script a MetaTrader 5 MetaEditor64.exe-jét használja a fordításhoz, és automatikusan kezeli a fordított fájlok elhelyezését.

## Fájl információ

- **Elérési út:** `scripts/install/scripts/compile_mql.sh`
- **Típus:** Bash shell script
- **Feladat:** MQL5 fájlok fordítása Linux alatt Wine használatával

## Funkciók

### Főbb jellemzők

1. **Wine integráció:** Wine-en keresztül futtatja a MetaEditor64.exe-t
2. **Automatikus fájlfelderítés:** A script automatikusan felismeri a különböző MQL5 fájltípusokat (EA, Indicator, Script)
3. **Több hely ellenőrzése:** Keresi a fordított .ex5 fájlt több lehetséges helyen
4. **Automatikus másolás:** A fordított fájlokat átmásolja a projekt és az MT5 mappákba
5. **Színes kimenet:** Színes konzol kimenet a jobb átláthatóságért

### Függvények

#### `compile_file()`
Egyetlen MQL5 fájlt fordít le.

**Paraméterek:**
- `$1` - A forrásfájl elérési útja

**Viselkedés:**
- Ellenőrzi a fájltípust (.mq5 vagy .mqh)
- Meghatározza a kimeneti alkönyvtárat a fájlnév alapján
- Lefordítja a fájlt a MetaEditor segítségével
- Keresi a létrejött .ex5 fájlt több lehetséges helyen
- Átmásolja a fordított fájlt a `neural_ai/experts/mt5/compiled` mappába

#### `copy_to_mt5()`
A forrásfájlt és a fordított .ex5 fájlt átmásolja az MT5 Experts mappájába.

**Paraméterek:**
- `$1` - A forrásfájl elérési útja

**Viselkedés:**
- Létrehozza az MT5 Experts mappát, ha nem létezik
- Átmásolja a forrás .mq5 fájlt
- Megkeresi a fordított .ex5 fájlt
- Átmásolja a .ex5 fájlt az MT5 mappába

## Konfiguráció

A script a következő konfigurációs változókat használja:

```bash
WINEPREFIX="${WINEPREFIX:-$HOME/.mt5}"  # Wine prefix elérési út
MQL_DIR="$WINEPREFIX/drive_c/Program Files/MetaTrader 5"  # MT5 telepítési könyvtár
METAEDITOR="$MQL_DIR/MetaEditor64.exe"  # MetaEditor elérési út
SOURCE_DIR="${1:-$(pwd)}"  # Forráskönyvtár
OUTPUT_DIR="$MQL_DIR/MQL5"  # Kimeneti könyvtár
COMPILED_DIR="neural_ai/experts/mt5/compiled"  # Fordított fájlok könyvtára
```

## Használat

### Összes .mq5 fájl fordítása

Az aktuális könyvtárban lévő összes .mq5 fájl fordításához futtasd a scriptet argumentumok nélkül:

```bash
./scripts/install/scripts/compile_mql.sh
```

### Egy adott fájl fordítása

Egy specifikus fájl fordításához add meg a fájl elérési útját:

```bash
./scripts/install/scripts/compile_mql.sh neural_ai/experts/mt5/src/Neural_AI_Next_Multi.mq5
```

## Előfeltételek

A script futtatásához a következők szükségesek:

1. **Wine:** Telepítve kell legyen a rendszerre
   ```bash
   sudo apt install wine-stable
   ```

2. **MetaTrader 5:** Telepítve kell legyen a Wine prefixben
   - A script a `$HOME/.mt5` Wine prefixet használja alapértelmezetten
   - A MetaEditor64.exe-nek elérhetőnek kell lennie

3. **Wine prefix:** A Wine prefixnek léteznie kell
   - Alapértelmezett: `$HOME/.mt5`
   - Alternatívásként beállítható a `WINEPREFIX` környezeti változóval

## Kimenet

### Sikeres fordítás

```
==========================================
✓ Fordítás és másolás sikeres
==========================================

Az EA készen áll itt:
  Projekt: neural_ai/experts/mt5/compiled/
  MT5: /home/user/.mt5/drive_c/Program Files/MetaTrader 5/MQL5/Experts/

Használat MT5-ben:
  1. Nyisd meg az MT5-öt
  2. Navigator → Expert Advisors
  3. keresd meg az EA-t és húzd a chartra
```

### Sikertelen fordítás

```
==========================================
✗ Fordítás SIKERTELEN
==========================================

Ellenőrizd a fenti hibákat és próbáld újra.
```

## Fájltípusok

A script a következő fájltípusokat támogatja:

- **.mq5 (Expert Advisor):** EA-ként fordítja, az `Experts` mappába helyezi
- **.mq5 (Indicator):** Ha a fájlnév tartalmazza az "Indicator" szót, az `Indicators` mappába kerül
- **.mq5 (Script):** Ha a fájlnév tartalmazza a "Script" szót, a `Scripts` mappába kerül
- **.mqh (Header):** Header fájlokat nem fordítja, átugorja

## Hibakeresés

Ha a fordítás sikertelen, a script a következő információkat jeleníti meg:

1. A Wine visszatérési kódját
2. A keresett helyeket (forrás, kimenet, fordított mappa)
3. A MetaEditor naplójának tartalmát (`/tmp/mql_compile.log`)

## Kapcsolódó fájlok

- **Forrásfájlok:** `neural_ai/experts/mt5/src/*.mq5`
- **Fordított fájlok:** `neural_ai/experts/mt5/compiled/*.ex5`
- **MT5 mappa:** `$MQL_DIR/MQL5/Experts/`

## Telepítési útmutató

A script használatához kövesd a `docs/INSTALLATION_GUIDE.md` fájlban található utasításokat.

## Jegyzetek

- A script csak Linux rendszeren használható
- Wine-en keresztüli működés miatt a fordítás lassabb lehet, mint natív Windows alatt
- A MetaEditor verziójától függően a kimeneti fájl helye változhat
- A script automatikusan kezeli a különböző kimeneti helyeket
