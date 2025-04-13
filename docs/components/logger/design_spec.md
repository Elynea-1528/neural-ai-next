# Logger Komponens Specifikáció

## Áttekintés

A Logger komponens a Neural-AI-Next rendszer egyik alapvető infrastruktúra eleme, amely felelős a rendszer működése során keletkező események, információk és hibák strukturált rögzítéséért. A cél egy egységes, konfigurálható és kiterjeszthető naplózási mechanizmus biztosítása, amely támogatja a fejlesztést, hibaelhárítást és a rendszer működésének monitorozását.

## Fő funkciók

- Különböző részletességi szintű naplózás támogatása (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Többféle kimeneti formátum és cél támogatása (konzol, fájl, hálózat)
- Strukturált naplózás extra kontextus információkkal
- Hierarchikus logger struktúra (modul/almodul szintű logolás)
- Konfigurálható formátumok és szűrők
- Teljesítményoptimalizált működés

## Architektúra

A Logger komponens az alábbi fő részekből áll:

1. **LoggerInterface**: Az alapvető naplózási funkcionalitást definiáló interfész
2. **LoggerFactoryInterface**: Logger példányok létrehozásáért felelős interfész
3. **Implementációk**:
   - DefaultLogger: Python stdlib logging alapú alap implementáció
   - FileLogger: Fájl alapú naplózás
   - ConsoleLogger: Konzol kimenet
   - NetworkLogger: Távoli naplózás
4. **LoggerFactory**: Különböző logger implementációk példányosítása

## Interfészek

### LoggerInterface

```python
class LoggerInterface(ABC):
    @abstractmethod
    def debug(self, message: str, **kwargs) -> None:
        """Debug szintű üzenet logolása."""
        pass

    @abstractmethod
    def info(self, message: str, **kwargs) -> None:
        """Információs szintű üzenet logolása."""
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs) -> None:
        """Figyelmeztetés szintű üzenet logolása."""
        pass

    @abstractmethod
    def error(self, message: str, **kwargs) -> None:
        """Hiba szintű üzenet logolása."""
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs) -> None:
        """Kritikus hiba szintű üzenet logolása."""
        pass
```

### LoggerFactoryInterface

```python
class LoggerFactoryInterface(ABC):
    @staticmethod
    @abstractmethod
    def get_logger(name: str, config: Optional[Dict[str, Any]] = None) -> LoggerInterface:
        """Logger példány létrehozása vagy meglévő visszaadása."""
        pass

    @staticmethod
    @abstractmethod
    def configure(config: Dict[str, Any]) -> None:
        """Globális logger konfiguráció beállítása."""
        pass
```
## Használati esetek
1. Alkalmazás szintű naplózás:

- Rendszerindulás és leállás
- Komponensek inicializálása
- Állapotváltozások
2. Hibakövetés és debugging:

- Kivételek és hibák részletes rögzítése
- Diagnosztikai információk
3. Üzleti logika naplózása:

- Fontos esemény és adat változások
- Döntési pontok és eredmények
4. Teljesítménymérés:

- Műveletek időtartama
- Erőforrás-használat

## Konfiguráció

A Logger komponens konfigurálása a configs/logging.yaml fájlban történik:

```yaml
logger:
  default_level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  date_format: "%Y-%m-%d %H:%M:%S"
  handlers:
    console:
      enabled: true
      level: INFO
    file:
      enabled: true
      level: DEBUG
      filename: "logs/app.log"
      max_size: 10485760  # 10MB
      backup_count: 5
    network:
      enabled: false
      level: WARNING
      host: "logserver.example.com"
      port: 9999
```
## Teljesítmény követelmények
- A naplózás nem befolyásolhatja jelentősen a rendszer teljesítményét
- A kritikus szakaszokban a naplózás aszinkron módon történik
- Nagy mennyiségű log esetén is hatékony működés
## Biztonsági szempontok
- Érzékeny adatok automatikus maszkolása
- Log rotáció és tisztítási szabályok
- Hozzáférés-szabályozás a log fájlokhoz
## Függőségek
- Python standard könyvtár (logging)
- ConfigManagerInterface a konfigurációhoz
