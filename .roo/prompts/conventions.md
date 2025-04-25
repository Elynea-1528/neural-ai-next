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
# Markdown vagy file tartalom esetén (4 backtick)
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

### 3.1 Fájl és osztály elnevezések
- Fájl/modul: snake_case (pl. data_processor.py)
- Osztályok: PascalCase (pl. DataProcessor)
- Függvények/változók: snake_case (pl. process_data)
- Konstansok: UPPERCASE_WITH_UNDERSCORES (pl. MAX_RETRY_COUNT)

### 3.2 Kód formázás
- Maximum sorhossz: 100 karakter
- Indentáció: 4 szóköz (ne tab)
- Sorvégi whitespace: nem megengedett
- Üres sorok: nem tartalmazhatnak whitespace karaktereket
- Fájl vége: egy üres sorral kell végződnie

### 3.3 Import sorrend
1. Standard library importok
2. Third-party library importok
3. Helyi/projekt importok

Példa:
```python
import os
import sys
from typing import Dict, List

import numpy as np
import pandas as pd

from neural_ai.core.base import BaseComponent
from neural_ai.utils import helpers
```

### 3.4 Docstring formátum (Google style)
```python
def calculate_metric(data: pd.DataFrame, window: int = 20) -> float:
    """Rövid egysoros leírás.

    Részletes többsoros leírás, ha szükséges.
    A leírás lehet több bekezdés is.

    Args:
        data: Az input adatok leírása
        window: Az ablakméret leírása

    Returns:
        A visszatérési érték leírása

    Raises:
        ValueError: Mikor és miért dobhat kivételt
    """
```

## 4. Dokumentációs szabályok

### 4.1 Markdown formázás
- H1 (#) csak dokumentum címhez
- H2 (##) fő szekciókhoz
- H3 (###) alszekciókhoz
- Kódblokkok kötelező syntax highlighting
- Lista behúzás: 2 szóköz
- Táblázatok kötelező fejléccel
- Sorvégi whitespace: nem megengedett
- Üres sorok: nem tartalmazhatnak whitespace karaktereket
- Fájl vége: egy üres sorral kell végződnie

### 4.2 Dokumentáció struktúra
```
/docs/components/[komponens_név]/
├── README.md                 # Áttekintés
├── api.md                    # API dokumentáció
├── architecture.md           # Architektúra leírás
├── design_spec.md           # Tervezési specifikáció
├── development_checklist.md  # Fejlesztési checklist
└── examples.md              # Használati példák
```

## 5. Git konvenciók

### 5.1 Branch elnevezések
- feature/[komponens]-[leírás]
- bugfix/[komponens]-[leírás]
- refactor/[komponens]-[leírás]
- docs/[komponens]-[leírás]
- test/[komponens]-[leírás]

### 5.2 Commit üzenetek
```
type(scope): rövid leírás

- Részletes pont 1
- Részletes pont 2

Issue: #123
```

Ahol type lehet:
- feat: új funkció
- fix: hibajavítás
- docs: dokumentáció
- style: formázás
- refactor: kód átírás
- test: tesztek
- chore: karbantartás
