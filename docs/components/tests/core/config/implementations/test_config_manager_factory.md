# ConfigManagerFactory Tesztelés

## Áttekintés

Ez a dokumentum a [`tests/core/config/implementations/test_config_manager_factory.py`](../tests/core/config/implementations/test_config_manager_factory.py:1) tesztfájl dokumentációja, amely a [`ConfigManagerFactory`](../../../neural_ai/core/config/factory.py:1) osztályt teszteli.

## Tesztelt Funkcionalitás

A tesztesetek a következő fő területeket fedik le:

### 1. Manager Regisztráció

- **`test_register_manager`**: Ellenőrzi, hogy egyéni manager osztályt lehet-e regisztrálni kiterjesztés alapján.
- **`test_register_manager_without_dot`**: Teszteli a pont nélküli kiterjesztések automatikus pont-hozzáadását.
- **`test_manager_types_dict_immutability`**: Ellenőrzi, hogy a `_manager_types` szótár globálisan módosul-e.

### 2. Manager Lekérés

- **`test_get_manager_by_yaml_extension`**: YAML kiterjesztésű fájlok kezelőjének lekérése.
- **`test_get_manager_by_yml_extension`**: YML kiterjesztésű fájlok kezelőjének lekérése.
- **`test_get_manager_by_path_object`**: Path objektummal történő lekérés.
- **`test_get_manager_with_explicit_type`**: Explicit típusmegadásos lekérés.
- **`test_get_manager_with_explicit_type_with_dot`**: Pontos explicit típusmegadás.
- **`test_get_manager_default_to_yaml_no_extension`**: Alapértelmezett YAML kezelő visszaadása.
- **`test_get_manager_with_temp_file`**: Ideiglenes fájlok kezelése.

### 3. Hibakezelés

- **`test_get_manager_unsupported_extension`**: Nem támogatott kiterjesztés esetén dobjon `ConfigLoadError`-t.
- **`test_get_manager_unknown_explicit_type`**: Ismeretlen explicit típus esetén dobjon hibát.
- **`test_create_manager_unknown_type`**: Ismeretlen típusú manager létrehozásakor dobjon hibát.

### 4. Manager Létrehozás

- **`test_create_manager_with_type`**: Manager létrehozása típus alapján.
- **`test_create_manager_with_type_and_args`**: Manager létrehozása argumentumokkal.
- **`test_create_manager_with_type_without_dot`**: Pont nélküli típusból történő létrehozás.

### 5. Egyéb Funkciók

- **`test_get_supported_extensions`**: Támogatott kiterjesztések listázása.
- **`test_case_insensitive_extension`**: Kis- és nagybetűérzéketlen kiterjesztés-egyeztetés.
- **`test_factory_singleton_behavior`**: Ellenőrzi, hogy mindig új példányt ad-e vissza a factory.

## Tesztstratégia

### Mockolás

A tesztek során a [`YAMLConfigManager`](../../../neural_ai/core/config/implementations/yaml_config_manager.py:1) `__init__` metódusát mockoljuk, hogy elkerüljük a tényleges fájlkezelést és inicializálást:

```python
with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
    manager = ConfigManagerFactory.get_manager("config.yaml")
    assert isinstance(manager, YAMLConfigManager)
    mock_init.assert_called_once_with(filename="config.yaml")
```

### Interface Ellenőrzés

A teszt egyéni manager osztályokat használ, amelyek implementálják a [`ConfigManagerInterface`](../../../neural_ai/core/config/interfaces/config_interface.py:1)-t, így biztosítva a helyes interfész használatát.

### Ideiglenes Fájlok

A `test_get_manager_with_temp_file` teszteset `tempfile.NamedTemporaryFile` használatával hoz létre ideiglenes fájlt, majd a teszt végén takarítja azt.

## Metrikák

- **Tesztesetek száma**: 19
- **Átmenő tesztek**: 19/19 ✅
- **Coverage**: 100% (Statement: 100% | Branch: 100%)
- **Linter**: `ruff check` 0 hiba

## Függőségek

- [`neural_ai.core.config.factory`](../../../neural_ai/core/config/factory.py:1)
- [`neural_ai.core.config.implementations.yaml_config_manager`](../../../neural_ai/core/config/implementations/yaml_config_manager.py:1)
- [`neural_ai.core.config.interfaces.config_interface`](../../../neural_ai/core/config/interfaces/config_interface.py:1)
- [`neural_ai.core.config.exceptions`](../../../neural_ai/core/config/exceptions/config_error.py:1)

## Futtatás

A teszteket a következő paranccsal lehet futtatni:

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/config/implementations/test_config_manager_factory.py -v
```

Coverage reporttal együtt:

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/config/implementations/test_config_manager_factory.py -v --cov=neural_ai.core.config.factory --cov-report=term-missing
```

## Státusz

✅ **STABIL** - Minden teszt átmegy, 100%-os coverage-val rendelkezik, és megfelel az architektúra szabványoknak.