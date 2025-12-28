# Core Config Tesztelés

Ez a dokumentáció a `core/config` modul tesztsuite-jének architektúráját és használatát mutatja be.

## Áttekintés

A `core/config` modul tesztsuite-je 177 tesztből áll, amelyek 89%-os kódlefedettséget érnek el. A tesztek három fő kategóriába sorolhatók:

1. **Implementáció tesztek** - A konkrét osztályok működésének ellenőrzése
2. **Interfész tesztek** - Az interfészek helyes definíciójának ellenőrzése
3. **Factory tesztek** - A factory mintázat helyes működésének ellenőrzése

## Tesztstruktúra

### Implementáció tesztek

#### `test_dynamic_config_manager.py`
- **Tesztosztályok:** 11
- **Tesztek száma:** 46
- **Leírás:** A `DynamicConfigManager` osztály teljes funkcionalitásának tesztelése

**Fontosabb tesztkategóriák:**
- Inicializálás és érvényesítés
- Get/Set műveletek
- Szekciókezelés
- Validáció
- Listener kezelés
- Hot reload funkcionalitás
- Metaadatok kezelése
- Törlés (soft delete)

#### `test_yaml_config_manager.py`
- **Tesztosztályok:** 2
- **Tesztek száma:** 52
- **Leírás:** A `YAMLConfigManager` osztály teljes funkcionalitásának tesztelése

**Fontosabb tesztkategóriák:**
- Validációs kontextus
- Inicializálás
- Get/Set műveletek
- Fájlkezelés (mentés, betöltés)
- Validáció (típus, range, choices)
- Mappabetöltés (load_directory)

### Interfész tesztek

#### `test_config_interface.py`
- **Tesztek száma:** 20
- **Leírás:** A `ConfigManagerInterface` interfész helyes definíciójának ellenőrzése

**Tesztelt tulajdonságok:**
- Absztrakt osztály ellenőrzése
- Absztrakt metódusok jelenléte
- Metódus aláírások helyessége
- Implementálhatóság
- Típusjelzések megőrzése
- Docstring jelenléte

#### `test_async_config_interface.py`
- **Tesztek száma:** 30
- **Leírás:** A `AsyncConfigManagerInterface` interfész helyes definíciójának ellenőrzése

**Tesztelt tulajdonságok:**
- Minden szinkron interfész teszt
- Aszinkron metódusok await-elhetősége
- ConfigListener típusalias
- Hot reload metódusok
- Metaadatok kezelésére vonatkozó metódusok

#### `test_factory_interface.py`
- **Tesztek száma:** 25
- **Leírás:** A `ConfigManagerFactoryInterface` interfész helyes definíciójának ellenőrzése

**Tesztelt tulajdonságok:**
- Classmethod dekorátorok jelenléte
- Regisztráció és létrehozás műveletek
- Többkezelős támogatás
- Hibakezelés

### Factory tesztek

#### `test_factory.py`
- **Tesztek száma:** 30
- **Leírás:** A `ConfigManagerFactory` konkrét implementációjának tesztelése

**Tesztelt funkcionalitások:**
- Manager létrehozás fájlkiterjesztés alapján
- Manager létrehozás explicit típus alapján
- Aszinkron manager létrehozás
- Hibakezelés
- Támogatott kiterjesztések és típusok
- Manager regisztráció

## Tesztelési szabványok

### Visszatérési típusok

Minden tesztmetódusnak kötelező a `-> None` visszatérési típus:

```python
def test_example(self) -> None:
    """Teszt példa."""
    # Teszt logika
```

### Típusjelzések

- Minden változónak legyen explicit típusjelzése
- Mock objektumokat annotálni kell: `mock_obj: MagicMock`
- `Any` típus használata tilos

### Aszinkron tesztek

Aszinkron tesztekhez kötelező a `@pytest.mark.asyncio` dekorátor:

```python
@pytest.mark.asyncio
async def test_async_method(self) -> None:
    """Aszinkron teszt."""
    result = await some_async_method()
    assert result == expected
```

### Docstring

Minden tesztmetódusnak kötelező magyar docstringgel rendelkeznie (Google Style):

```python
def test_example(self) -> None:
    """Teszteli a példa metódus működését.
    
    A teszt ellenőrzi, hogy a metódus helyesen dolgozza fel
    a bemeneti paramétereket és adja vissza a várt eredményt.
    """
```

## Futtatás

### Összes config teszt futtatása

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/config/ -v
```

### Coverage jelentés

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/config/ --cov=neural_ai.core.config --cov-report=term-missing
```

### Specifikus teszt futtatása

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/config/interfaces/test_config_interface.py -v
```

## Tesztadatok

### Konfigurációs fájlok

A tesztek a következő konfigurációs fájlokat használják:

- `tests/core/config/test_config.yaml` - Alap YAML konfiguráció
- `tests/core/config/test_config.xyz` - Ismeretlen kiterjesztésű fájl
- `tests/core/config/test_config` - Kiterjesztés nélküli fájl

### Mock objektumok

A tesztek a következő mock objektumokat használják:

- `AsyncMock` - Aszinkron session mock
- `MagicMock` - Logger és egyéb szolgáltatások mockja

## Hibakeresés

### Egy teszt futtatása

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/config/path/to/test.py::TestClass::test_method -v
```

### Debug módban futtatás

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/config/ -v --pdb
```

### Csak a bukott tesztek futtatása

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/config/ --lf
```

## Best Practices

1. **Tesztelj korai, tesztelj gyakran** - A CI/CD folyamat része legyen a tesztfuttatás
2. **Nevességi konvenciók** - Tesztmetódusok nevei legyenek leíróak
3. **Független tesztek** - Minden teszt fusson függetlenül a többitől
4. **Gyors tesztek** - A tesztek fussanak gyorsan, használj mockokat
5. **Magyar docstring** - Minden teszt legyen dokumentálva magyarul

## Metrikák

- **Összes teszt:** 177
- **Átlagos futási idő:** ~1-3 másodperc
- **Kódlefedettség:** 89%
- **Bukott tesztek:** 0 (állandó cél)

## Kapcsolódó dokumentációk

- [`ConfigManagerInterface`](interfaces/config_interface.md)
- [`AsyncConfigManagerInterface`](interfaces/async_config_interface.md)
- [`ConfigManagerFactoryInterface`](interfaces/factory_interface.md)
- [`DynamicConfigManager`](implementations/dynamic_config_manager.md)
- [`YAMLConfigManager`](implementations/yaml_config_manager.md)
- [`ConfigManagerFactory`](factory.md)