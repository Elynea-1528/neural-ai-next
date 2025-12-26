# DIContainer és LazyComponent Tesztelés

## Áttekintés

Ez a dokumentum a [`tests/core/base/test_container.py`](../../../../tests/core/base/test_container.py) tesztfájl dokumentációja, amely a `DIContainer` és `LazyComponent` osztályok funkcionalitását ellenőrzi.

## Tesztelt Komponensek

### LazyComponent

A lusta betöltésű komponensek wrapper osztályának tesztelése:

- **`test_lazy_loading_initial_state`**: Ellenőrzi a kezdeti állapotot
  - A komponens nem betöltött állapotban van
  - Az instance None értékű

- **`test_lazy_loading_get`**: Teszteli a komponens lekérését
  - A factory függvény csak egyszer hívódik meg
  - A komponens betöltött állapotba kerül
  - Az instance helyesen jön létre

- **`test_lazy_loading_thread_safety`**: Ellenőrzi a szálbiztosságot
  - 10 szálból mind ugyanazt az instance-t kapja
  - A factory csak egyszer hívódik meg

### DIContainer

A dependency injection konténer tesztelése:

#### Alap műveletek

- **`test_initialization`**: Konténer inicializálás
  - Üres instances, factories és lazy_components szótárak

- **`test_register_instance`**: Példány regisztrálása
  - Az instance elmentésre kerül a megfelelő interfész alá

- **`test_register_factory`**: Factory regisztrálása
  - A factory függvény elmentésre kerül

- **`test_resolve_instance`**: Példány feloldása
  - A regisztrált instance-t adja vissza

- **`test_resolve_factory`**: Factory feloldása
  - A factory létrehozza és elmenti az instance-t

- **`test_resolve_not_found`**: Nem található komponens
  - None értékkel tér vissza

#### Lusta komponensek kezelése

- **`test_register_lazy_valid`**: Érvényes lusta komponens regisztrálása
  - A komponens elmentésre kerül a lazy_components szótárba
  - Kezdetben nem betöltött állapotban van

- **`test_register_lazy_invalid_name`**: Érvénytelen név ellenőrzése
  - Üres string esetén ValueError kivételt dob

- **`test_register_lazy_invalid_factory`**: Érvénytelen factory ellenőrzése
  - Nem hívható objektum esetén ValueError kivételt dob

- **`test_get_lazy_component`**: Lusta komponens lekérése
  - A komponens betöltődik és áthelyeződik a regular instances-be
  - A lazy_components-ből törlődik

- **`test_get_component_not_found`**: Nem található komponens lekérése
  - ComponentNotFoundError kivételt dob

- **`test_get_lazy_components_status`**: Lusta komponensek állapotának lekérdezése
  - Visszaadja az összes lusta komponens betöltöttségi állapotát

- **`test_preload_components`**: Komponensek előtöltése
  - A megadott komponensek előre betöltésre kerülnek

#### Konténer kezelés

- **`test_clear`**: Konténer ürítése
  - Minden szótár kiürítésre kerül

#### Singleton minta ellenőrzés

- **`test_verify_singleton_warning`**: Singleton figyelmeztetés
  - Nem megfelelő singleton implementáció esetén figyelmeztetést ad

- **`test_enforce_singleton_violation`**: Singleton megsértésének észlelése
  - Duplikált regisztráció esetén SingletonViolationError kivételt dob

#### Komponens regisztráció

- **`test_register_valid`**: Érvényes komponens regisztrálása
  - A példány elmentésre kerül

- **`test_register_invalid_name`**: Érvénytelen név ellenőrzése
  - Üres string esetén ValueError kivételt dob

- **`test_register_none_instance`**: None példány ellenőrzése
  - None érték esetén ValueError kivételt dob

#### Memóriahasználat

- **`test_get_memory_usage`**: Memóriahasználat lekérdezése
  - Visszaadja a konténer statisztikáit
  - Tartalmazza az instance-ok méretét

#### Példány lekérés

- **`test_get_regular_instance`**: Regisztrált példány lekérése
  - A get metódussal történő lekérés helyes instance-t ad vissza

## Tesztlefedettség

A tesztfájl 100% statement és branch coverage-t biztosít a [`DIContainer`](../../../neural_ai/core/base/implementations/di_container.md) és [`LazyComponent`](../../../neural_ai/core/base/implementations/di_container.md) osztályokhoz.

## Futtatás

```bash
# Egyedi tesztfájl futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/base/test_container.py -v

# Coverage jelentéssel
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/base/test_container.py -v \
  --cov=neural_ai.core.base.implementations.di_container --cov-report=term

# Linter ellenőrzés
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check tests/core/base/test_container.py
```

## Kapcsolódó Dokumentáció

- [`DIContainer` implementáció](../../../neural_ai/core/base/implementations/di_container.md)
- [`LazyComponent` implementáció](../../../neural_ai/core/base/implementations/di_container.md)
- [Base modul áttekintés](../../../neural_ai/core/base/__init__.md)
- [Tesztelési szabványok](../../../development/architecture_standards.md)