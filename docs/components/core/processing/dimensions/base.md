# BaseDimensionProcessor

## Áttekintés

Az absztrakt alap osztály minden dimenzió processzor számára. Dependency Injection támogatással biztosítja a konfigurációs kezelést és naplózást.

## Architektúra

```python
class BaseDimensionProcessor(IDimensionProcessor, ABC):
    def __init__(self, config: ConfigManagerInterface, logger: LoggerInterface):
        self.config = config
        self.logger = logger
        section = f"processors.d{self.dimension_id:02d}"
        self.dim_config = config.get_section(section) or {}
```

## Főbb Funkciók

- **Konfigurációs Betöltés**: Automatikusan betölti a dimenzió-specifikus konfigurációt
- **Dependency Injection**: Config és Logger interfészek injektálása
- **Hiba Kezelés**: Warning logolás hiányzó konfiguráció esetén

## Használat

Minden dimenzió processzor örököl ebből az osztályból:

```python
class D01PriceProcessor(BaseDimensionProcessor):
    @property
    def dimension_id(self) -> int:
        return 1
```

## Kapcsolódó Fájlok

- `neural_ai/core/processing/interfaces/dimension_processor_interface.py` - Interfész definíció
- `neural_ai/core/processing/dimensions/d01_price/processor.py` - Példa implementáció