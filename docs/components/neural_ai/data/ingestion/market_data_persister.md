# neural_ai/data/ingestion/market_data_persister.py

MarketDataPersister - Piaci adatok persistáló szolgáltatás.

Ez az osztály felelős a piaci adatok (tick adatok) gyűjtéséért és persistálásáért
az adatfolyamból. Aszinkron módon dolgozza fel az eseményeket, pufferezéssel és
időszakos flush mechanizmussal biztosítja az adatvesztés minimalizálását.

## Osztályok

### `MarketDataPersister`

Piaci adatok persistáló szolgáltatás eseményalapú feldolgozással.

Ez az osztály implementálja a piaci adatok gyűjtését és tárolását buffereléssel
és időalapú flush mechanizmussal. Event-driven architektúrát használ a
valós idejű adatfolyam feldolgozásához.

Attributes:
    buffer_size: A buffer maximális mérete flush előtt
    flush_interval: Időintervallum másodpercben az automatikus flush-hoz
    symbol_buffers: Szimbólum alapú adat buffer-ek
    storage_service: A tárolási szolgáltatás interfésze

## Főbb metódusok

- `start`: Szolgáltatás indítása
- `stop`: Szolgáltatás leállítása
- `on_market_data`: Új piaci adat esemény feldolgozása
- `flush_all_buffers`: Összes buffer flush-ölése
- `periodic_flush`: Időszakos flush feladat

---

**Forrásfájl:** [`neural_ai/data/ingestion/market_data_persister.py`](../../../neural_ai/data/ingestion/market_data_persister.py)