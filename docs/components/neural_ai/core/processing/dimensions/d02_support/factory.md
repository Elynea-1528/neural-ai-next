# D02SupportFactory

## Áttekintés

A `D02SupportFactory` a D02 Support/Resistance processzor factory osztálya, amely biztosítja a `D02SupportProcessor` példányok létrehozását Dependency Injection (DI) használatával.

## Architektúra

Ez az osztály a `neural_ai.core.processing.dimensions.d02_support` modul része.

## Funkcionalitás

### create Metódus

```python
@staticmethod
def create(config: ConfigManagerInterface, logger: LoggerInterface) -> IDimensionProcessor:
```

Létrehoz egy új `D02SupportProcessor` példányt a megadott konfigurációval és logger interfészekkel.

#### Paraméterek

- `config`: Konfigurációs menedzser interfész
- `logger`: Logger interfész

#### Visszatérési érték

`IDimensionProcessor` - A D02SupportProcessor példány

## Példa használata

```python
from neural_ai.core.processing.dimensions.d02_support import D02SupportFactory

processor = D02SupportFactory.create(config, logger)
```

## Függőségek

- `ConfigManagerInterface` - Konfiguráció kezelése
- `LoggerInterface` - Logolás
- `IDimensionProcessor` - Dimenzió processzor interfész