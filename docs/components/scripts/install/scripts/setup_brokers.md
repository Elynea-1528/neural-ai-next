# setup_brokers.sh - Broker Telepítő Script

## 📝 Leírás

Ez a shell script a Neural AI Next projekt részeként fejlesztett broker telepítő eszköz. Támogatja a MetaTrader 5 platformot (MetaQuotes, XM, Dukascopy) és a Dukascopy JForex4 alkalmazást Linux környezetben.

## 🎯 Főbb Funkciók

### Támogatott Brókerek

1. **MetaTrader 5 (MetaQuotes Demo)** - Hivatalos MetaTrader 5 demo szerver
2. **XM Forex MT5** - XM bróker MetaTrader 5 platformja
3. **Dukascopy MT5** - Dukascopy bróker MetaTrader 5 platformja
4. **Dukascopy JForex4** - Dukascopy natív Linux alkalmazása

### Telepítési Opciók

- Egyedi bróker telepítése (1-4)
- Összes MT5 bróker telepítése (5)
- Összes JForex bróker telepítése (6)
- Minden bróker telepítése (7)

## 🔧 Technikai Előfeltételek

### MetaTrader 5-hez

- **Wine** - Windows alkalmazások futtatásához Linuxon
- **WebView2 Runtime** - Modern webes felület támogatás

### JForex4-hez

- **Java 8+** (opcionális, a telepítő tartalmaz JRE-t)

## 📁 Fájlstruktúra

```
scripts/install/scripts/setup_brokers.sh
```

### Konfigurációs Fájlok

A script a következő konfigurációs fájlokat várja:

- `configs/collectors/mt5/broker_metaquotes.yaml`
- `configs/collectors/mt5/broker_xm.yaml`
- `configs/collectors/mt5/broker_dukascopy.yaml`
- `configs/collectors/jforex/jforex_config.yaml`

## 🚀 Használat

### Alapvető Használat

```bash
bash scripts/install/scripts/setup_brokers.sh
```

### Környezeti Változók

```bash
# MT5 Wine prefix megadása (opcionális)
export WINEPREFIX_MT5="$HOME/.mt5"

# JForex4 telepítési könyvtár (opcionális)
export JFOREIX_INSTALL_DIR="$HOME/jforex"
```

## 🔍 Funkciók Részletesen

### Wine Ellenőrzés (`check_wine`)

Ellenőrzi, hogy a Wine telepítve van-e a rendszeren. Ha nem, hibaüzenetet jelenít meg és kilép.

### Java Ellenőrzés (`check_java`)

Ellenőrzi a Java verziót. A JForex4-hez Java 8 vagy újabb szükséges.

### Wine Környezet Beállítása (`setup_wine`)

- Létrehozza a Wine prefix könyvtárat
- Inicializálja a Wine környezetet
- Windows 11-re állítja a Windows verziót

### WebView2 Runtime Telepítés (`install_webview2`)

Letölti és telepíti a Microsoft WebView2 Runtime-ot a Wine környezetbe.

### MetaTrader 5 Telepítés (`install_mt5`)

- Letölti a kiválasztott bróker MT5 telepítőjét
- Wine-on keresztül telepíti az MT5-öt
- Törli a letöltött telepítőfájlt

### JForex4 Telepítés (`install_jforex4`)

- Letölti a JForex4 natív Linux telepítőt
- Futtathatóvá teszi a telepítőt
- Elindítja a grafikus telepítőt

### Broker Konfiguráció Beállítása (`setup_broker_config`)

Ellenőrzi a bróker specifikus konfigurációs fájlok létezését.

## 🎨 Színes Kimenet

A script színes kimenetet használ a jobb átláthatóság érdekében:

- 🔴 **Piros** - Hibák
- 🟢 **Zöld** - Sikeres műveletek
- 🟡 **Sárga** - Figyelmeztetések
- 🔵 **Kék** - Szakaszok címei

## ⚙️ Telepítési Lépések

1. **Wine ellenőrzése**
2. **Bróker kiválasztása** (interaktív menü)
3. **Wine környezet beállítása** (MT5 esetén)
4. **WebView2 Runtime telepítése** (MT5 esetén)
5. **Bróker platform telepítése**
6. **Konfiguráció ellenőrzése**
7. **Használati utasítások megjelenítése**

## 🧪 Tesztelés

A script manuális tesztelést igényel, mivel interaktív és külső függőségeket (Wine, Java) használ.

### Tesztelési Eljárás

1. **Előfeltételek ellenőrzése:**
   ```bash
   wine --version
   java -version
   ```

2. **Script futtatása:**
   ```bash
   bash scripts/install/scripts/setup_brokers.sh
   ```

3. **Telepítés ellenőrzése:**
   ```bash
   # MT5 esetén
   export WINEPREFIX=~/.mt5
   wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe

   # JForex4 esetén
   ~/jforex/JForex4
   ```

## 🔒 Biztonsági Megfontolások

- A script `set -e` opciót használ, ami hibák esetén azonnal leáll
- A letöltött telepítőfájlok törlésre kerülnek a telepítés után
- A Wine prefix elkülönített környezetben fut

## 🐛 Ismert Korlátozások

- **MT5 telepítő ablak:** A Wine-on futó MT5 telepítő ablakot manuálisan kell bezárni
- **JForex4 grafikus felület:** A JForex4 telepítő grafikus felülettel rendelkezik, manuális beavatkozást igényel
- **Windows verzió:** A Wine konfiguráció Windows 11-re van állítva, ami nem minden esetben optimális

## 📚 Kapcsolódó Dokumentáció

- [Telepítési Útmutató](../../../INSTALLATION_GUIDE.md)
- [MQL5 Fordító Script](compile_mql.sh.md)
- [Jupyter Setup Script](jupyter_setup.md)

## 🔄 Frissítési Terv

- [ ] Automatikus MT5 telepítő ablak kezelés
- [ ] JForex4 telepítés automatizálása
- [ ] További brókerek támogatása
- [ ] Telepítés visszavonásának lehetősége

## 👥 Fejlesztők

- Neural AI Next Fejlesztőcsapat

## 📄 Licenc

A projekt licencével megegyezően.

---

**Utolsó Frissítés:** 2025-12-22
**Verzió:** 1.0.0
