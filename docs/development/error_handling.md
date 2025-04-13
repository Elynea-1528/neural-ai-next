<!-- filepath: /home/elynea/Dokumentumok/neural-ai-next/docs/development/error_handling.md -->
# Hibakezelési Útmutató

Ez az útmutató részletezi a Neural-AI-Next projektben alkalmazandó hibakezelési stratégiákat és bevált gyakorlatokat.

## 1. Alapelvek

### 1.1 Specifikus kivételek használata

Minden komponenshez specifikus kivételosztályokat definiálunk, amelyek az adott komponens kontextusában jelentkező hibák pontosabb azonosítását teszik lehetővé.

```python
class ProcessorError(Exception):
    """Processzor komponenshez tartozó alap kivétel."""
    pass

class ValidationError(ProcessorError):
    """Adatvalidációs hiba."""
    pass

class CalculationError(ProcessorError):
    """Számítási hiba a processzor működése során."""
    pass
```
### 1.2 Hierarchikus kivételkezelés
A kivételeket hierarchikus struktúrában kell szervezni, hogy a hívó kód rugalmasan kezelhesse azokat különböző absztrakciós szinteken.
```python
# Alap komponens kivételek
class ComponentError(Exception):
    pass

# Komponens specifikus kivételek
class StorageError(ComponentError):
    pass
class ProcessorError(ComponentError):
    pass
class ModelError(ComponentError):
    pass

# Részletes hibák
class StorageReadError(StorageError):
    pass
class StorageWriteError(StorageError):
    pass
```

### 1.3 Kontextus információk
A kivételeknek mindig tartalmazniuk kell elegendő információt a probléma diagnosztizálásához:
```python
try:
    result = processor.process(data)
except ValidationError as e:
    # Kontextus információk hozzáadása
    raise ValidationError(
        f"Validation error for {symbol} {timeframe}: {str(e)}"
    ) from e
```
### 1.4 Kivételek dokumentálása
Minden publikus metódus docstringjében dokumentálni kell a lehetséges kivételeket:
```python
def process_data(self, data: pd.DataFrame) -> pd.DataFrame:
    """
    Adatok feldolgozása.

    Args:
        data: Feldolgozandó adatok DataFrame formátumban

    Returns:
        Feldolgozott adatok

    Raises:
        ValidationError: Ha a bemeneti adatok érvénytelenek
        CalculationError: Ha hiba történik a számítás során
        ProcessorError: Egyéb processzálási hibák esetén
    """
```
## 2. Hibakezelési minták

### 2.1 Alap hibakezelési minta
```python
try:
    # Művelet végrehajtása
    result = self._process_implementation(data)
    return result
except ValidationError as e:
    # Validációs hibák kezelése
    self.logger.error(f"Validation error: {e}")
    raise
except ProcessorError as e:
    # Processzor specifikus hibák kezelése
    self.logger.error(f"Processing error: {e}")
    raise
except Exception as e:
    # Váratlan hibák kezelése
    self.logger.critical(f"Unexpected error: {e}", exc_info=True)
    raise ProcessorError(f"Unexpected error during processing: {e}") from e
```

### 2.2 Újrapróbálkozási stratégia
Ideiglenes hibák kezelésére újrapróbálkozási mechanizmus:
```python
def retry_operation(operation, max_retries=3, retry_delay=1):
    """
    Művelet újrapróbálása hiba esetén.

    Args:
        operation: A végrehajtandó függvény
        max_retries: Maximum újrapróbálkozások száma
        retry_delay: Késleltetés másodpercekben próbálkozások között

    Returns:
        A művelet eredménye

    Raises:
        Az utolsó kísérlet kivétele
    """
    last_exception = None
    for attempt in range(max_retries):
        try:
            return operation()
        except (ConnectionError, TimeoutError) as e:
            last_exception = e
            wait_time = retry_delay * (2 ** attempt)  # Exponenciális backoff
            logger.warning(f"Operation failed, retrying in {wait_time}s. "
                          f"Attempt {attempt+1}/{max_retries}. Error: {e}")
            time.sleep(wait_time)

    # Ha minden próbálkozás sikertelen volt
    raise last_exception
```
### 2.3 Fallback mechanizmusok
Kritikus komponensek számára fallback mechanizmusok:
```python
try:
    data = primary_data_source.get_data(symbol, timeframe)
except DataSourceError:
    logger.warning("Primary data source failed, trying fallback source")
    try:
        data = fallback_data_source.get_data(symbol, timeframe)
    except DataSourceError as e:
        logger.error("Fallback data source also failed")
        raise DataNotAvailableError(f"No data available for {symbol} {timeframe}") from e
```

## 3. Naplózási irányelvek
### 3.1 Hibaszintek megfelelő használata
- DEBUG: Részletes diagnosztikai információk
- INFO: Normál működés megerősítése
- WARNING: Potenciális problémák, amelyek nem akadályozzák a működést
- ERROR: Hibák, amelyek megakadályozzák egy adott művelet végrehajtását
- CRITICAL: Súlyos hibák, amelyek a rendszer leállását okozhatják

### 3.2 Strukturált naplózás
Használjunk strukturált naplózást a könnyebb kereshetőség érdekében:
```python
# Egyszerű üzenet helyett
logger.error(f"Processing failed for {symbol} {timeframe}: {e}")

# Strukturált naplózás
logger.error(
    "Processing failed",
    extra={
        "symbol": symbol,
        "timeframe": timeframe,
        "error": str(e),
        "processor": self.__class__.__name__
    }
)
```
### 3.3 Kivételek naplózása
```python
try:
    # Kód...
except Exception as e:
    logger.error("An error occurred", exc_info=True)
    # vagy
    logger.exception("An error occurred")
```

## 4. Kivétel típusok

### 4.1 Alap rendszer kivételek
```python
# Core kivételek
class CoreError(Exception): pass
class ConfigError(CoreError): pass
class LoggerError(CoreError): pass
class StorageError(CoreError): pass

# Processzor kivételek
class ProcessorError(Exception): pass
class ValidationError(ProcessorError): pass
class CalculationError(ProcessorError): pass
class FeatureExtractionError(ProcessorError): pass

# Collector kivételek
class CollectorError(Exception): pass
class ConnectionError(CollectorError): pass
class DataFetchError(CollectorError): pass
class ApiError(CollectorError): pass

# Model kivételek
class ModelError(Exception): pass
class PredictionError(ModelError): pass
class TrainingError(ModelError): pass
class EvaluationError(ModelError): pass
```
### 4.2 Kivételek használati mintái
Validációs hibák
```python
def validate_data(self, data: pd.DataFrame) -> None:
    # Ellenőrzés, hogy vannak-e kötelező oszlopok
    required_columns = ['open', 'high', 'low', 'close']
    missing_columns = [col for col in required_columns if col not in data.columns]

    if missing_columns:
        raise ValidationError(
            f"Missing required columns: {missing_columns}"
        )
```
Számítási hibák
```python
def calculate_indicator(self, data: pd.DataFrame, period: int) -> pd.Series:
    if period <= 0:
        raise ValueError(f"Period must be positive, got {period}")

    try:
        # Indikátor számítása
        return result
    except Exception as e:
        raise CalculationError(
            f"Failed to calculate indicator with period={period}: {str(e)}"
        ) from e
```

## 5. Hibakezelés a tesztekben

### 5.1 Kivételek tesztelése
```python
def test_validation_error():
    processor = TestProcessor()
    invalid_data = pd.DataFrame({"invalid_column": [1, 2, 3]})

    with pytest.raises(ValidationError) as excinfo:
        processor.process(invalid_data)

    # Ellenőrizzük, hogy a kivétel üzenete tartalmazza a hiányzó oszlopok nevét
    assert "Missing required columns" in str(excinfo.value)
```
### 5.2 Határesetek tesztelése
```python
@pytest.mark.parametrize("input_data, expected_exception", [
    (pd.DataFrame(), ValidationError),  # Üres DataFrame
    (pd.DataFrame({"close": []}), ValidationError),  # Üres oszlop
    (pd.DataFrame({"close": [1, 2, None, 4]}), None),  # None értékek (elfogadható)
    (pd.DataFrame({"close": [1, 2, float('nan'), 4]}), None),  # NaN értékek (elfogadható)
])
def test_edge_cases(input_data, expected_exception):
    processor = TestProcessor()

    if expected_exception:
        with pytest.raises(expected_exception):
            processor.process(input_data)
    else:
        # Nem várunk kivételt
        result = processor.process(input_data)
        assert result is not None
```
## 6. Check-and-Act minta
```python
def process_data(self, data: pd.DataFrame) -> pd.DataFrame:
    # Ellenőrzés előre
    if data is None:
        raise ValueError("Data cannot be None")

    if len(data) == 0:
        # Üres DataFrame kezelése
        return pd.DataFrame()

    if not isinstance(data, pd.DataFrame):
        # Automatikus konverzió, ha lehetséges
        try:
            data = pd.DataFrame(data)
        except Exception as e:
            raise ValidationError(f"Could not convert to DataFrame: {e}") from e

    return self._process_implementation(data)
```
