# Broker Telepítési Útmutató

## Áttekintés

Ez a dokumentum részletesen leírja a különböző brókerek telepítését és konfigurálását a Neural AI Next projekthez.

## Támogatott Brókerek

### MetaTrader 5 (MT5)

A projekt támogatja a következő MT5 brókereket:

1. **MetaQuotes Demo** - Hivatalos MT5 demo szerver
2. **XM Forex** - XM MT5 platform
3. **Dukascopy** - Dukascopy MT5 platform

#### Telepítés

```bash
# Indítsd el a broker telepítőt
bash setup_brokers.sh

# Válaszd ki a kívánt opciót:
# 1) MetaTrader 5 (MetaQuotes Demo)
# 2) XM Forex MT5
# 3) Dukascopy MT5
# 5) Összes MT5 bróker
```

#### Konfiguráció

A konfigurációs fájlok a `configs/collectors/mt5/` mappában találhatók:

- `broker_metaquotes.yaml` - MetaQuotes konfiguráció
- `broker_xm.yaml` - XM konfiguráció
- `broker_dukascopy.yaml` - Dukascopy konfiguráció

#### Használat

```bash
# MT5 indítása
export WINEPREFIX=~/.mt5
wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe

# Demo fiók létrehozása után konfiguráld a kapcsolatot
```

### JForex4

A projekt támogatja a Dukascopy JForex4 platformot.

**Fontos:** A JForex4 natív Linux alkalmazás, nem Wine-on fut. Java alapú platform, amelyhez Java 8 vagy újabb szükséges.

#### Előfeltételek

```bash
# Java telepítése (ajánlott, bár a telepítő tartalmaz JRE-t)
# Ubuntu/Debian
sudo apt install openjdk-11-jdk

# Fedora
sudo dnf install java-11-openjdk
```

#### Telepítés

```bash
# Indítsd el a broker telepítőt
bash setup_brokers.sh

# Válaszd ki a 4-es opciót: Dukascopy JForex4
```

A telepítő letölti a `JForex4_unix_64_JRE_bundled.sh` fájlt és natív Linux telepítést végez.

#### Konfiguráció

A konfigurációs fájl a `configs/collectors/jforex/` mappában található:

- `jforex_config.yaml` - JForex konfiguráció

#### Használat

```bash
# JForex4 indítása (telepítés helyétől függően)
~/jforex/JForex4

# vagy ha más helyre lett telepítve
/opt/jforex/JForex4

# Demo fiók létrehozása után konfiguráld a kapcsolatot
```

#### Telepítés ellenőrzése

```bash
# Ellenőrizd, hogy a JForex4 elérhető-e
ls -la ~/jforex/

# vagy
ls -la /opt/jforex/
```

## Csoportos Telepítés

### Összes MT5 Bróker

```bash
bash setup_brokers.sh
# Válaszd ki az 5-ös opciót
```

Ez a következő brókereket telepíti:
- MetaQuotes Demo
- XM Forex
- Dukascopy

### Minden Bróker

```bash
bash setup_brokers.sh
# Válaszd ki a 7-es opciót
```

Ez az összes támogatott brókert telepíti.

## Konfiguráció

A konfigurációs fájlok a `configs/collectors/` mappában találhatók:

```
configs/collectors/
├── mt5/
│   ├── broker_metaquotes.yaml
│   ├── broker_xm.yaml
│   └── broker_dukascopy.yaml
└── jforex/
    └── jforex_config.yaml
```

A konfigurációs fájlokat manuálisan kell létrehozni a saját beállításaid szerint.

## Hibaelhárítás

### Wine telepítése

```bash
# Ubuntu/Debian
sudo apt install wine-stable

# Fedora
sudo dnf install wine
```

### Java telepítése (JForex4-hez)

A JForex4 Java alapú alkalmazás. A telepítő tartalmaz JRE-t, de ajánlott előtelepíteni:

```bash
# Ubuntu/Debian
sudo apt install openjdk-11-jdk

# Fedora
sudo dnf install java-11-openjdk

# Verzió ellenőrzése
java -version
```

### WebView2 Runtime telepítése

A WebView2 Runtime automatikusan települ az MT5 telepítésekor. Ha manuálisan kell telepíteni:

```bash
cd ~/Downloads
curl -L https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/f2910a1e-e5a6-4f17-b52d-7faf525d17f8/MicrosoftEdgeWebview2Setup.exe --output webview2.exe
WINEPREFIX=~/.mt5 wine webview2.exe /silent /install
```

### Demo Fiók Létrehozása

1. Indítsd el a brókert
2. Kattints a "Open an Account" gombra
3. Válaszd ki a "Demo Account" opciót
4. Töltsd ki az űrlapot
5. Mentsd el a kapcsolati adatokat a konfigurációs fájlba

## További Források

- [Telepítési Útmutató](INSTALLATION_GUIDE.md)
- [Hibaelhárítás](TROUBLESHOOTING.md)
- [MT5 Collector Dokumentáció](../../../docs/components/collectors/mt5/README.md)