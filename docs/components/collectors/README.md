# Neural AI - Collector Komponensek

## Áttekintés

A Collector komponensek felelősek különböző adatforrásokból történő adatgyűjtésért. Minden collector implementálja a `CollectorInterface`-t és a `CollectorFactory` segítségével hozható létre.

## Elérhető Collectorok

### MT5 Collector

Az MT5 Collector a MetaTrader 5 platformról gyűjt adatokat FastAPI szerveren keresztül.

**Főbb funkciók:**
- Valós idejű tick és OHLCV adatok gyűjtése
- Több instrumentum és időkeret támogatása
- Adatvalidáció és hibakezelés
- Integrált Data Warehouse kezelés

**Dokumentáció:** [MT5 Collector](mt5/README.md)

## Használat

### Alapvető használat

```python
from neural_ai.collectors.mt5 import CollectorFactory
from neural_ai.core.config import ConfigManagerFactory

# Konfiguráció betöltése
config = ConfigManagerFactory.get_manager("configs/collector_config.yaml")

# Collector létrehozása
collector = CollectorFactory.get_collector("mt5", config)

# Szerver indítása
await collector.start_server()
```

## Fejlesztés

### Új Collector implementálása

1. Hozz létre egy új mappát a `neural_ai/collectors/` alatt
2. Implementáld a `CollectorInterface`-t
3. Regisztráld a collector-t a `CollectorFactory`-ban
4. Készítsd el a szükséges dokumentációt

## Kapcsolódó komponensek

- [Logger](../logger/README.md) - Naplózás
- [Storage](../storage/README.md) - Adattárolás
- [Config](../config/README.md) - Konfigurációkezelés

## Licensz

MIT License - lásd a LICENSE fájlt a részletekért.
