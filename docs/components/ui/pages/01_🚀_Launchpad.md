# 🚀 Launchpad Oldal

## Áttekintés

A Launchpad oldal az alkalmazás fő indítólapja, amely áttekintést nyújt a rendszer állapotáról és gyors elérést biztosít a különböző modulokhoz. Ez az oldal szolgál a felhasználói navigáció központi pontjaként.

## Szerkezet

### Fájl elérési út
- **Forráskód**: [`neural_ai/ui/pages/01_🚀_Launchpad.py`](../../../neural_ai/ui/pages/01_🚀_Launchpad.py)
- **Tesztfájl**: [`tests/ui/pages/test_launchpad_page.py`](../../../tests/ui/pages/test_launchpad_page.py)

### Osztályok

#### `LaunchpadPage`

Az indítólap fő osztálya, amely implementálja a `PageInterface` interfészt.

##### Attribútumok

- `_bridge: CoreBridgeInterface` - A backend bridge példány
- `_loaded: bool` - Az oldal betöltöttségi állapota
- `_title: str` - Az oldal címe ("🚀 Launchpad")

##### Metódusok

###### `__init__(bridge: CoreBridgeInterface, **kwargs: Optional[str]) -> None`

Az osztály konstruktora.

**Paraméterek:**
- `bridge`: A backend bridge példány, amely biztosítja a kapcsolatot a core rendszerrel
- `**kwargs`: Opcionális kulcsszó argumentumok

**Példa:**
```python
from neural_ai.ui.pages import LaunchpadPage
from neural_ai.ui.core_bridge import CoreBridge

bridge = CoreBridge()
page = LaunchpadPage(bridge=bridge)
```

###### `render() -> None`

Az oldal tartalmának renderelése. Létrehozza a vizuális kártyákat a különböző modulokhoz, amelyek kerettel ellátott container-ekben jelennek meg.

**Funkcionalitás:**
- Megjeleníti az oldal címét
- Létrehozza a kártyákat 3 sorban:
  - **Első sor**: Data Hub és Dev Center
  - **Második sor**: Live Ops és AI Lab
  - **Harmadik sor**: Strategy Lab
- Minden kártya tartalmaz:
  - Alcímet (subheader)
  - Rövid leírást
  - Linket a megfelelő oldalra
- Megjeleníti a rendszer áttekintését

**Vizuális elrendezés:**
```
┌─────────────────────┬─────────────────────┐
│  📥 Data Hub        │  🛠️ Dev Center      │
│  Leírás...          │  Leírás...          │
│  [👉 Megnyitás]     │  [👉 Megnyitás]     │
└─────────────────────┴─────────────────────┘
┌─────────────────────┬─────────────────────┐
│  ⚡ Live Ops        │  🧠 AI Lab          │
│  Leírás...          │  Leírás...          │
│  [👉 Megnyitás]     │  [👉 Megnyitás]     │
└─────────────────────┴─────────────────────┘
┌─────────────────────┐
│  🪲 Strategy Lab    │
│  Leírás...          │
│  [👉 Megnyitás]     │
└─────────────────────┘
```

###### `on_navigate_to(params: Optional[dict[str, str]] = None) -> None`

Akció, amikor az oldalra navigálnak.

**Paraméterek:**
- `params`: Navigációs paraméterek dictionary formájában, vagy None

**Viselkedés:**
- Beállítja a `_loaded` attribútumot `True` értékre
- Naplózza a navigációt a konzolra

###### `on_navigate_from() -> None`

Akció, amikor elnavigálnak az oldalról.

**Viselkedés:**
- Naplózza az elnavigálást a konzolra

##### Property-k

###### `title: str` (read-only)

Az oldal címét adja vissza.

**Visszatérési érték:**
- `str`: Az oldal címe ("🚀 Launchpad")

###### `is_loaded: bool` (read-only)

Az oldal betöltöttségi állapotát ellenőrzi.

**Visszatérési érték:**
- `bool`: True, ha az oldal betöltött, egyébként False

## Használat

### Alapvető használat

```python
from neural_ai.ui.pages import LaunchpadPage
from neural_ai.ui.core_bridge import CoreBridge

# Bridge létrehozása
bridge = CoreBridge()

# Oldal példányosítása
page = LaunchpadPage(bridge=bridge)

# Oldal renderelése
page.render()
```

### Navigáció kezelése

```python
# Oldalra navigálás
page.on_navigate_to({"source": "menu"})

# Oldalról elnavigálás
page.on_navigate_from()

# Állapot ellenőrzése
if page.is_loaded:
    print(f"Oldal betöltve: {page.title}")
```

## Tesztelés

A modult átfogó tesztesetekkel ellátottuk, amelyek a következő területeket fedik le:

### Tesztesetek

1. **Inicializálás tesztjei**
   - Alap inicializálás
   - Inicializálás további paraméterekkel

2. **Property tesztjei**
   - `title` property ellenőrzése
   - `is_loaded` property kezdeti állapota
   - `is_loaded` property navigáció után

3. **Navigációs tesztek**
   - Navigálás paraméterekkel
   - Navigálás paraméterek nélkül
   - Oldal elhagyása

4. **Renderelési tesztek**
   - Render metódus alapvető működése
   - Render metódus hibamentes futása

### Tesztfuttatás

```bash
# Összes teszt futtatása
pytest tests/ui/pages/test_launchpad_page.py -v

# Coverage jelentés
pytest tests/ui/pages/test_launchpad_page.py --cov=neural_ai.ui.pages --cov-report=html
```

### Teszt eredmények

- **Tesztesetek száma**: 10
- **Sikeres tesztek**: 10/10 ✅
- **Coverage**: 100% (Statement és Branch)

## Fejlesztés

### Architektúra

A `LaunchpadPage` osztály követi a projekt architektúra szabványait:

- **Interface-elv**: A `PageInterface` interfészt implementálja
- **Dependency Injection**: A `CoreBridgeInterface`-t konstruktoron keresztül kapja meg
- **Típusos annotációk**: Minden metódus rendelkezik típusannotációval
- **Docstring**: Google Style docstring-ek használata

### Kódminőség

- **Linter**: Ruff (0 hiba)
- **Típusellenőrzés**: Szigorú típusos használat, `Any` típus tiltva
- **Dokumentáció**: Magyar nyelvű docstring-ek

### Refaktorálás

A legutóbbi refaktorálás során a következő változtatásokat hajtottuk végre:

1. **Vizuális fejlesztés**: A sima `st.page_link`-eket vizuális kártyákra cseréltük
2. **Típusok javítása**: Az `Any` típusokat konkrét típusokra cseréltük
3. **Dokumentáció**: Teljes körű magyar Google Style docstring-eket adtunk hozzá
4. **Tesztelés**: 100% coverage-t biztosító teszteseteket hoztunk létre

## Kapcsolódó dokumentáció

- [UI Architektúra](../architecture.md)
- [Page Interface](../../interfaces/page_interface.md)
- [Core Bridge Interface](../../interfaces/core_bridge_interface.md)
- [Streamlit App](../../streamlit_app.md)

## Verziótörténet

- **v6.0.0** (2026-01-04): Refaktorálás - Vizuális kártyák bevezetése
- **v5.x**: Előző verziók sima linkekkel

## Szerző

- **Fejlesztő**: Neural AI Next Team
- **Utolsó módosítás**: 2026-01-07