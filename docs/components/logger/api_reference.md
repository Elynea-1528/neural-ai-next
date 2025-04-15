# Logger Komponens API Referencia

## Interfaces

### LoggerInterface

A logger komponensek alap interfésze.

```python
class LoggerInterface(ABC):
    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        """Debug szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        pass

    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        """Információs szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        """Figyelmeztetés szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        pass

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        """Hiba szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs: Any) -> None:
        """Kritikus hiba szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        pass
```

### LoggerFactoryInterface

Logger példányok létrehozásáért felelős interfész.

```python
class LoggerFactoryInterface(ABC):
    @staticmethod
    @abstractmethod
    def get_logger(name: str, config: Optional[Dict[str, Any]] = None) -> LoggerInterface:
        """Logger példány létrehozása vagy meglévő visszaadása.

        Args:
            name: A logger neve
            config: Opcionális konfiguráció

        Returns:
            LoggerInterface: Logger példány
        """
        pass

    @staticmethod
    @abstractmethod
    def configure(config: Dict[str, Any]) -> None:
        """Globális logger konfiguráció beállítása.

        Args:
            config: A logger rendszer konfigurációja
        """
        pass
```

## Implementációk

### DefaultLogger

Alap naplózási funkciókat biztosító implementáció.

```python
class DefaultLogger(LoggerInterface):
    def __init__(self, name: str) -> None:
        """Logger inicializálása.

        Args:
            name: A logger neve
        """
        self._logger = logging.getLogger(name)
```

### ColoredLogger

Színes konzol kimenettel rendelkező implementáció.

```python
class ColoredLogger(LoggerInterface):
    def __init__(
        self,
        name: str,
        format_str: Optional[str] = None,
        stream: Optional[TextIO] = None
    ) -> None:
        """Logger inicializálása.

        Args:
            name: A logger neve
            format_str: Opcionális formátum string
            stream: Opcionális kimenet stream
        """
```

### RotatingFileLogger

Fájl alapú, rotációt támogató implementáció.

```python
class RotatingFileLogger(LoggerInterface):
    def __init__(
        self,
        name: str,
        filename: str,
        rotation_type: str = "size",
        max_bytes: int = 1024 * 1024,
        backup_count: int = 5,
        when: str = "midnight",
        encoding: str = "utf-8",
        format_str: Optional[str] = None,
        level: str = "DEBUG"
    ) -> None:
        """Logger inicializálása.

        Args:
            name: A logger neve
            filename: A log fájl útvonala
            rotation_type: Rotáció típusa ("size" vagy "time")
            max_bytes: Maximális fájlméret byte-okban
            backup_count: Backup fájlok száma
            when: Időalapú rotáció időpontja
            encoding: Fájl kódolás
            format_str: Opcionális formátum string
            level: Log szint
        """
```

## Formatters

### ColoredFormatter

Színes kimenet formázó.

```python
class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt: Optional[str] = None) -> None:
        """Formázó inicializálása.

        Args:
            fmt: Opcionális formátum string
        """
```

## Konfigurációs Opciók

### Alapértelmezett Konfiguráció

```yaml
default_level: "INFO"
format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format: "%Y-%m-%d %H:%M:%S"

handlers:
  console:
    enabled: true
    level: "INFO"
    colored: true

  file:
    enabled: true
    level: "DEBUG"
    filename: "logs/app.log"
    rotating: true
    max_bytes: 1048576  # 1MB
    backup_count: 5
```

### Konfigurációs Paraméterek

| Paraméter | Típus | Alapértelmezett | Leírás |
|-----------|-------|-----------------|---------|
| default_level | str | "INFO" | Alapértelmezett log szint |
| format | str | lásd fent | Log bejegyzések formátuma |
| date_format | str | "%Y-%m-%d %H:%M:%S" | Dátum formátum |
| handlers.console.enabled | bool | true | Konzol kimenet engedélyezése |
| handlers.console.colored | bool | true | Színes kimenet engedélyezése |
| handlers.file.enabled | bool | true | Fájl kimenet engedélyezése |
| handlers.file.rotating | bool | true | Log rotáció engedélyezése |
| handlers.file.max_bytes | int | 1048576 | Maximum fájlméret byte-okban |
| handlers.file.backup_count | int | 5 | Backup fájlok száma |

## Log Szintek

| Szint | Érték | Használat |
|-------|--------|-----------|
| DEBUG | 10 | Fejlesztési információk |
| INFO | 20 | Általános információk |
| WARNING | 30 | Figyelmeztetések |
| ERROR | 40 | Hibák |
| CRITICAL | 50 | Kritikus hibák |