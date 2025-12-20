# ❓ Ask Mód - Neural AI Next

## Alapelvek

Az Ask módban a következő alapelvekre kell koncentrálni:

1. **Magyar nyelv** - Minden választ magyar nyelven adj
2. **Tömörség** - Légy pontos és tömör, de mindig adj elég kontextust
3. **Strukturáltság** - Használj markdown formázást a válaszokban
4. **Projekt kontextus** - Mindig tartsd szem előtt a Neural AI Next projekt specifikációit

## Válaszadási szabályok

### 1. Nyelvi preferencia

- Minden választ **magyar nyelven** adj
- Használj szakmai terminológiát, de magyarul
- A kódkommenteket is magyarul írd

### 2. Formázás

Használd a markdown formázást:

- **Félkövér** a fontos kiemelésekhez
- *Dőlt* a hangsúlyozáshoz
- `kód` a kódrészletekhez
- ```python ... ``` a teljes kódblokkokhoz

### 3. Linkelés

Minden fájlt és kódrészletet linkelj a projektben:

- Fájlok: [`fájlnév`](relative/path/to/file.ext)
- Kód: [`function_name()`](relative/path/to/file.ext:line)
- Dokumentáció: [Dokumentáció neve](../../docs/path/to/doc.md)

### 4. Példák és kód

Amikor kódot mutatsz be, mindig:
- Használj syntax highlightingot
- Add meg a fájl elérési útját
- Magyarázd el, mit csinál a kód
- Mutass konkrét példát a projektből

### 5. Projekt specifikus kontextus

Mindig emlékezz a következőkre:

- A projekt **Python 3.10+**-t használ
- **Container-based architektúra** van érvényben
- **Komponens alapú** fejlesztés
- **Hierarchikus rendszer** struktúra
- **MT5 integráció** a kulcsfontosságú

## Kérdések típusai és válaszadás

### 1. Koncepciók és elmélet

Amikor elméleti kérdés jön:
- Magyarázd el a koncepciót egyszerűen
- Mutass példát a projektből
- Linkeld a releváns dokumentációt
- Ne terjengőss, de legyél átfogó

### 2. Kódmagyarázat

Amikor kódot kell magyarázni:
- Mutasd be a kódot részletekben
- Magyarázd el, mit csinál minden rész
- Mutass alternatívák a projektben
- Linkeld a kapcsolódó komponenseket

### 3. Hibaelhárítás

Amikor hibaüzenet jön:
- Elemezd a hiba okát
- Mutass a projektben lévő hibakezelési mechanizmusokra
- Javasolj konkrét megoldást
- Linkeld a releváns dokumentációt

### 4. Dokumentáció

Amikor dokumentációt kérnek:
- Vezesd a felhasználót a megfelelő fájlhoz
- Részletezd a dokumentáció struktúrát
- Mutasd be a kapcsolódó komponenseket
- Linkeld a template-eket és példákat

## Projekt specifikus tudnivalók

### Core Komponensek

Mindig emlékezz a projekt fő komponenseire:

1. **Base** - Alap komponens, Container osztály
2. **Config** - YAML alapú konfigurációkezelés
3. **Logger** - Strukturált naplózás
4. **Storage** - Fájl alapú adattárolás
5. **Collectors** - Adatgyűjtő komponensek (MT5)

### Dokumentáció struktúra

A projekt dokumentációja a következő szerkezetet követi:

- `docs/architecture/` - Rendszerarchitektúra
- `docs/components/` - Komponens dokumentáció
- `docs/development/` - Fejlesztői útmutatók
- `docs/templates/` - Kód template-ek

### Fejlesztési folyamat

Amikor fejlesztési kérdés jön:
- Említsd meg a komponens alapú megközelítést
- Hivatkozz a template-ekre
- Linkeld a fejlesztési checklistákat
- Mutasd be a tesztelési stratégiát

## Hasznos linkek gyűjteménye

### Architektúra
- [Rendszer Architektúra](../../docs/architecture/overview.md)
- [Hierarchikus Rendszer](../../docs/architecture/hierarchical_system/overview.md)
- [Modell Struktúra](../../docs/models/hierarchical/structure.md)

### Komponensek
- [Base Komponens](../../docs/components/base/README.md)
- [Config Komponens](../../docs/components/config/README.md)
- [Logger Komponens](../../docs/components/logger/README.md)
- [Storage Komponens](../../docs/components/storage/README.md)

### Fejlesztés
- [Egységes Fejlesztési Útmutató](../../docs/development/unified_development_guide.md)
- [Komponens Fejlesztési Útmutató](../../docs/development/component_development_guide.md)
- [Code Review Útmutató](../../docs/development/code_review_guide.md)

### Template-ek
- [Komponens Template](../../docs/templates/component_template.py)
- [Interfész Template](../../docs/templates/interface_template.py)
- [Teszt Template](../../docs/templates/test_template.py)

## Válaszadási példák

### Jó válasz példa:

```python
# A projektben a [`Container`](neural_ai/core/base/container.py:1) osztályt kell használni
# komponensek létrehozásához. Ez biztosítja a függőséginjektálást és a naplózást.

from neural_ai.core.base.container import Container

class MyComponent(Container):
    """Példa komponens."""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.logger = self.get_logger()
```

### Rossz válasz példa:

"Használd a Container osztályt."

(Az első példa jobb, mert konkrét kódot mutat, linkeli a fájlt, és magyarázatot ad.)
