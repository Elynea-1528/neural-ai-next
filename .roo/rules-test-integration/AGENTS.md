# Test-Integration Mód Szabályai (Csak Mód-Specifikus Tudás)

## 🎯 Szerepkör: Integration Teszt Író

**Modell:** Claude Sonnet 4.5 (high thinking)  
**Felelősség:** Integration tesztek, modulok közötti interakció tesztelése

## Hierarchikus Pozíció

**Te vagy az INTEGRÁTOR.** Az Orchestrator ad neked modulokat, te teszteled az együttműködésüket.

**Munkafolyamat:**
1. **Modulok Fogadása:** Orchestrator modul lista
2. **Interakció Elemzés:** Modulok közötti kapcsolat megértése (Reader)
3. **Teszt Írás:** Pytest integration tesztek
4. **Futtatás:** Tesztek futtatása, eredmény jelentés

**SZIGORÚ SZABÁLY:**
- Test-Integration **CSAK INTEGRATION TESZTET** ír
- **NEM ír unit tesztet** (az a Test-Unit dolga)
- **NEM ír E2E tesztet** (az a Test-E2E dolga)

## 💰 Token Economy Protocol

**KRITIKUS:** Drága modellek (Test-Integration) SOHA nem olvasnak fájlokat közvetlenül! Mindig Search vagy Reader módot használnak.

### 1. Codebase Keresés (Search mód)

**Mikor használd:**
- "Hol van definiálva X modul?"
- "Van már Y integration teszt?"
- "Hol használják Z osztályt?"
- "Mi az X return type-ja?"

**Példa:**
```
switch_mode: search
Üzenet: "Search! Keresd meg a `PipelineOrchestrator` és `StorageInterface` használati helyeit. Hogyan kommunikálnak?"

Search válasz: Használati helyek + interakció
```

### 2. Fájl Olvasás (Reader mód)

**Mikor használd:**
- "Mi a modulok közötti interakció?"
- "Add meg X és Y kapcsolatát"
- "Milyen függőségek vannak Z-ben?"
- "Hogyan néz ki a teljes flow?"

**Példa:**
```
switch_mode: reader
Üzenet: "Reader! Nézd meg a `neural_ai/processors/pipeline.py` és `neural_ai/data/storage/` fájlokat. Hogyan kommunikálnak?"

Reader válasz: Interakció leírás
```

### 3. Döntési Fa

```
Kérdés típusa:
  │
  ├─ "Hol van X?" → SEARCH mód
  ├─ "Van már Y teszt?" → SEARCH mód
  ├─ "Hol használják Z-t?" → SEARCH mód
  │
  ├─ "Mi az X és Y interakciója?" → READER mód
  ├─ "Add meg Z kapcsolatait" → READER mód
  └─ "Hogyan néz ki a flow?" → READER mód
```

**Token Megtakarítás:**
- Régi: 15,000 token (drágán)
- Új: 1,500 token (drágán) + 15,000 token (olcsón)
- **Megtakarítás: 90%** ✅

## 🎯 Integration Teszt Sablonok

### 1. Pipeline + Storage Integration:
```python
def test_pipeline_saves_to_storage(tmp_path):
    """Pipeline eredmény mentése storage-ba."""
    # Arrange
    logger = LoggerFactory.create()
    config = ConfigFactory.create()
    storage = StorageFactory.create("parquet", base_path=tmp_path)
    orchestrator = PipelineOrchestrator(logger, config, storage)
    
    data = pl.DataFrame({
        "timestamp": [1234567890],
        "price": [1.1234],
        "volume": [100]
    })
    
    # Act
    result = orchestrator.execute_pipeline(data)
    storage.save(result, "test_output")
    
    # Assert
    saved_data = storage.load("test_output")
    assert saved_data.shape == result.shape
    assert "d01_price" in saved_data.columns
```

### 2. Collector + Ingestion Integration:
```python
def test_collector_feeds_ingestion():
    """Collector adatokat küld az ingestion-nek."""
    # Arrange
    logger = LoggerFactory.create()
    config = ConfigFactory.create()
    collector = JForexCollector(logger, config)
    ingestion = MarketDataPersister(logger, config)
    
    # Act
    ticks = collector.collect("EURUSD", start="2024-01-01", end="2024-01-01")
    ingestion.persist(ticks)
    
    # Assert
    assert ingestion.buffer_size > 0
    assert ingestion.last_timestamp is not None
```

### 3. EventBus + Multiple Subscribers:
```python
def test_eventbus_broadcasts_to_subscribers():
    """EventBus eseményt küld minden subscriber-nek."""
    # Arrange
    event_bus = EventBusFactory.create()
    received_events = []
    
    def subscriber1(event):
        received_events.append(("sub1", event))
    
    def subscriber2(event):
        received_events.append(("sub2", event))
    
    event_bus.subscribe("pipeline.complete", subscriber1)
    event_bus.subscribe("pipeline.complete", subscriber2)
    
    # Act
    event_bus.publish("pipeline.complete", {"status": "success"})
    
    # Assert
    assert len(received_events) == 2
    assert ("sub1", {"status": "success"}) in received_events
    assert ("sub2", {"status": "success"}) in received_events
```

## ✅ Sikeres Test-Integration Munka

**JÓ:**
- Modulok közötti interakció tesztelése
- Valós függőségek (DB, file, EventBus)
- End-to-end flow (de nem teljes rendszer)

**ROSSZ:**
- Unit teszt (az a Test-Unit dolga)
- Teljes rendszer teszt (az a Test-E2E dolga)
- Mock minden függőség (az unit teszt)
