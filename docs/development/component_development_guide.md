# Komponens Fejlesztési Útmutató

Ez az útmutató részletes leírást ad a Neural-AI-Next rendszerben új komponensek fejlesztéséhez. A dokumentum végigvezet a komponens tervezésétől a tesztelésig és dokumentálásig.

## 1. Komponens Tervezése

### 1.1. Követelmények meghatározása
- Mi a komponens pontos funkciója?
- Milyen interfészekkel fog rendelkezni?
- Milyen adatokat fogad és ad vissza?
- Milyen hibakezelési stratégiát alkalmaz?
- Milyen teljesítmény- és skálázhatósági követelményei vannak?

### 1.2. Interfész tervezése
1. Definiáld az interfészt egy absztrakt osztályban (`interfaces.py` fájlban)
2. Határozd meg a publikus metódusokat
3. Dokumentáld a paramétereket és visszatérési értékeket
4. Határozd meg a kivételeket

### 1.3. Komponens architektúra
- Tervezd meg a komponens belső struktúráját
- Azonosítsd a szükséges osztályokat és azok felelősségeit
- Határozd meg a függőségeket más komponensektől

## 2. Implementáció Lépései

### 2.1. Interfész definíció
```python
# példa egy interfész definícióra
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class ProcessorInterface(ABC):
    @abstractmethod
    def process(self, data: Any) -> Any:
        """
        Adatok feldolgozása.

        Args:
            data: Feldolgozandó adatok

        Returns:
            Feldolgozott adatok

        Raises:
            ProcessorError: Feldolgozási hiba esetén
        """
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Feldolgozási metaadatok lekérése.

        Returns:
            A feldolgozás metaadatai
        """
        pass
```

### 2.2. Komponens implementáció
```python
# példa egy implementációra
from neural_ai.core.logger import LoggerFactory
from neural_ai.processors.interfaces import ProcessorInterface

class TrendProcessor(ProcessorInterface):
    """
    Trend feldolgozó komponens.

    Ez a komponens piaci trend indikátorokat számít.
    """

    def __init__(self, config: Dict[str, Any], logger=None):
        self.config = config
        self.logger = logger or LoggerFactory.get_logger(__name__)
        self.window = config.get("window", 20)
        self._metadata = {}

        self.logger.info(f"{self.__class__.__name__} initialized with window={self.window}")

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Implementálja a trend feldolgozást.

        Args:
            data: OHLCV adatok pandas DataFrame-ben

        Returns:
            DataFrame trend indikátorokkal kiegészítve

        Raises:
            ProcessorError: Feldolgozási hiba esetén
        """
        try:
            self.logger.debug(f"Processing data with shape {data.shape}")
            # Implementáció...
            self._metadata = {...}  # Metaadatok tárolása
            return result
        except Exception as e:
            self.logger.error(f"Error processing trend: {e}")
            raise ProcessorError(f"Trend processing failed: {e}")

    def get_metadata(self) -> Dict[str, Any]:
        """
        Visszaadja a feldolgozás metaadatait.

        Returns:
            Feldolgozási metaadatok
        """
        return self._metadata
```

### 2.3. Factory osztály
```python
# példa egy factory osztályra
class ProcessorFactory:
    """Factory osztály a feldolgozók létrehozásához."""

    @staticmethod
    def create_processor(processor_type: str, config: Dict[str, Any]) -> ProcessorInterface:
        """
        Processzor példány létrehozása.

        Args:
            processor_type: Processzor típusa
            config: Konfiguráció

        Returns:
            ProcessorInterface: Processzor példány

        Raises:
            ValueError: Ismeretlen processzor típus esetén
        """
        if processor_type == "trend":
            return TrendProcessor(config)
        elif processor_type == "support_resistance":
            return SupportResistanceProcessor(config)
        else:
            raise ValueError(f"Unknown processor type: {processor_type}")
```

## 3. Tesztelés

### 3.1. Unit tesztek
Minden komponenshez készíts unit teszteket:

- Teszteld az interfész minden metódusát
- Teszteld a normál eseteket és a kivételes helyzeteket
- Használj mock objektumokat a függőségek helyettesítésére

```python
# példa unit teszt
import pytest
import pandas as pd
from neural_ai.processors import ProcessorFactory

def test_trend_processor_initialization():
    config = {"window": 30}
    processor = ProcessorFactory.create_processor("trend", config)
    assert processor.window == 30

def test_trend_processor_processing():
    # Test data preparation
    data = pd.DataFrame({...})  # Test data

    # Processing
    config = {"window": 20}
    processor = ProcessorFactory.create_processor("trend", config)
    result = processor.process(data)

    # Assertions
    assert "trend_strength" in result.columns
    assert not result["trend_strength"].isna().any()
    assert result.shape[0] == data.shape[0]
```
### 3.2. Integration tesztek
- Teszteld a komponens együttműködését más komponensekkel
- Ellenőrizd a teljes adatfolyamatot

## 4. Dokumentáció

### 4.1. Komponens dokumentáció
Minden komponenshez készíts dokumentációt a components könyvtárban:

- README.md: Áttekintés és főbb funkciók
- specification.md: Részletes specifikáció
- usage.md: Használati példák
- api.md: API dokumentáció
### 4.2. API dokumentáció
Dokumentáld az összes publikus interfészt:

- Metódusok paraméterei
- Visszatérési értékek
- Kivételek
- Példák
### 4.3. Példák
Készíts példákat a komponens használatára:

- Egyszerű használati esetek
- Összetettebb szcenáriók
- Hibakezelési példák

## 5. Ellenőrzőlista
Implementáció
- [ ] Interfész definiálása
- [ ] Implementáció elkészítése
- [ ] Factory osztály létrehozása vagy frissítése
- [ ] Konfigurációs paraméterek dokumentálása

Tesztelés
- [ ] Unit tesztek minden metódushoz
- [ ] Edge case tesztek
- [ ] Teljesítmény tesztek (ha kritikus)
- [ ] Integráció tesztek

Dokumentáció
- [ ] Komponens dokumentáció
- [ ] API dokumentáció
- [ ] Példák
- [ ] Konfigurációs lehetőségek dokumentálása

Review és merge
- [ ] Self-review
- [ ] Peer review
- [ ] CI tesztek sikeressége
- [ ] Dokumentáció frissítése a fő dokumentációban
