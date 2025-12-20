# MT5 Collector Logger Implementáció

**Dátum:** 2025-12-15
**Komponens:** MT5 Collector
**Funkció:** Dupla logolás (console + file) implementációja

---

## 1. ÁTTEKINTÉS

A MT5 Collector logger implementációja **dupla logolási stratégiát** alkalmaz:
- **Console logger:** Valós idejű figyeléshez (colored logger)
- **File logger:** Részletes naplózáshoz és hibakereséshez (rotating file logger)

### Előnyök

1. **Valós idejű monitorozás:** Színes konzol kimenet azonnali visszajelzéshez
2. **Részletes naplózás:** Minden adatátvitel és hiba fájlba mentése
3. **Automatikus rotáció:** Log fájlok időalapú rotációja (naponta)
4. **Hibakeresés:** DEBUG szintű logolás fájlban, INFO szintű a konzolon
5. **Hosszú távú tárolás:** 7 napos backup történet

---

## 2. IMPLEMENTÁCIÓ

### 2.1 Dupla Logger Inicializálás

A [`collector.py`](../../../../neural_ai/collectors/mt5/collector.py) fájlban:

```python
# 1. Initialize Config
self.config_manager = ConfigManagerFactory.get_manager(filename=config_path)

# Get logger configuration from config file
logger_config = self.config_manager.get_section("logger")
logger_type = logger_config.get("type", "colored")
log_level = logger_config.get("level", "INFO")

# 2. Initialize Console Logger - Dual logging (console + file)
self.logger = LoggerFactory.get_logger(
    name="MT5Collector",
    logger_type=logger_type,
    log_level=log_level
)

# 3. Initialize File Logger for data collection logs
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
self.file_logger = LoggerFactory.get_logger(
    name="MT5CollectorFile",
    logger_type="rotating",
    log_file=str(log_dir / "mt5_collector.log"),
    rotation_type="time",
    when="midnight",
    backup_count=7
)
```

### 2.2 Logolási Stratégia

| Logger             | Típus              | Szint | Cél                          |
| ------------------ | ------------------ | ----- | ---------------------------- |
| `self.logger`      | ColoredLogger      | INFO  | Konzol kimenet (valós idejű) |
| `self.file_logger` | RotatingFileLogger | DEBUG | Fájl naplózás (részletes)    |

### 2.3 Használat a Tick Adatoknál

```python
# Log the received data to both loggers
log_message = (
    f"Tick received: {tick_data.symbol} "
    f"Bid={tick_data.bid:.5f} "
    f"Ask={tick_data.ask:.5f} "
    f"Time={tick_data.time}"
)
self.logger.info(log_message)           # Console: INFO
self.file_logger.debug(log_message)     # File: DEBUG

# ... adatok tárolása ...

# Log successful storage
self.file_logger.info(
    f"Tick data stored: {tick_data.symbol} "
    f"at {datetime.now().isoformat()}"
)
```

### 2.4 Hibakezelés

```python
except Exception as e:
    error_message = f"Error processing tick data: {e}"
    self.logger.error(error_message)        # Console: ERROR
    self.file_logger.error(error_message)   # File: ERROR
    raise HTTPException(status_code=500, detail=str(e))
```

---

## 3. KONFIGURÁCIÓ

### 3.1 Konfigurációs Fájl

[`configs/collector_config.yaml`](../../../../configs/collector_config.yaml):

```yaml
# Logger configuration
logger:
  type: "colored"
  level: "INFO"
```

### 3.2 Rotating File Logger Paraméterek

| Paraméter       | Érték                    | Leírás                |
| --------------- | ------------------------ | --------------------- |
| `name`          | "MT5CollectorFile"       | Logger neve           |
| `logger_type`   | "rotating"               | Rotating file logger  |
| `log_file`      | "logs/mt5_collector.log" | Log fájl útvonala     |
| `rotation_type` | "time"                   | Időalapú rotáció      |
| `when`          | "midnight"               | Napi rotáció éjfélkor |
| `backup_count`  | 7                        | 7 napos történet      |

---

## 4. LOG FÁJL STRUKTÚRA

### 4.1 Mappa szerkezet

```
logs/
├── mt5_collector.log          # Aktuális log fájl
├── mt5_collector.log.2025-12-14  # Előző napi log
├── mt5_collector.log.2025-12-13  # 2 napos log
└── ...                        # Legfeljebb 7 nap
```

### 4.2 Log Formátum

```
2025-12-15 22:18:22,568 - MT5CollectorFile - INFO - OHLCV data stored: EURUSD TF=16385 at 2025-12-15T22:18:22.568692
```

**Formátum elemek:**
- `%(asctime)s` - Időbélyeg
- `%(name)s` - Logger neve
- `%(levelname)s` - Log szint (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `%(message)s` - Üzenet

---

## 5. LOG SZINTEK

### 5.1 Console Logger (ColoredLogger)

| Szint    | Használat             | Szín            |
| -------- | --------------------- | --------------- |
| INFO     | Általános információk | Fehér           |
| WARNING  | Figyelmeztetések      | Sárga           |
| ERROR    | Hibák                 | Piros           |
| CRITICAL | Kritikus hibák        | Vörös, félkövér |

### 5.2 File Logger (RotatingFileLogger)

| Szint    | Használat                         |
| -------- | --------------------------------- |
| DEBUG    | Részletes adatátvitel információk |
| INFO     | Sikeres műveletek                 |
| WARNING  | Figyelmeztetések                  |
| ERROR    | Hibák                             |
| CRITICAL | Kritikus hibák                    |

---

## 6. HASZNÁLATI PÉLDÁK

### 6.1 Tick Adatok Logolása

**Console kimenet:**
```
2025-12-15 22:18:51,085 - MT5Collector - INFO - Tick received: EURUSD Bid=1.17520 Ask=1.17525 Time=1765840730
```

**File log:**
```
2025-12-15 22:18:51,085 - MT5CollectorFile - DEBUG - Tick received: EURUSD Bid=1.17520 Ask=1.17525 Time=1765840730
2025-12-15 22:18:51,085 - MT5CollectorFile - INFO - Tick data stored: EURUSD at 2025-12-15T22:18:51.085933
```

### 6.2 OHLCV Adatok Logolása

**Console kimenet:**
```
2025-12-15 22:18:22,568 - MT5Collector - INFO - OHLCV received: EURUSD TF=16385 Bars=10 Time=1765840700
```

**File log:**
```
2025-12-15 22:18:22,568 - MT5CollectorFile - DEBUG - OHLCV received: EURUSD TF=16385 Bars=10 Time=1765840700
2025-12-15 22:18:22,568 - MT5CollectorFile - INFO - OHLCV data stored: EURUSD TF=16385 at 2025-12-15T22:18:22.568692
```

### 6.3 Hiba Logolása

**Console kimenet:**
```
2025-12-15 22:19:15,123 - MT5Collector - ERROR - Error processing tick data: Connection timeout
```

**File log:**
```
2025-12-15 22:19:15,123 - MT5CollectorFile - ERROR - Error processing tick data: Connection timeout
```

---

## 7. TESZTELÉS

### 7.1 Logger Létrehozás Tesztelése

```python
def test_logger_initialization():
    """Teszteli a logger inicializálást."""
    collector = MT5Collector()

    # Ellenőrizzük, hogy mindkét logger létezik
    assert collector.logger is not None
    assert collector.file_logger is not None

    # Ellenőrizzük a logger típusokat
    assert isinstance(collector.logger, ColoredLogger)
    assert isinstance(collector.file_logger, RotatingFileLogger)
```

### 7.2 Log Fájl Létrehozás Tesztelése

```bash
# Ellenőrizzük, hogy a log fájl létezik-e
ls -la logs/mt5_collector.log

# Olvassuk ki az első 10 sort
head -10 logs/mt5_collector.log
```

### 7.3 Log Rotáció Tesztelése

```bash
# Várunk éjfélig, majd ellenőrizzük a rotációt
ls -la logs/
# Eredmény: mt5_collector.log (új fájl) + mt5_collector.log.2025-12-15 (régi)
```

---

## 8. GYAKORI PROBLÉMÁK ÉS MEGOLDÁSAIK

### 8.1 Nem jön létre a log fájl

**Probléma:** A `logs/` mappa üres marad.

**Lehetséges okok:**
1. Nincs írási jogosultság
2. A RotatingFileLogger paraméterei hibásak
3. A logger_type nem "rotating"

**Megoldás:**
```bash
# Ellenőrizzük az írási jogosultságot
chmod 755 logs/

# Ellenőrizzük a konfigurációt
cat configs/collector_config.yaml
```

### 8.2 Túl sok log fájl

**Probléma:** Több mint 7 log fájl van.

**Megoldás:**
```bash
# Régi log fájlok törlése
rm logs/mt5_collector.log.2025-12-0*
```

### 8.3 Log fájl túl nagy

**Probléma:** A log fájl mérete meghaladja a 1GB-ot.

**Megoldás:** Váltsunk méret alapú rotációra:
```python
self.file_logger = LoggerFactory.get_logger(
    name="MT5CollectorFile",
    logger_type="rotating",
    log_file=str(log_dir / "mt5_collector.log"),
    rotation_type="size",          # Méret alapú
    max_bytes=100*1024*1024,       # 100MB
    backup_count=10                # 10 backup
)
```

---

## 9. FEJLESZTÉSI TERV

### 9.1 Jelenlegi állapot

✅ **Dupla logolás működik**
- Console logger (colored)
- File logger (rotating, time-based)

### 9.2 Jövőbeli fejlesztések

- [ ] Log szintek konfigurálása külön a console és file loggerhez
- [ ] JSON formátumú logolás támogatása
- [ ] Log aggregáció (pl. ELK stack)
- [ ] Metrikák gyűjtése (pl. adatátviteli sebesség)
- [ ] Alert rendszer (pl. hiba esetén email)

---

## 10. KAPCSOLÓDÓ DOKUMENTUMOK

- [Logger API](../logger/api.md)
- [Logger Architektúra](../logger/architecture.md)
- [RotatingFileLogger Implementáció](../../../core/logger/implementations/rotating_file_logger.py)
- [LoggerFactory](../../../core/logger/implementations/logger_factory.py)
- [MT5 Collector Kód](../../../../neural_ai/collectors/mt5/collector.py)
- [Konfigurációs Fájl](../../../../configs/collector_config.yaml)

---

## 11. VÁLASZTÓK ÉS DÖNTÉSEK

### 11.1 Miért dupla logolás?

**Kérdés:** Miért nem elég csak a console logger vagy csak a file logger?

**Válasz:**
- **Console logger:** Valós idejű visszajelzés a fejlesztés és tesztelés során
- **File logger:** Hosszú távú naplózás, hibakeresés, audit trail
- **Kettő együtt:** Mindkét előny megszerzése

### 11.2 Miért időalapú rotáció?

**Kérdés:** Miért nem méretalapú rotáció?

**Válasz:**
- **Időalapú:** Könnyebb dátum alapján keresni a logokban
- **Napi rotáció:** Minden nap új fájl, könnyű archiválni
- **Adatgyűjtés jellege:** Folyamatos adatfolyam, napi bontás logikus

### 11.3 Miért 7 napos backup?

**Kérdés:** Miért pont 7 nap?

**Válasz:**
- **Egy hét:** Elég idő a legtöbb hibakereséshez
- **Tárolás:** Nem foglal túl sok helyet
- **Kompromisszum:** Hosszú távú tárolás vs. tárhely

---

**Dokumentum állapota:** Véglegesítve
**Utolsó frissítés:** 2025-12-15
**Felelős:** Code mód
