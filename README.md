# Neural-AI-Next

## Áttekintés

A Neural-AI-Next egy moduláris, hierarchikus kereskedési rendszer, amely különböző piaci dimenziókat elemez és integrál, hogy komplex kereskedési döntéseket hozzon. A rendszer modern gépi tanulási technikákat alkalmaz a pénzügyi piacok elemzésére.

## Fő jellemzők

- Moduláris, interfész-alapú architektúra
- Hierarchikus modell struktúra
- Több dimenzió együttes elemzése
- Integrált gépi tanulási modellek
- Konfiguráció-vezérelt működés
- Teljeskörű naplózás és monitorozás
- Skálázható és kiterjeszthető kialakítás

## Projekt struktúra

```
/neural-ai-next
├── neural_ai/                       # Fő kódkönyvtár
│   ├── collectors/                  # Adatgyűjtők
│   ├── processors/                  # Adatfeldolgozók
│   ├── models/                      # Modell definíciók
│   ├── trainers/                    # Modell tanítók
│   ├── evaluators/                  # Kiértékelők
│   ├── core/                        # Alapvető komponensek
│   │   ├── logger/                  # Logger rendszer
│   │   ├── config/                  # Konfigurációkezelés
│   │   └── storage/                 # Adattárolás
│   └── utils/                       # Segédeszközök
├── tests/                           # Tesztek
├── docs/                            # Dokumentáció
├── configs/                         # Konfigurációs fájlok
├── data/                            # Adatok
├── logs/                            # Logfájlok
├── models/                          # Modell mentések
└── examples/                        # Példakódok
```

## Telepítés

A telepítéshez kövesse az [INSTALL.md](INSTALL.md) fájlban található utasításokat.

```bash
# Conda környezet létrehozása
conda env create -f environment.yml

# Környezet aktiválása
conda activate neural-ai-next

# Telepítés fejlesztői módban
pip install -e .
```

## Fejlesztés

A fejlesztéssel kapcsolatos további információk a [docs/development](docs/development/) könyvtárban találhatók. A fejlesztés aktuális állapotáról a [DEVELOPMENT_STATUS.md](docs/development/DEVELOPMENT_STATUS.md) fájl nyújt tájékoztatást.

## Licenc

Privát projekt, minden jog fenntartva.