# MQL5 Fordítási Útmutató

## 🎯 Bevezetés

Ez az útmutató a Neural AI Next projekt MQL5 fejlesztéséhez szükséges fordítási folyamatot mutatja be. A projekt a MetaTrader 5 Expert Advisorokat használja valós idejű piaci adatok gyűjtéséhez.

## 📋 Előfeltételek

### Szükséges bővítmények (VS Code)

1. **MQL Extension Pack** (nicholishen)
   - Szintaxis kiemelés MQL5 fájlokhoz
   - Szerkesztő: File → Preferences → Extensions → "MQL Extension Pack"
   - Vagy: `ext install nicholishen.mql`

2. **C/C++ Extension Pack** (Microsoft)
   - C++ nyelvi támogatás (MQL5 C++-on alapul)
   - Automatikusan települ a MQL Extension Packkel

### VS Code beállítások

A projekt tartalmazza a szükséges beállításokat (`.vscode/settings.json`):

```json
"files.associations": {
    "*.mq5": "cpp",
    "*.mqh": "cpp"
}
```

Ez biztosítja a megfelelő szintaxis kiemelést `.mq5` és `.mqh` fájlokhoz.

## 🔧 Fordítási Módszerek

### 1. Automatikus Fordítási Script (Ajánlott)

Használd a `scripts/compile_mql.sh` scriptet a könnyű fordításért:

```bash
# Egy fájl fordítása
./scripts/compile_mql.sh neural_ai/core/collectors/mt5/Neural_AI_Next.mq5

# Az aktuális könyvtár összes .mq5 fájljának fordítása
./scripts/compile_mql.sh

# Teljes elérési úttal
bash scripts/compile_mql.sh /elérési/út/fájl.mq5
```

**Előnyök:**
- ✅ Automatikus Wine + MetaEditor integráció
- ✅ Színes kimenet (siker/hiba)
- ✅ Automatikus .ex5 fájl keresés
- ✅ Naplófájl létrehozása hibakereséshez
- ✅ Automatikus másolás MT5 Experts mappába
- ✅ Nincs VS Code bővítmény függőség

### 2. Kézi Fordítás Wine-en keresztül

```bash
# Wine prefix beállítása
export WINEPREFIX=~/.mt5

# Fordítás MetaEditorral
wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/metaeditor.exe \
  /compile:"/elérési/út/Neural_AI_Next.mq5" /log
```

### 3. Fordítás MT5-ben

1. **MetaEditor indítása:**
   ```bash
   export WINEPREFIX=~/.mt5
   wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/metaeditor.exe
   ```

2. **Kézi fordítás:**
   - File → Open → Válaszd ki a `.mq5` fájlt
   - Nyomd meg az `F7`-et vagy kattints a "Compile" gombra
   - Ellenőrizd a hibákat a kimeneti ablakban

## 🚀 Ajánlott Fejlesztési Munkafolyamat

### 1. Fájl Szerkesztése

```bash
# Navigálj az MT5 collector könyvtárba
cd neural_ai/core/collectors/mt5

# Szerkeszd az Expert Advisor-t
code Neural_AI_Next.mq5
```

### 2. Fordítás

```bash
# Projekt gyökérből
./scripts/compile_mql.sh neural_ai/core/collectors/mt5/Neural_AI_Next.mq5
```

### 3. Kimenet Ellenőrzése

```bash
# Ellenőrizd, hogy létrejött-e a .ex5 fájl
ls -la ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/MQL5/Experts/

# Vagy MT5 adatkönyvtár
ls -la ~/.mt5/drive_c/Users/Public/Documents/MetaTrader\ 5/MQL5/Experts/
```

### 4. Tesztelés MT5-ben

1. Nyisd meg az MT5-öt
2. Navigator → Expert Advisors
3. Húzd az EA-t egy chartra
4. Engedélyezd az "Allow automated trading" opciót

## 📁 Fájl Helyek

### Forrásfájlok

```
Projekt könyvtár:
  neural_ai/core/collectors/mt5/Neural_AI_Next.mq5

MT5 könyvtár:
  ~/.mt5/drive_c/Program Files/MetaTrader 5/MQL5/Experts/Neural_AI_Next.mq5
```

### Kimeneti Fájlok (Automatikusan generálva)

```
Elsődleges hely:
  ~/.mt5/drive_c/Program Files/MetaTrader 5/MQL5/Experts/Neural_AI_Next.ex5

Alternatív hely (MT5 adatkönyvtár):
  ~/.mt5/drive_c/Users/Public/Documents/MetaTrader 5/MQL5/Experts/Neural_AI_Next.ex5
```

## 🐛 Hibaelhárítás

### Hiba: "Wine not found"

```bash
# Wine telepítése
sudo apt install wine-stable winbind

# Ellenőrzés
wine --version
```

### Hiba: "MetaEditor not found"

```bash
# Ellenőrizd az MT5 telepítést
ls ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/metaeditor.exe

# Ha nem található, telepítsd az MT5-öt először
# Lásd: docs/WINE_MT5_SETUP.md
```

### Hiba: "Sikeres fordítás, de nincs .ex5 fájl"

```bash
# Ellenőrizd az MT5 adatkönyvtárat (gyakori probléma)
ls -la ~/.mt5/drive_c/Users/Public/Documents/MetaTrader\ 5/MQL5/Experts/

# MT5-ben: File → Open Data Folder → MQL5 → Experts
```

### Hiba: "Permission denied"

```bash
# Script futtathatóvá tétele
chmod +x scripts/compile_mql.sh

# MT5 könyvtár írhatóvá tétele
chmod -R u+w ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/MQL5
```

### Hiba: "Wine prefix not found"

```bash
# Wine prefix beállítása
export WINEPREFIX=~/.mt5

# Vagy állandó beállításhoz add hozzá a ~/.bashrc-hoz
echo 'export WINEPREFIX=~/.mt5' >> ~/.bashrc
```

## 🔄 VS Code Integráció (Opcionális)

Hozz létre egy `.vscode/tasks.json` fájlt a gyors fordításért:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "MQL5 Fordítás",
            "type": "shell",
            "command": "${workspaceFolder}/scripts/compile_mql.sh ${file}",
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            }
        }
    ]
}
```

**Használat:** Nyomj `Ctrl+Shift+B`-t az aktuális fájl fordításához

## 📊 Összehasonlítás: VS Code Bővítmény vs Script

| Funkció       | VS Code Bővítmény         | Fordítási Script       |
| ------------- | ------------------------- | ---------------------- |
| Beállítás     | Magas (bővítmény config)  | Alacsony (egy script)  |
| Megbízhatóság | Közepes (bővítmény hibák) | Magas (közvetlen Wine) |
| Integráció    | VS Code UI                | Terminál               |
| Sebesség      | Gyors (ha működik)        | Gyors                  |
| Hibakeresés   | Bővítmény naplók          | Script naplók          |
| Hordozhatóság | VS Code függő             | Önálló                 |

## ✅ Ellenőrzés

Fordítás után ellenőrizd:

```bash
# 1. Ellenőrizd a .ex5 fájl létezését
ls -la ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/MQL5/Experts/Neural_AI_Next.ex5

# 2. Ellenőrizd a fordítási naplót
cat /tmp/mql_compile.log

# 3. Töltsd be MT5-be
# Navigator → Expert Advisors → Neural_AI_Next
```

## 🎯 Következő Lépések

Miután a fordítás működik:

1. **HTTP Kliens Implementálása** az EA-ban (adatok küldése FastAPI-nak)
2. **HTTP Szerver Implementálása** az EA-ban (parancsok fogadása)
3. **Kétirányú Kommunikáció Tesztelése**
4. **Integráció Python Collectorral**

## 📚 További Erőforrások

- [Fordítási Script](../scripts/compile_mql.sh)
- [Wine + MT5 Beállítási Útmutató](WINE_MT5_SETUP.md)
- [MQL5 Dokumentáció](https://www.mql5.com/en/docs)
- [MetaEditor Parancssori Referencia](https://www.mql5.com/en/docs/common/metaeditor)

## 🔍 Projektstruktúra

```
neural_ai/core/collectors/
├── mt5/                          # MT5 specifikus kollektor
│   ├── Neural_AI_Next.mq5        # Expert Advisor forráskód
│   ├── Neural_AI_Next.ex5        # Fordított EA (generálva)
│   └── __init__.py              # Python csomag inicializálás
└── __init__.py                   # Collector csomag inicializálás
```

**Megjegyzés:** A projekt jelenleg csak MT5-öt használ, így nincs szükség külön metatrader almappára. Ha később más forrásokat (pl. MT4, TradingView) is hozzáadunk, akkor érdemes lehet átszervezni a struktúrát.