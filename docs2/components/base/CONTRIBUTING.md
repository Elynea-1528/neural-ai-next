# Közreműködési Útmutató

## Üdvözöljük!

Köszönjük, hogy érdeklődsz a Base komponens fejlesztése iránt! Ez az útmutató segít megérteni, hogyan lehet hatékonyan hozzájárulni a projekthez.

## Tartalomjegyzék

1. [Hogyan lehet hozzájárulni?](#hogyan-lehet-hozzájárulni)
2. [Fejlesztői környezet beállítása](#fejlesztői-környezet-beállítása)
3. [Kódolási konvenciók](#kódolási-konvenciók)
4. [Pull Request folyamat](#pull-request-folyamat)
5. [Tesztelés](#tesztelés)
6. [Dokumentáció](#dokumentáció)
7. [Hibajelentés](#hibajelentés)
8. [Funkció javaslat](#funkció-javaslat)
9. [Közösségi irányelvek](#közösségi-irányelvek)

## Hogyan lehet hozzájárulni?

### Hozzájárulási módok

1. **Hibajavítás** - Jelents hibát, vagy javíts ki egy meglévőt
2. **Új funkciók** - Implementálj új funkciókat vagy javíts a meglévőkön
3. **Dokumentáció** - Segíts javítani vagy bővíteni a dokumentációt
4. **Tesztelés** - Írj teszteket vagy segíts tesztelni
5. **Példák** - Hozz létre használati példákat
6. **Code Review** - Végezz code review-t mások kódján

### Első lépések

1. **Repository fork** - Forkold a repository-t a saját GitHub fiókodba
2. **Clone** - Klónozd le a forkol repository-t
3. **Branch** - Hozz létre egy új branchet a változtatásaidhoz
4. **Változtatások** - Végezd el a változtatásaidat
5. **Tesztelés** - Futtasd le a teszteket
6. **Pull Request** - Nyiss egy pull request-et

```bash
# Repository fork és clone
git clone https://github.com/YOUR_USERNAME/neural-ai-next.git
cd neural-ai-next

# Branch létrehozása
git checkout -b feature/my-new-feature

# Változtatások elvégzése
# ...

# Változtatások commitolása
git add .
git commit -m "Add my new feature"

# Branch pusholása
git push origin feature/my-new-feature
```

## Fejlesztői környezet beállítása

### Előfeltételek

- Python 3.8 vagy újabb
- Git
- Virtualenv (ajánlott)

### Telepítés

```bash
# Repository klónozása
git clone https://github.com/neural-ai/neural-ai-next.git
cd neural-ai-next

# Virtuális környezet létrehozása
python -m venv venv

# Aktiválás (Linux/Mac)
source venv/bin/activate

# Aktiválás (Windows)
venv\Scripts\activate

# Függőségek telepítése
pip install -r requirements.txt

# Fejlesztői függőségek telepítése
pip install -r requirements-dev.txt

# Projekt telepítése fejlesztői módban
pip install -e .
```

### Fejlesztői eszközök

```bash
# Tesztek futtatása
pytest tests/

# Kód formázás
black neural_ai/

# Linting
flake8 neural_ai/

# Típusellenőrzés
mypy neural_ai/

# Pre-commit hookok
pre-commit install
```

## Kódolási konvenciók

### Stílusvezérlés

A projekt a következő eszközöket használja a kódminőség érdekében:

- **Black** - Automatikus kódformázás
- **Flake8** - Linting
- **Mypy** - Statikus típusellenőrzés
- **Pylint** - Kódminőség ellenőrzés

### Kódolási szabályok

1. **Típusannotációk** - Minden függvényhez és metódushoz kötelező
2. **Docstring** - Minden osztályhoz és metódushoz kötelező (Google style)
3. **Névkonvenciók** - snake_case függvényekhez, PascalCase osztályokhoz
4. **Sorhossz** - Maximum 100 karakter
5. **Import sorrend** - Standard library, third-party, local imports

### Példa kód

```python
from typing import Dict, Any, Optional
from neural_ai.core.base.container import DIContainer


class MyComponent:
    """Új komponens leírása.

    Ez a komponens felelős a...
    """

    def __init__(self, config: Dict[str, Any]):
        """Inicializálás.

        Args:
            config: Konfigurációs beállítások
        """
        self.config = config
        self.container = DIContainer()

    def process_data(self, data: Any) -> Optional[Any]:
        """Adatok feldolgozása.

        Args:
            data: A feldolgozandó adatok

        Returns:
            A feldolgozott adatok, vagy None ha hiba történt

        Raises:
            ValueError: Ha az adatok érvénytelenek
        """
        if not data:
            raise ValueError("Az adatok nem lehetnek üresek")

        # Feldolgozás
        return processed_data
```

## Pull Request folyamat

### Pull Request létrehozása

1. **Branch neve** - Használj leíró nevet: `feature/`, `fix/`, `docs/`, stb.
2. **Commit üzenetek** - Legyenek egyértelműek és leíróak
3. **Tesztelés** - Minden változtatást tesztelj
4. **Dokumentáció** - Frissítsd a dokumentációt szükség esetén

### Commit üzenet formátum

```
type(scope): rövid leírás

- Részletes pont 1
- Részletes pont 2

Issue: #123
```

**Type lehet:**
- `feat` - Új funkció
- `fix` - Hibajavítás
- `docs` - Dokumentáció változtatás
- `style` - Formázás (nem változtat funkcionalitást)
- `refactor` - Kód refaktorálás
- `test` - Tesztek hozzáadása
- `chore` - Build folyamat vagy segédeszközök változtatása

**Példa:**
```
feat(container): add memory usage monitoring

- Add get_memory_usage() method to DIContainer
- Add memory statistics tracking
- Add example usage in documentation

Issue: #45
```

### Pull Request leírás

```markdown
## Milyen változtatásokat tartalmaz ez a PR?

Rövid leírás a változtatásokról.

## Milyen problémát old meg?

- Problem 1
- Problem 2

## Milyen funkciókat ad hozzá?

- Feature 1
- Feature 2

## Tesztelés

- [ ] Unit tesztek futtatva
- [ ] Integration tesztek futtatva
- [ ] Dokumentáció frissítve

## Screenshotok (ha alkalmazható)

## Kapcsolódó issue-k

Fixes #123
Related to #456
```

## Tesztelés

### Tesztelési stratégia

1. **Unit tesztek** - Egyedi komponensek tesztelése
2. **Integration tesztek** - Komponensek közötti interakciók tesztelése
3. **Teljesítménytesztek** - Lazy loading és egyéb optimalizációk tesztelése

### Teszt írása

```python
import unittest
from neural_ai.core.base import DIContainer


class TestDIContainer(unittest.TestCase):
    """DIContainer tesztosztály."""

    def setUp(self):
        """Teszt előkészítés."""
        self.container = DIContainer()

    def test_register_and_get_component(self):
        """Komponens regisztráció és lekérés tesztelése."""
        # Given
        test_component = TestComponent()

        # When
        self.container.register_instance(TestComponent, test_component)
        retrieved = self.container.get(TestComponent)

        # Then
        self.assertIs(retrieved, test_component)

    def test_lazy_loading(self):
        """Lazy loading tesztelése."""
        # Given
        load_count = 0

        def factory():
            nonlocal load_count
            load_count += 1
            return TestComponent()

        self.container.register_lazy('lazy_component', factory)

        # When
        self.assertEqual(load_count, 0)  # Még nem töltődött be

        component = self.container.get('lazy_component')

        # Then
        self.assertEqual(load_count, 1)  # Most töltődött be
        self.assertIsInstance(component, TestComponent)
```

### Teszt futtatás

```bash
# Összes teszt futtatása
pytest tests/

# Konkrét tesztfájl
pytest tests/core/base/test_container.py

# Konkrét teszt
pytest tests/core/base/test_container.py::TestDIContainer::test_register_and_get_component

# Részletes output
pytest -v tests/

# Coverage report
pytest --cov=neural_ai tests/
```

## Dokumentáció

### Dokumentációs szabályok

1. **Markdown formázás** - Kövessük a projekt konvencióit
2. **Kódpéldák** - Minden funkcióhoz tartozzon példa
3. **Linkek** - Használj relatív linkeket a dokumentációban
4. **Frissesség** - Tartsuk naprakészen a dokumentációt

### Dokumentáció szerkezet

```
docs2/components/base/
├── README.md                 # Áttekintés
├── api/                      # API dokumentáció
├── architecture/             # Architektúra dokumentáció
├── examples/                 # Használati példák
├── guides/                   # Útmutatók
├── CHANGELOG.md             # Változások naplója
└── CONTRIBUTING.md          # Közreműködési útmutató
```

### Dokumentáció írása

```markdown
# [Cím]

## Áttekintés

[Rövid leírás]

## Használat

```python
# Kódpélda
from neural_ai.core.base import DIContainer

container = DIContainer()
```

## Kapcsolódó dokumentáció

- [Link 1](link1.md)
- [Link 2](link2.md)
```

## Hibajelentés

### Hiba jelentésének lépései

1. **Keresés** - Ellenőrizd, hogy a hiba már fenn van-e jelentve
2. **Új issue** - Ha nem, hozz létre egy újat
3. **Leírás** - Add meg a hiba részletes leírását
4. **Reprodukció** - Írd le, hogyan lehet reprodukálni a hibát
5. **Várt viselkedés** - Add meg, mi a várt viselkedés
6. **Környezet** - Add meg a környezet adatait

### Issue template

```markdown
## Hiba leírása

Rövid és egyértelmű leírás a hibáról.

## Hogyan reprodukálni a hibát?

1. Lépés 1
2. Lépés 2
3. Lépés 3

## Várt viselkedés

Mit vártál volna, hogy történjen?

## Aktuális viselkedés

Mi történik valójában?

## Környezet

- Python verzió: [pl. 3.9.0]
- Operációs rendszer: [pl. Linux, Windows, macOS]
- Base komponens verzió: [pl. 1.0.0]

## További információk

Kiegészítő információk, screenshotok, stb.
```

## Funkció javaslat

### Funkció javaslat lépései

1. **Keresés** - Ellenőrizd, hogy a funkció már fenn van-e javasolva
2. **Új issue** - Ha nem, hozz létre egy újat
3. **Leírás** - Add meg a funkció részletes leírását
4. **Használati eset** - Írd le, milyen problémát oldana meg
5. **Alternatívák** - Felsorolni a lehetséges alternatívákat
6. **Kiegészítő információk** - További információk, mockupok, stb.

### Feature request template

```markdown
## Funkció leírása

Rövid és egyértelmű leírás a kívánt funkcióról.

## Probléma/motiváció

Miért lenne szükség erre a funkcióra? Milyen problémát oldana meg?

## Javasolt megoldás

Hogyan képzeled el a megvalósítást?

## Alternatívák

Milyen alternatív megoldásokat fontoltál meg?

## További információk

Kiegészítő információk, példák, stb.
```

## Közösségi irányelvek

### Viselkedési szabályok

1. **Tisztelet** - Legyél tisztelettel mások iránt
2. **Konstruktivitás** - Építő jellegű kritikát gyakorolj
3. **Nyitottság** - Fogadj el mások véleményét
4. **Együttműködés** - Segíts másoknak
5. **Proaktivitás** - Vállalj felelősséget

### Kommunikáció

- **Issues** - Használjunk egyértelmű és tiszteletteljes nyelvezetet
- **Pull Requests** - Legyünk nyitottak a konstruktív kritikára
- **Discussions** - Tartsunk ki a témához kapcsolódó beszélgetéseket
- **Code Review** - Koncentráljunk a kódra, ne a személyre

### Elfogadható viselkedés

- Tiszteletteljes és befogadó kommunikáció
- Konstruktív kritika és feedback
- Mások véleményének tiszteletben tartása
- Együttműködés és segítségnyújtás
- Proaktív hozzáállás

### Elfogadhatatlan viselkedés

- Sértő vagy kirekesztő megjegyzések
- Személyes támadások
- Trollkodás vagy provokáció
- Nyilvános vagy privát zaklatás
- Szerzői jogok megsértése

## GYIK (Gyakran Ismételt Kérdések)

### Hogyan kezdjek hozzá?

1. Olvasd el ezt az útmutatót
2. Nézd át a meglévő issue-kat
3. Válassz egy kisebb issue-t kezdésnek
4. Kérj hozzárendelést az issue-hoz
5. Kezdd el a fejlesztést

### Milyen issue-kat érdemes választani?

- `good first issue` - Jó kezdésnek
- `help wanted` - Segítségre vár
- `bug` - Hibajavítások
- `enhancement` - Funkcióbővítések

### Hogyan kérjek segítséget?

1. Nézd át a dokumentációt
2. Keress rá a korábbi issue-kra
3. Kérdezz a Discussions-ben
4. Nyiss egy issue-t, ha szükséges

### Mennyi időt kell szánnom?

Annyit, amennyit csak tudsz. Akár egy kis javítás is sokat segíthet.

## Kapcsolat

### Maintainerek

- [Maintainer 1](mailto:maintainer1@example.com)
- [Maintainer 2](mailto:maintainer2@example.com)

### További információk

- [Projekt README](README.md)
- [Dokumentáció](api/overview.md)
- [Változások naplója](CHANGELOG.md)
- [GitHub Repository](https://github.com/neural-ai/neural-ai-next)

## Köszönet

Köszönjük mindenkinek, aki hozzájárul a Base komponens fejlesztéséhez! A te hozzájárulásod segít jobbá tenni a projektet mindenki számára.

---

**Utolsó frissítés:** 2025-12-19
**Verzió:** 1.0.0
**Felelős:** Base Komponens Csapat
