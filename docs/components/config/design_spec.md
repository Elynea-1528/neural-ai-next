<!-- filepath: /home/elynea/Dokumentumok/neural-ai-next/docs/components/config/README.md -->
# Konfigurációkezelő Komponens

## Áttekintés

A konfigurációkezelő komponens felelős a Neural-AI-Next rendszer különböző részeinek konfigurálásáért. Egységes interfészt biztosít a konfigurációs adatok kezeléséhez, többféle formátum támogatásával (YAML, JSON, stb.).

## Fő funkciók

- Konfigurációs fájlok betöltése és elemzése
- Konfigurációs értékek lekérése hierarchikus kulcsokkal
- Alapértelmezett értékek kezelése
- Konfigurációk validálása
- Konfigurációs változtatások mentése

## Architektúra

A konfigurációkezelő az alábbi komponensekből áll:

1. **ConfigManagerInterface**: Alap interfész a konfigurációkezeléshez
2. **ConfigManagerFactory**: Factory osztály a megfelelő implementáció létrehozásához
3. **Implementációk**:
   - YAMLConfigManager: YAML fájlok kezelése
   - JSONConfigManager: JSON fájlok kezelése
   - INIConfigManager: INI fájlok kezelése

## Használati példák

```python
# Konfiguráció betöltése
config_manager = ConfigManagerFactory.get_manager("configs/app.yaml")

# Értékek lekérése
log_level = config_manager.get("logging", "level", default="INFO")

# Teljes szekció lekérése
storage_config = config_manager.get_section("storage")

# Érték beállítása
config_manager.set("processing", "batch_size", 64)

# Konfiguráció mentése
config_manager.save()
```


## Konfigurációs fájl struktúra

A rendszer a következő konfigurációs fájl struktúrát használja:

/configs
├── app/                      # Alkalmazás szintű konfigurációk
│   ├── logging.yaml          # Logging beállítások
│   └── system.yaml           # Rendszer beállítások
├── collectors/               # Adatgyűjtő konfigurációk
│   ├── mt5.yaml
│   └── api.yaml
├── processors/               # Processzor konfigurációk
│   ├── d1_price_action.yaml
│   ├── d2_support_resistance.yaml
│   └── ...
└── storage/                  # Tároló konfigurációk
    └── storage.yaml

Konfiguráció validálás
A komponens opcionális validációs sémákat használhat a konfigurációs értékek ellenőrzésére:
```python
# Schema definíció
schema = {
    "logging": {
        "level": {"type": "string", "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]},
        "file": {"type": "string"}
    },
    "processing": {
        "batch_size": {"type": "integer", "min": 1, "max": 1024}
    }
}

# Validáció
is_valid, errors = config_manager.validate(schema)
if not is_valid:
    print(f"Configuration errors: {errors}")
```

## Fejlesztési útmutató
Új konfigurációkezelő implementáció létrehozásához:

1. Implementálja a ConfigManagerInterface interfészt
2. Regisztrálja az új implementációt a ConfigManagerFactory osztályban
3. Készítsen unit teszteket az új implementációhoz
