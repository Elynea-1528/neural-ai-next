# ILiveFeed Interface

## Áttekintés

Az `ILiveFeed` interfész definiálja a JForex live adatfolyam kezeléséhez szükséges metódusokat. Ez az interfész biztosítja a konzisztens viselkedést minden live feed implementáció számára.

## Cél

Az interfész célja, hogy:
- Standardizálja a live feed komponensek viselkedését
- Lehetővé tegye a dependency injection-t
- Egyszerűsítse a tesztelést mock objektumokkal
- Biztosítsa a típusbiztosságot

## Interfész definíció

```python
from abc import ABC, abstractmethod


class ILiveFeed(ABC):
    """Absztrakt osztály a JForex live adatfolyam kezeléséhez."""
    
    @abstractmethod
    async def start(self) -> None:
        """Indítja a live adatfolyam fogadását."""
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """Leállítja a live adatfolyam fogadását."""
        pass
    
    @abstractmethod
    def is_running(self) -> bool:
        """Visszaadja, hogy a live feed jelenleg fut-e."""
        pass
```

## Metódusok

### `start()`

**Szignatúra:** `async def start(self) -> None`

Indítja a live adatfolyam fogadását. Ez a metódus felelős a kommunikációs csatorna létrehozásáért és a háttérfolyamat elindításáért.

**Előfeltételek:**
- A konfigurációban megadott host és port elérhető
- A szükséges erőforrások (pl. ZMQ context) létrehozhatók

**Utófeltételek:**
- A kommunikációs csatorna aktív
- A háttérfolyamat fut és fogadja az üzeneteket
- Az `is_running()` metódus `True`-t ad vissza

**Kivételek:**
- `LiveFeedError`: Ha a csatlakozás vagy a fogadás indítása sikertelen

### `stop()`

**Szignatúra:** `async def stop(self) -> None`

Leállítja a live adatfolyam fogadását. Ez a metódus felelős a kommunikációs csatorna lezárásáért és a háttérfolyamat leállításáért.

**Előfeltételek:**
- A feed jelenleg fut (vagy nem, ekkor nem csinál semmit)

**Utófeltételek:**
- A kommunikációs csatorna lezárult
- A háttérfolyamat leállt
- Az `is_running()` metódus `False`-t ad vissza
- Minden erőforrás felszabadult

**Kivételek:**
- Nincs (a metódusnak hibatűrőnek kell lennie)

### `is_running()`

**Szignatúra:** `def is_running(self) -> bool`

Visszaadja a live feed aktuális futási állapotát.

**Visszatérési érték:**
- `bool`: `True`, ha a feed jelenleg fut, `False` egyébként

**Előfeltételek:**
- Nincs

**Utófeltételek:**
- A visszaadott érték pontos tükrözi a feed aktuális állapotát

## Implementációs jegyzetek

### Élettartam kezelés

Az implementációknak kezelniük kell a következő élettartam eseményeket:

1. **Inicializálás**: A konstruktorban be kell állítani az alapértelmezett állapotot
2. **Start**: A `start()` metódusnak kell létrehoznia a szükséges erőforrásokat
3. **Futás**: A háttérfolyamatnak folyamatosan kell fogadnia és feldolgoznia az üzeneteket
4. **Stop**: A `stop()` metódusnak kell felszabadítania az összes erőforrást
5. **Újraindítás**: Lehetővé kell tenni a stop után történő újraindítást

### Hibatűrés

Az implementációknak hibatűrőnek kell lenniük:

- **Start hiba**: Ha a start sikertelen, az összes erőforrást felszabadítani kell
- **Futás közbeni hiba**: A háttérfolyamatnak nem szabad összeomlania hibák miatt
- **Stop hiba**: A stop metódusnak minden körülmények között le kell állítania a feedet

### Aszinkron működés

Minden metódus aszinkron, ezért az implementációknak:
- `async/await` szintaxist kell használniuk
- Aszinkron I/O műveleteket kell végezniük
- Nem blokkoló műveleteket kell használniuk

## Használati minta

```python
from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed


class MyLiveFeed(ILiveFeed):
    """Saját live feed implementáció."""
    
    def __init__(self, config):
        self._running = False
        self._config = config
    
    async def start(self) -> None:
        """Indítja a live feedet."""
        if self._running:
            return
        
        # Implementáció specifikus logika
        await self._setup_connection()
        self._running = True
        self._listen_task = asyncio.create_task(self._listen_loop())
    
    async def stop(self) -> None:
        """Leállítja a live feedet."""
        if not self._running:
            return
        
        self._running = False
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass
        
        await self._close_connection()
    
    def is_running(self) -> bool:
        """Visszaadja a futási állapotot."""
        return self._running
    
    async def _setup_connection(self):
        """Kapcsolat létrehozása (implementáció specifikus)."""
        pass
    
    async def _close_connection(self):
        """Kapcsolat lezárása (implementáció specifikus)."""
        pass
    
    async def _listen_loop(self):
        """Háttérfolyamat (implementáció specifikus)."""
        while self._running:
            # Üzenetek fogadása és feldolgozása
            pass
```

## Tesztelés

Az interfész implementációit a következőképpen lehet tesztelni:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock


class TestILiveFeed:
    """ILiveFeed implementációk tesztelése."""
    
    def test_start_stop_cycle(self):
        """Teszteli a start-stop ciklust."""
        feed = MyLiveFeed(config=MagicMock())
        
        # Kezdetben nem fut
        assert not feed.is_running()
        
        # Start után fut
        await feed.start()
        assert feed.is_running()
        
        # Stop után nem fut
        await feed.stop()
        assert not feed.is_running()
    
    def test_double_start_handling(self):
        """Teszteli a dupla start kezelését."""
        feed = MyLiveFeed(config=MagicMock())
        
        await feed.start()
        assert feed.is_running()
        
        # Dupla start nem okozhat hibát
        await feed.start()
        assert feed.is_running()
    
    def test_stop_when_not_running(self):
        """Teszteli a stop hívását, ha nem fut."""
        feed = MyLiveFeed(config=MagicMock())
        
        # Stop hívás nem futó feeden nem okozhat hibát
        await feed.stop()
        assert not feed.is_running()
```

## Implementációk

- [JForexLiveFeed](../implementations/live_feed.md): ZMQ-alapú implementáció a Java Bridge-hez

## Kapcsolódó dokumentáció

- [JForex Collector Áttekintés](../index.md)
- [Dependency Injection Pattern](../../../core/base/implementations/di_container.md)
- [EventBus Interface](../../../core/events/interfaces/event_bus_interface.md)