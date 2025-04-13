# GitHub Copilot Instructions

## 1. Válasz formátum

- Használj Markdown formázást a válaszokban
- Minden választ magyar nyelven adj
- Válaszonként csak egy választ adj (ne alternatívák listáját)
- Vedd figyelembe a VS Code kontextust
- Linux specifikus parancsokat használj

### 1.1 Kódblokk formázási szabályok

```python
# Normál kódblokk (3 backtick)
def example_function():
    return "Hello World"
```

````markdown
<!-- Markdown vagy file tartalom esetén (4 backtick) -->
```python
def example_function():
    return "Hello World"
```
````

### 1.2 Létező fájl módosításakor

```python
# ...existing code...
def new_function():
    """Új függvény."""
    # Implementáció
    return result
# ...existing code...
```

## 2. ASCII diagramok és hierarchia struktúrák
- NE használj backtick-eket ASCII diagramok és hierarchia struktúrák köré
- A projekt faszerkezetet és ASCII diagramokat közvetlenül, indentálással formázd
- A hierarchia struktúrát egyszerű szövegként illeszd be, megfelelő behúzással
- Példa a helyes formázásra:

### ASCII diagram példa:
  +-------+      +--------+
  |       |      |        |
  | InputA+----->+ OutputX|
  |       |      |        |
  +-------+      +--------+

## 3. Kódolási konvenciók

- **Fájl/modul elnevezés**: snake_case (pl. data_processor.py)
- **Osztályok**: PascalCase (pl. DataProcessor)
- **Függvények/változók**: snake_case (pl. process_data)
- **Konstansok**: UPPERCASE_WITH_UNDERSCORES (pl. MAX_RETRY_COUNT)
- **Max sorhossz**: 100 karakter
- **Behúzás**: 4 szóköz (ne tab)
- **Import sorrend**: standard lib → third-party → project
- **Docstring stílus**: Google style

### 3.1 Docstring példa

```python
def calculate_trend_strength(price_data: pd.DataFrame, window: int = 20, threshold: float = 0.01) -> Dict[str, Any]:
    """
    Kiszámítja a piaci trend erősségét és irányát az adott árfolyamadatok alapján.

    A függvény mozgóátlagok és a korreláció kombinációjával határozza meg a trend
    jelenlétét és erősségét. Az eredmények normalizálva vannak 0-1 közötti értékre.

    Args:
        price_data (pd.DataFrame): OHLCV árfolyamadatok DataFrame formában
        window (int, optional): Időablak mérete. Alapértelmezett: 20
        threshold (float, optional): Trend váltási küszöbérték. Alapértelmezett: 0.01

    Returns:
        Dict[str, Any]: Trend erősség mutatók szótára:
            - 'strength': 0-1 közötti érték a trend erősségére
            - 'direction': 1 (emelkedő), 0 (oldalazó), -1 (csökkenő)

    Raises:
        ValueError: Ha az árfolyamadatok nem tartalmaznak elegendő sort
        TypeError: Ha az árfolyamadatok nem DataFrame formátumúak
    """
```

## 4. Dokumentációs szabályok

A komponensek dokumentációja az alábbi struktúrát kövesse:

```
/docs/components/[komponens_név]/
  ├── README.md                 # Áttekintés és használati útmutató
  ├── api.md                    # API dokumentáció
  ├── architecture.md           # Architektúra leírás
  ├── design_spec.md            # Tervezési specifikáció
  ├── development_checklist.md  # Fejlesztési checklist
  └── examples.md               # Használati példák
```

Emellett a projekt szintű fejlesztések követésére az alábbi struktúrát használjuk:

```
/docs/development/
  ├── DEVELOPMENT_STATUS.md    # Központi fejlesztési állapot dokumentum
  └── checklist_template.md    # Checklist sablon új komponensekhez
```

A fejlesztési checklistek karbantartása elengedhetetlen a projekt előrehaladásának követéséhez és a fejlesztési folyamat standardizálásához.

A részletesebb projektspecifikus információkat, struktúrákat és mintákat a `.github/prompts/.prompt.md` fájlban találod.

## 5. Git és verziókezelési konvenciók

### 5.1 Branch elnevezések
- **feature/komponens_nev-funkcio_nev**: Új funkciók fejlesztése
- **bugfix/komponens_nev-hiba_leiras**: Hibák javítása
- **refactor/komponens_nev-refaktor_leiras**: Kód refaktorálás
- **docs/komponens_nev-dokumentacio_leiras**: Dokumentáció frissítés
- **test/komponens_nev-teszt_leiras**: Tesztekkel kapcsolatos változtatások

### 5.2 Branch létrehozása új komponens fejlesztéséhez
```bash
git checkout main
git pull
git checkout -b feature/processors-trend_analyzer
```

### 5.3 Commit üzenetek formátuma
- Használj szemantikus commit üzeneteket: `típus(hatókör): üzenet`
   - Példák:
     - `feat(processors): trend erősség számítás hozzáadása`
     - `fix(storage): üres dataframe hiba kezelése`
     - `docs(readme): telepítési útmutató frissítése`
     - `test(collectors): unit tesztek hozzáadása az mt5 collectorhoz`

## 7. Fejlesztési Checklist Formátum

### 7.1 Komponens checklist struktúra
```markdown
# [Komponens Név] Fejlesztési Checklist

## Előkészületek
- [ ] Komponens specifikáció áttekintése
- [ ] Függőségek elemzése
- [ ] Interfészek megtervezése

## Implementáció
- [ ] Interfész definiálása az `interfaces` mappában
- [ ] Alapimplementáció létrehozása
- [ ] Factory osztály implementálása vagy frissítése
- [ ] Segédosztályok és függvények implementálása
- [ ] Hibakezelés implementálása
- [ ] Logolás megfelelő szinteken

## Tesztelés
- [ ] Unit tesztek írása az interfészhez
- [ ] Unit tesztek írása az implementációhoz
- [ ] Edge case tesztek
- [ ] Teljesítmény tesztek (ha szükséges)
- [ ] Integrációs tesztek

## Dokumentáció
- [ ] README.md elkészítése
- [ ] API dokumentáció frissítése
- [ ] Architektúra leírás
- [ ] Használati példák
- [ ] Konfigurációs lehetőségek dokumentálása

## Ellenőrzés
- [ ] Kód áttekintés
- [ ] Teljesítmény ellenőrzés
- [ ] Docstringek minden osztályhoz és metódushoz
- [ ] Tesztek 100% lefedettséggel
```
### 7.2 Központi Fejlesztési Állapot Frissítése
A központi fejlesztési állapotot frissítsd a következő sablonnal:
```markdown
# Neural-AI-Next Fejlesztési Állapot

Utoljára frissítve: [DÁTUM]

## Jelenlegi fókusz
- [Komponens név] implementálása

## Befejezett komponensek
- [x] [Komponens név] ([befejezés dátuma])
```
