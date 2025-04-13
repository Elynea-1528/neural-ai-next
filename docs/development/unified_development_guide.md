# Neural-AI-Next Egységes Fejlesztési Útmutató

## 1. Bevezetés

Ez az útmutató tartalmazza a Neural-AI-Next projekt fejlesztési szabványait, konvencióit és best practice-eit. Minden fejlesztőnek követnie kell ezt az útmutatót a kód konzisztenciájának és minőségének biztosítása érdekében.

## 2. Komponens Architektúra

### 2.1 Interfész-alapú fejlesztés

Minden fő komponenshez definiáljunk először interfészt, amely meghatározza a komponens viselkedését. Ez a megközelítés:

- Elkerüli a körkörös importokat
- Egyszerűsíti a tesztelést mockolt komponensekkel
- Biztosítja a komponensek cserélhetőségét

```python
# Példa interfész struktúra
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class ComponentInterface(ABC):
    @abstractmethod
    def main_operation(self, input_data: Any) -> Any:
        """Fő működési metódus leírása."""
        pass
```
### 2.2 Factory pattern használata

Minden komponenshez használjunk factory osztályt a példányok létrehozásához:

```python
class ComponentFactory:
    @staticmethod
    def get_component(component_type: str, config: Dict[str, Any]) -> ComponentInterface:
        if component_type == "type1":
            return Type1Component(config)
        elif component_type == "type2":
            return Type2Component(config)
        else:
            raise ValueError(f"Ismeretlen komponens típus: {component_type}")
```

### 2.3 Dependency Injection

A komponenseket úgy kell megtervezni, hogy függőségeiket kívülről kapják:

```python
class Processor:
    def __init__(self, config: Dict[str, Any], logger=None, storage=None):
        self.config = config
        self.logger = logger or LoggerFactory.get_logger(__name__)
        self.storage = storage or StorageFactory.get_storage(config)
```
## 3. Kódolási Szabványok

### 3.1 Kód formázás és stílus

- Fájlok és modulok: snake_case (pl. data_processor.py)
- Osztályok: PascalCase (pl. DataProcessor)
- Függvények és változók: snake_case (pl. process_data)
- Konstansok: UPPERCASE_WITH_UNDERSCORES (pl. MAX_RETRY_COUNT)
- Maximális sorhossz: 100 karakter
- Behúzás: 4 szóköz (ne tab)
- Import sorrend:
    1. Standard könyvtárak
    2. Külső függőségek
    3. Projekt modulok

### 3.2 Docstrings

Minden osztályhoz, metódushoz és függvényhez használjunk Google stílusú docstringet:

```python
def calculate_moving_average(data: np.ndarray, window: int = 20) -> np.ndarray:
    """
    Kiszámítja a mozgóátlagot egy adatsorozatra.

    Args:
        data: Idősor adatok
        window: Ablakméret a mozgóátlaghoz

    Returns:
        Mozgóátlaggal kiegészített adatok

    Raises:
        ValueError: Ha az ablakméret nagyobb, mint az adatok hossza
    """
```
### 3.3 Hibakezelés

- Minden lehetséges hibát explicit kezeljünk
- Használjunk specifikus kivételosztályokat
- A hibákat megfelelően loggoljuk
- Kritikus szakaszokhoz használjunk try-except blokkokat

```python
try:
    data = self.process_data(input_data)
except DataProcessingError as e:
    self.logger.error(f"Adatfeldolgozási hiba: {e}")
    raise
except Exception as e:
    self.logger.critical(f"Váratlan hiba: {e}")
    raise SystemError(f"Rendszerhiba a feldolgozás során: {e}")
```
## 4. Komponensek Egységes Használata

### 4.1 Logger

A loggert minden komponens egységesen használja:

```python
# Logger inicializálása
self.logger = logger or LoggerFactory.get_logger(__name__)

# Logger használata
self.logger.debug("Részletes diagnosztikai információ")
self.logger.info("Általános információs üzenet")
self.logger.warning("Figyelmeztetés, ami nem akadályozza a működést")
self.logger.error("Hiba, ami megakadályozza egy művelet végrehajtását")
self.logger.critical("Kritikus hiba, ami a rendszer leállását okozhatja")
```

### 4.2 Config Manager

A konfigurációkezelő egységes használata:

```python
# Config inicializálása
self.config = config or ConfigManagerFactory.get_manager("configs/default.yaml")

# Config használata
log_level = self.config.get("logging", "level", "INFO")
batch_size = self.config.get("processing", "batch_size", 100)

# Config szekció lekérése
storage_config = self.config.get_section("storage")
```
### 4.3 Storage

Az adattároló komponens egységes használata:

```python
# Storage inicializálása
self.storage = storage or StorageFactory.get_storage(storage_config)

# Storage használata - adatok mentése
await self.storage.save_raw_data(data_frame, symbol, timeframe)

# Storage használata - adatok betöltése
data = await self.storage.load_raw_data(symbol, timeframe)
```
### 4.4 Processorok

Az adatfeldolgozók egységes használata:

```python
# Processor létrehozása
processor = ProcessorFactory.create_processor("d1_price_action", config)

# Processor használata
features = processor.process(raw_data)
```
## 5. Tesztelési Előírások

### 5.1 Unit tesztek

Minden komponenshez készítsünk unit teszteket:
```python
# pytest használatával
def test_processor_initialization():
    config = {"parameter": "value"}
    processor = TestProcessor(config)
    assert processor.parameter == "value"

def test_processor_processing():
    processor = TestProcessor(test_config)
    result = processor.process(test_data)
    assert result.shape[0] == test_data.shape[0]
```
### 5.2 Integration tesztek
Komponensek együttműködésének tesztelése:

```python
def test_data_flow():
    collector = CollectorFactory.get_collector("mt5", collector_config)
    processor = ProcessorFactory.create_processor("trend", processor_config)

    data = collector.collect("EURUSD", "M1")
    processed_data = processor.process(data)

    assert processed_data is not None
    assert "trend_strength" in processed_data.columns
```
## 6. Dokumentációs Szabványok

### 6.1 Komponens dokumentáció

Minden komponenshez készítsünk részletes dokumentációt a /docs/components/ könyvtárban:

/docs/components/[komponens_név]/
  ├── README.md         # Áttekintés és használati útmutató
  ├── api.md            # API dokumentáció
  ├── architecture.md   # Architektúra leírás
  ├── design_spec.md   # Tervezési specifikáció
  └── examples.md       # Használati példák

### 6.2 API dokumentáció
Az API dokumentáció tartalmazza:

- A komponens által nyújtott publikus interfészek leírását
- A metódusok paramétereit és visszatérési értékeit
- Példakódokat a használathoz
- Lehetséges hibák és kezelésük

## 7. Workflow és Pull Request Szabályok

### 7.1 Feature fejlesztés workflow
1. Hozz létre egy új branch-et a feature-höz: feature/ISSUE-ID-short-description
2. Implementáld a változtatásokat
3. Írj unit teszteket
4. Frissítsd a dokumentációt
5. Commitolj a konvenciók szerint
6. Nyiss Pull Request-et a develop branch-be

### 7.2 Pull Request szabályok
Minden PR-nek tartalmaznia kell:

- Világos leírást a változtatásokról
- Az érintett komponensek listáját
- Az új vagy frissített teszteket
- A kapcsolódó dokumentációs változtatásokat

## 8. Monitoring és Teljesítmény

### 8.1 Kód teljesítmény

- Minden kritikus komponenst benchmarkoljunk
- Az eredményeket dokumentáljuk a komponens dokumentációjában
- Teljesítmény regresszió esetén vizsgáljuk meg a változások hatását

### 8.2 Rendszer monitoring

- A rendszerkomponenseknek monitorozhatónak kell lenniük
- Minden kritikus művelethez mérjük az időt és erőforrás-használatot
- A metrikákat strukturáltan loggoljuk

```python
start_time = time.time()
result = self.process_large_dataset(data)
processing_time = time.time() - start_time

self.logger.info(
    "Nagy adathalmaz feldolgozva",
    processing_time=processing_time,
    data_size=len(data),
    memory_used=get_memory_usage()
)
```
