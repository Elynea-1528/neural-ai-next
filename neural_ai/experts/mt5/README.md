# MT5 Expert Advisors

Ez a könyvtár a MetaTrader 5 Expert Advisorokat tartalmazza, amelyek valós idejű piaci adatokat gyűjtenek a Neural AI Next rendszer számára.

## 📁 Mappa Struktúra

```
neural_ai/experts/
└── mt5/                          # MT5 specifikus Expert Advisorok
    ├── Neural_AI_Next.mq5        # Expert Advisor forráskód
    ├── Neural_AI_Next.ex5        # Fordított EA (generálva)
    └── README.md                 # Ez a fájl
```

## 🎯 Használat

### Expert Advisor

Az [`Neural_AI_Next.mq5`](Neural_AI_Next.mq5) egy intelligens Expert Advisor, amely:

- **Tick adatokat gyűjt** valós időben
- **OHLCV adatokat küld** időszakos frissítésekben
- **HTTP kommunikációt használ** a FastAPI szerverrel
- **Kétirányú kommunikációt** támogat (adatok küldése + parancsok fogadása)

### Fordítás

```bash
# Projekt gyökérből
./scripts/compile_mql.sh neural_ai/experts/mt5/Neural_AI_Next.mq5
```

### Telepítés MT5-be

A fordítási script automatikusan másolja a fájlokat az MT5 Experts mappájába:

```
~/.mt5/drive_c/Program Files/MetaTrader 5/MQL5/Experts/Neural_AI_Next.ex5
```

### Konfiguráció

Az EA beállításai az MT5 charton:

- **FastAPI_Server**: FastAPI szerver címe (alapértelmezett: `http://localhost:8000`)
- **Update_Interval**: Frissítési intervallum másodpercben (alapértelmezett: 60)
- **Enable_HTTP_Logs**: HTTP kérések naplózásának engedélyezése

## 🔧 Fejlesztés

### MQL5 Fejlesztés

1. **Szintaxis kiemelés:** Telepítsd a MQL Extension Pack bővítményt
2. **Fordítás:** Használd a `scripts/compile_mql.sh` scriptet
3. **Tesztelés:** Töltsd be az EA-t MT5-be és húzd egy chartra

### Kommunikáció

Az EA a következő végpontokkal kommunikál:

```
POST /api/v1/collect/tick    # Tick adatok küldése
POST /api/v1/collect/ohlcv   # OHLCV adatok küldése
GET  /api/v1/ping            # Kapcsolat tesztelése
```

### Adatstruktúra

**Tick adatok:**
```json
{
  "symbol": "EURUSD",
  "bid": 1.12345,
  "ask": 1.12356,
  "time": 1702684800,
  "volume": 12345
}
```

**OHLCV adatok:**
```json
{
  "symbol": "EURUSD",
  "timeframe": 60,
  "bars": [...],
  "time": 1702684800
}
```

## 🐛 Hibaelhárítás

### EA nem jelenik meg MT5-ben

1. Ellenőrizd a fordítási naplót: `cat /tmp/mql_compile.log`
2. Ellenőrizd a fájl helyét: `ls -la ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/MQL5/Experts/`
3. Indítsd újra az MT5-öt

### Nincs kapcsolat a FastAPI szerverrel

1. Ellenőrizd, hogy fut-e a FastAPI szerver
2. Ellenőrizd a `FastAPI_Server` beállítást az EA-ban
3. Ellenőrizd a tűzfal beállításokat

### Fordítási hibák

1. Ellenőrizd az MQL5 szintaxist
2. Ellenőrizd, hogy telepítve van-e a Wine és MT5
3. Futtasd a fordítási scriptet verbose módban

## 📚 További Erőforrások

- [MQL5 Fordítási Útmutató](../../../docs/MQL5_COMPILATION_GUIDE.md)
- [Wine + MT5 Beállítás](../../../docs/WINE_MT5_SETUP.md)
- [MQL5 Dokumentáció](https://www.mql5.com/en/docs)
- [FastAPI Integráció](../../../docs/architecture/overview.md)

## 🔮 Jövőbeli Fejlesztések

- [ ] HTTP kliens implementáció WinInet vagy socket használatával
- [ ] Szerver oldali végpontok implementációja parancsok fogadásához
- [ ] Hibakezelés és újrapróbálkozási logika
- [ ] Titkosítás a kommunikációban
- [ ] Több időkeret támogatása
- [ ] Több szimbólum egyidejű kezelése

## 📝 Megjegyzések

- Az Expert Advisorok az `neural_ai/experts/` mappában vannak
- A Collector komponensek az `neural_ai/collectors/` mappában lesznek
- A projekt készen áll más források (MT4, TradingView) hozzáadására
- Az EA forráskódját mindig tartsd szinkronban a projekt git repository-jával