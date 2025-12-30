# JForex Bridge Deployment Guide

## Áttekintés

Ez a dokumentáció leírja a JForex Bridge automatikus telepítési folyamatát, amely MT5-szerű egyszerűsített élményt nyújt.

## Funkciók

- **Automatikus JForex mappa detektálás**: A szkript automatikusan megkeresi a JForex telepítési mappát
- **Gradle build**: Automatikusan lefordítja a Java kódot és letölti a függőségeket
- **Intelligens telepítés**: A szükséges fájlokat a megfelelő helyre másolja
- **Felhasználóbarát összefoglaló**: Tiszta utasításokat ad a következő lépésekre

## Előfeltételek

### 1. Gradle Telepítés

A szkript használatához szükséges a Gradle build eszköz:

```bash
# Ubuntu/Debian
sudo apt-get install gradle

# Vagy használja a Gradle Wrapper-t (ajánlott)
cd external/jforex-bridge
gradle wrapper
```

### 2. JForex Platform

A JForex platformnak telepítve kell lennie az alábbi mappák egyikében:
- `~/JForex/Strategies`
- `~/Documents/JForex/Strategies`
- `~/JForex`
- `~/Documents/JForex`

## Telepítési Lépések

### 1. Build Folyamat

A szkript a következő lépéseket hajtja végre:

1. **JForex mappa keresése**
   - Automatikusan ellenőrzi a lehetséges helyeket
   - Ha nem találja, kéri a felhasználótól a mappa útvonalát

2. **Gradle Build**
   ```bash
   cd external/jforex-bridge
   gradle build
   ```
   
   A build folyamat:
   - Letölti a függőségeket (JeroMQ, Gson)
   - Lefordítja a Java kódot
   - Összegyűjti az összes JAR fájlt a `build/libs` mappába

3. **Fájlok másolása**
   - `NeuralBridgeStrategy.java` → JForex Strategies mappa
   - Függőségi JAR-ok → JForex Strategies/files mappa

### 2. Szkript Futtatása

```bash
# A projekt gyökérkönyvtárából
python3 scripts/deploy_jforex.py
```

### 3. Várható Kimenet

```
============================================================
🧠 NEURAL AI - JFOREX BRIDGE AUTO-DEPLOY
============================================================

🔍 JForex mappa keresése...
✅ JForex mappa megtalálva: /home/user/JForex/Strategies
✅ Bridge mappa megtalálva: /path/to/neural-ai-next/external/jforex-bridge

🔨 Gradle build futtatása: /path/to/neural-ai-next/external/jforex-bridge
✅ Gradle build sikeres!

🚀 Fájlok telepítése: ... -> /home/user/JForex/Strategies
   📄 Java fájl másolása: /home/user/JForex/Strategies/NeuralBridgeStrategy.java
   📦 JAR másolása: jeromq-0.5.4.jar
   📦 JAR másolása: gson-2.10.1.jar
✅ Összes fájl sikeresen telepítve!

============================================================
🎉 JFOREX BRIDGE TELEPÍTÉS SIKERES!
============================================================

📁 Telepítési mappa: /home/user/JForex/Strategies

📋 Telepített fájlok:
   ✓ /home/user/JForex/Strategies/NeuralBridgeStrategy.java
   ✓ /home/user/JForex/Strategies/files/jeromq-0.5.4.jar
   ✓ /home/user/JForex/Strategies/files/gson-2.10.1.jar

🚀 Következő lépések:
   1. Indítsa el a JForex platformot
   2. Nyissa meg a Strategy Manager-t
   3. Importálja a NeuralBridgeStrategy.java fájlt
   4. Futtassa a stratégia egy demo számlán

⚠️  FIGYELEM: A stratégia csak demo módban futtatható!
============================================================
```

## JForex Platformon Történő Beállítás

### 1. Strategy Manager

1. Indítsa el a JForex platformot
2. Nyissa meg a **Strategy Manager**-t
3. Kattintson az **Import** gombra
4. Tallózzon a `NeuralBridgeStrategy.java` fájlhoz
5. Ellenőrizze, hogy a stratégia betöltődött

### 2. Demo Számla

1. Győződjön meg róla, hogy demo módban van
2. Nyisson meg egy chartot egy támogatott instrumentummal (pl. EUR/USD)
3. Húzza a NeuralBridgeStrategy-t a chartra
4. Állítsa be a stratégia paramétereit (ha szükséges)
5. Indítsa el a stratégia futtatását

### 3. ZeroMQ Kommunikáció Ellenőrzése

A stratégia indítása után:

- **Tick Publisher**: Port 5555 (PUB socket)
- **Command Receiver**: Port 5556 (REP socket)

Ellenőrizze a JForex konzolon a következő üzenetet:
```
Neural Bridge started - Ports: 5555, 5556
```

## Hibaelhárítás

### 1. Gradle Build Hiba

**Probléma**: `Gradle parancs nem található`

**Megoldás**:
```bash
# Telepítse a Gradle-t
sudo apt-get install gradle

# Vagy használja a Gradle Wrapper-t
cd external/jforex-bridge
gradle wrapper
./gradlew build
```

### 2. JForex Mappa Nem Található

**Probléma**: A szkript nem találja a JForex mappát

**Megoldás**:
- Adja meg kézzel a JForex mappa teljes útvonalát
- Ellenőrizze, hogy a JForex telepítve van-e

### 3. JAR Fájlok Hiánya

**Probléma**: `Nincs JAR fájl a build/libs mappában`

**Megoldás**:
- Ellenőrizze, hogy a `gradle build` sikeresen lefutott-e
- Futtassa kézzel a buildet:
  ```bash
  cd external/jforex-bridge
  gradle build
  ```

### 4. Port Foglaltság

**Probléma**: A stratégia nem tud bind-olni a portokra

**Megoldás**:
- Ellenőrizze, hogy másik stratégia nem használja-e a 5555-5556 portokat
- Módosítsa a portokat a `NeuralBridgeStrategy.java` fájlban:
  ```java
  private static final int TICK_PORT = 5555;
  private static final int COMMAND_PORT = 5556;
  ```

## Fejlesztői Információk

### Build.gradle Struktúra

```gradle
plugins {
    id 'java'
}

repositories {
    mavenCentral()
    maven { url "https://www.dukascopy.com/client/jforexlib/publicrepo" }
}

dependencies {
    implementation 'org.zeromq:jeromq:0.5.4'
    implementation 'com.google.code.gson:gson:2.10.1'
    compileOnly 'com.dukascopy.api:JForex-API:2.13.53'
}

// Függőségek másolása a build/libs mappába
task copyDependencies(type: Copy) {
    from configurations.runtimeClasspath
    into 'build/libs'
}

build.dependsOn copyDependencies
```

### Szkript Funkciók

A `deploy_jforex.py` szkript fő funkciói:

1. **`find_jforex_folder()`**: JForex mappa keresése
2. **`run_gradle_build()`**: Gradle build futtatása
3. **`deploy_files()`**: Fájlok másolása a JForex mappába
4. **`print_summary()`**: Telepítés utáni összefoglaló

### Fájl Struktúra

```
external/jforex-bridge/
├── build.gradle                 # Gradle konfiguráció
├── src/main/java/com/neuralai/bridge/
│   └── NeuralBridgeStrategy.java  # JForex stratégia
└── build/libs/                  # Buildelt JAR-ok

scripts/
└── deploy_jforex.py             # Telepítő szkript

JForex/Strategies/
├── NeuralBridgeStrategy.java    # Másolt stratégia
└── files/
    ├── jeromq-0.5.4.jar         # ZeroMQ könyvtár
    └── gson-2.10.1.jar          # JSON könyvtár
```

## Biztonsági Megfontolások

- ⚠️ **Csak Demo Mód**: A stratégia kizárólag demo számlán futtatható
- 🔒 **Port Védelem**: A 5555-5556 portok csak lokális hozzáférésre vannak kötve
- 📡 **ZeroMQ Biztonság**: A kommunikáció csak lokális hálózaton történik
- 🔐 **API Kulcs**: A JForex API csak demo környezetben használható

## Kapcsolódó Dokumentációk

- [JForex Collector Architektúra](index.md)
- [Live Feed Implementáció](implementations/live_feed.md)
- [BI5 Downloader](implementations/bi5_downloader.md)
- [Factory Pattern](factory.md)

## Verziótörténet

- **v1.0.0** (2025-12-30): Kezdeti verzió
  - Automatikus JForex mappa detektálás
  - Gradle build integráció
  - Intelligens fájl telepítés
  - Felhasználóbarát összefoglaló

## Kapcsolat

Ha problémába ütközik a telepítés során, kérjük vegye fel a kapcsolatot a Neural AI csapattal.