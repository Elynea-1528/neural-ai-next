# Tesztelési Dokumentáció: `tests/core/base/test_exceptions.py`

## Áttekintés

Ez a dokumentáció a [`tests/core/base/test_exceptions.py`](tests/core/base/test_exceptions.py:1) fájl tesztelési stratégiáját és implementációját mutatja be. A modul az összes kivétel osztályt teszteli a `neural_ai.core.base.exceptions` csomagból.

## Tesztelt Komponensek

### 1. NeuralAIException
- **Teszt célja:** Az alap kivétel osztály helyes működésének ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel szövegének helyes létrehozását
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobásának mechanizmusát

### 2. StorageException
- **Teszt célja:** A tárolási kivétel hierarchia ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 3. StorageWriteError
- **Teszt célja:** Az írási hiba kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a StorageException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 4. StorageReadError
- **Teszt célja:** Az olvasási hiba kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a StorageException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 5. StoragePermissionError
- **Teszt célja:** A jogosultsági hiba kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a StorageException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 6. ConfigurationError
- **Teszt célja:** A konfigurációs hiba kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a NeuralAIException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 7. DependencyError
- **Teszt célja:** A függőségi hiba kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a NeuralAIException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 8. SingletonViolationError
- **Teszt célja:** A singleton megsértésének kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a NeuralAIException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 9. ComponentNotFoundError
- **Teszt célja:** A komponens nem található kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a NeuralAIException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 10. NetworkException
- **Teszt célja:** A hálózati kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a NeuralAIException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 11. TimeoutError
- **Teszt célja:** Az időtúllépési kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a NetworkException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 12. ConnectionError
- **Teszt célja:** A kapcsolódási hiba kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a NetworkException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 13. InsufficientDiskSpaceError
- **Teszt célja:** A lemezterület hiányának kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a StorageException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 14. PermissionDeniedError
- **Teszt célja:** A jogosultság megtagadásának kivétel ellenőrzése
- **Metódusok:**
  - `test_kivetel_letrehozasa`: Ellenőrzi a kivétel létrehozását és a StorageException öröklődését
  - `test_kivetel_okozasa`: Ellenőrzi a kivétel dobását

### 15. ExceptionHierarchy
- **Teszt célja:** A kivétel hierarchia teljes ellenőrzése
- **Metódusok:**
  - `test_storage_hierarchia`: Ellenőrzi a tárolási kivételek hierarchiáját
  - `test_network_hierarchia`: Ellenőrzi a hálózati kivételek hierarchiáját
  - `test_base_hierarchia`: Ellenőrzi az alap kivételek hierarchiáját

## Tesztelési Metrikák

### Coverage Eredmények
- **Statement Coverage:** 100%
- **Branch Coverage:** 100%
- **Modul:** `neural_ai.core.base.exceptions`

### Futtatási Statisztikák
- **Összes teszt:** 31
- **Sikeres tesztek:** 31
- **Sikertelen tesztek:** 0
- **Futási idő:** ~0.26s

## Kivétel Hierarchia

```
NeuralAIException
├── StorageException
│   ├── StorageWriteError
│   ├── StorageReadError
│   ├── StoragePermissionError
│   ├── InsufficientDiskSpaceError
│   └── PermissionDeniedError
├── ConfigurationError
├── DependencyError
├── SingletonViolationError
├── ComponentNotFoundError
└── NetworkException
    ├── TimeoutError
    └── ConnectionError
```

## Tesztelési Stratégia

### 1. Egységtesztek
Minden kivétel osztályhoz két alapvető teszt tartozik:
- **Létrehozási teszt:** Ellenőrzi, hogy a kivétel helyesen jön létre a megadott üzenettel
- **Dobási teszt:** Ellenőrzi, hogy a kivétel ténylegesen dobódik a várt módon

### 2. Hierarchia tesztek
A `TestExceptionHierarchy` osztály ellenőrzi, hogy a kivétel osztályok helyesen öröklődnek egymásból, és a hierarchia megfelel a tervezésnek.

### 3. Típusellenőrzés
Minden teszt ellenőrzi az `isinstance()` használatával, hogy a kivétel valóban a megfelelő szülőosztályból származik-e.

## Kódminőség

### Linter Eredmények
- **Ruff Check:** 0 hiba
- **Típusellenőrzés:** Minden metódus rendelkezik típus-hint-ekkel
- **Dokumentáció:** Minden tesztosztály és metódus rendelkezik magyar nyelvű docstringgel

### Best Practices
- **Arrange-Act-Assert minta:** Minden teszt követi a háromlépéses tesztelési mintát
- **Elnevezési konvenció:** A teszt metódusok nevei magyarul írják le a teszt célját
- **Függetlenség:** Minden teszt független és izoláltan futtatható

## Kapcsolódó Dokumentáció

- [Kivétel alaposztályok](../neural_ai/core/base/exceptions/base_error.md)
- [Kivétel modul](../neural_ai/core/base/exceptions/__init__.md)
- [Tesztelési útmutató](../../../../docs/development/TESTING_GUIDE.md)

## Verzió Történet

- **v1.0:** Kezdeti implementáció - 2025.12.26
  - 31 teszteset implementálva
  - 100% coverage elérve
  - Minden kivétel osztály tesztelve