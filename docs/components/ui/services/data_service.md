# ui/services/data_service.py

Data Service implementáció.

Ez a modul implementálja az adatkezelési szolgáltatást, amely
az adatok betöltését, szűrését és kezelését végzi Big Data támogatással.

## Osztályok

### `DataService`

Data Service - Adatkezelésért felelős.

    Ez az osztály implementálja az adatok lekérdezését és kezelését
    végző metódusokat, Big Data támogatással és chunkolással.

    Attributes:
        _bridge: A backend bridge példány
        _data_sources: Az elérhető adatforrások definíciói


## Függvények

### `__init__`

A Data Service inicializálása.

    Args:
        bridge: A backend bridge példány, amelyen keresztül elérjük a
            backend komponenseket (Bi5Downloader, ParquetStorage)

### `load_data`

Adatok aszinkron betöltése chunkokban.

    Args:
        source: Az adatforrás azonosítója
        filters: Szűrőfeltételek
        chunk_size: A chunkok mérete

    Yields:
        List[Dict[str, Any]]: Adat chunkok

### `get_data_sources`

Elérhető adatforrások lekérdezése.

    Returns:
        List[Dict[str, str]]: Az adatforrások listája

### `get_data_info`

Adatforrás információk lekérdezése.

    Args:
        source: Az adatforrás azonosítója

    Returns:
        Dict[str, Any]: Az adatforrás metaadatai

### `apply_filters`

Szűrők alkalmazása adatokra.

    Args:
        data: A szűrendő adatok
        filters: A alkalmazandó szűrők

    Returns:
        List[Dict[str, Any]]: A szűrt adatok

### `export_data`

Adatok exportálása különböző formátumokba.

    Args:
        data: Az exportálandó adatok
        format: A célformátum (parquet, csv, json)
        destination: A cél útvonal

    Returns:
        bool: True, ha sikeres az exportálás

### `get_default_date_range`

Alapértelmezett dátumtartomány lekérdezése a konfigurációból.

    A metódus kiolvassa a configból a `collectors.jforex.date_range.start` és
    `end` értékeit, és datetime objektumokká konvertálja őket. Ha a konfiguráció
    üres vagy hiba történik, akkor fallback értékeket használ.

    Returns:
        tuple[datetime, datetime]: A kezdő és záró dátum tuple-ben.
            Fallback: (2020-01-01, ma)

### `download_history`

Történelmi adatok letöltése aszinkron módon.

    Ez a metódus a CoreBridge-en keresztül eléri a Bi5Downloader-t,
    és valós adatletöltést végez a Dukascopy .bi5 formátumból.
    A tick adatok csak a forrásból jövő 5 oszlopot tartalmazzák:
    timestamp, bid, ask, ask_volume, bid_volume.

    Args:
        symbol: A szimbólum (pl. 'EURUSD' vagy 'ALL' az összesre)
        start: A kezdő dátum
        end: A záró dátum

    Returns:
        dict[str, Any]: A letöltött adatok metaadatai és az adatok
            - symbol: A letöltött szimbólum (vagy 'ALL')
            - start_date: Kezdő dátum ISO formátumban
            - end_date: Záró dátum ISO formátumban
            - status: Letöltési állapot ('downloaded', 'failed', 'partial')
            - records: Letöltött rekordok száma
            - size_mb: Letöltött adatok mérete MB-ban
            - format: Az adatformátum ('parquet')
            - path: A tárolási útvonal
            - successful_dates: Sikeres napok száma
            - failed_dates: Sikertelen napok száma
            - total_days: Összes napok száma

    Raises:
        ValueError: Ha a dátumtartomány érvénytelen
        RuntimeError: Ha a letöltés sikertelen

### `list_available_data`

Elérhető adatok listázása DataFrame formátumban.

    Ez a metódus a CoreBridge-en keresztül eléri a ParquetStorage-t,
    és valós adatokról állít össze listát.

    Args:
        symbol: Opcionális szimbólum szűréshez

    Returns:
        pd.DataFrame: Az elérhető adatok DataFrame-je, amely tartalmazza:
            - source_id: Az adatforrás azonosítója
            - name: Az adatforrás neve
            - description: Leírás
            - format: Az adatformátum
            - size_gb: Méret GB-ban
            - records: Rekordok száma
            - last_updated: Utolsó frissítés időpontja
            - available_dates: Elérhető dátumok száma

### `get_storage_path`

Az adattárolási útvonal lekérdezése.

    Ez a metódus a CoreBridge-en keresztül eléri a ParquetStorage-t,
    és a tényleges tárolási útvonalat adja vissza.

    Returns:
        Path: Az adattárolási útvonal

    Raises:
        RuntimeError: Ha a storage komponens nem érhető el

### `get_configured_symbols`

Konfigurált szimbólumok lekérdezése.

    A metódus eléri a konfigurációt a CoreBridge-en keresztül, és kiolvassa
    a JForex collectorhoz tartozó szimbólumokat. Ha a konfiguráció üres vagy
    hiba történik a lekérdezés során, akkor egy alapértelmezett szimbólumlistát
    ad vissza.

    Returns:
        list[str]: A konfigurált szimbólumok listája. Alapértelmezett esetben
            ["EURUSD"]-t ad vissza, ha a konfigurációból nem sikerül
            lekérdezni a szimbólumokat.


---

**Forrásfájl:** [`ui/services/data_service.py`](../../../neural_ai/ui/services/data_service.py)
