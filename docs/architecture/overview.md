# Neural-AI-Next Architektúra Áttekintés

## Rendszer architektúra

A Neural-AI-Next egy modern, moduláris és skálázható rendszer a pénzügyi piacok elemzésére és előrejelzésére. A rendszer több rétegből áll, amelyek egymásra épülnek:

### Adatgyűjtés és tárolás réteg
- **Collectors**: Különböző forrásokból (MT5, API-k, stb.) gyűjtenek adatokat
- **Storage**: Az adatok hatékony tárolásáért és kezeléséért felelős

### Feldolgozási réteg
- **Processors**: Az adatok feldolgozása és feature-ök kinyerése
- **Dimenziók**: Az adatfeldolgozók különböző piaci dimenziókat elemeznek
  - D1: Price Action
  - D2: Support/Resistance
  - D3: Trend
  - D4: Volatility
  - D5: Volume
  - stb.

### Modellezési réteg
- **Base Models**: Alapvető modellek az egyes dimenziók elemzésére
- **Hierarchikus modellek**: A különböző dimenziók együttes értelmezése
- **Meta-elemzők**: A különböző modellek eredményeinek egyesítése

### Rendszer mag
- **Core**: Alapvető infrastruktúra komponensek, amelyeket az összes többi réteg használ
  - **Logger**: Egységes naplózás
  - **Config**: Konfiguráció kezelés
  - **Storage**: Adattárolás és hozzáférés

## Interfész-alapú fejlesztés

A Neural-AI-Next erősen támaszkodik az interfész-alapú fejlesztési módszertanra:

1. **Interfész definíciók**: Minden fő komponenshez tartozik egy vagy több interfész, amely definiálja a komponens által nyújtott szolgáltatásokat.
2. **Implementációk**: Az interfészekhez különböző implementációk készülnek (pl. FileLogger, ConsoleLogger).
3. **Factory osztályok**: A komponensek példányosítását factory osztályok végzik, amelyek a konfigurációtól függően a megfelelő implementációt hozzák létre.

Ez a megközelítés számos előnyt nyújt:
- Körkörös importálások elkerülése
- Komponensek egyszerű cserélhetősége
- Egyszerűsített tesztelés mockolt komponensekkel
- Tiszta függőségi hierarchia

## Hierarchikus model struktúra

A Neural-AI-Next egy hierarchikus modell megközelítést alkalmaz:

1. **Szakértő modellek**: Egy-egy piaci dimenzió (pl. trend, support/resistance) elemzésére
2. **Dimenzión belüli integrátor**: Az azonos dimenzión belüli különböző elemzések egyesítése
3. **Dimenziók közötti integrátor**: Különböző dimenziók együttes értelmezése
4. **Meta-integrátor**: A végső döntési/előrejelzési modell
                +-------------------+
                |  Meta-integrátor  |
                +--------+----------+
                         |
 +------------------+----+----+------------------+
 |                  |         |                  |
 +--------v--------+ +-------v-------+ +-------v-------+ +--------v--------+ | D1 Integrátor | | D2 Integrátor | | D3 Integrátor | | ... Integrátor | +--------+--------+ +-------+-------+ +-------+-------+ +--------+--------+ | | | | +----+----+ +----+----+ +----+----+ +----+----+ | Modell | | Modell | | Modell | | Modell | +----+----+ +----+----+ +----+----+ +----+----+


## Komponensek közötti adatáramlás

+-------------+ +-------------+ +-------------+ | | | | | | | Collectors +----->+ Processors +----->+ Models | | | | | | | +------+------+ +------+------+ +------+------+ | | | | | | v v v +------+--------------------+--------------------+------+ | | | Storage | | | +-------------------------------------------------------+ ^ ^ ^ | | | | | | +------+------+ +------+------+ +------+------+ | | | | | | | Trainers | | Evaluators | | Visualizers | | | | | | | +-------------+ +-------------+ +-------------+

## Technológiai stack

- **Nyelv**: Python 3.10+
- **Adatkezelés**: pandas, numpy
- **Gépi tanulás**: scikit-learn, pytorch, lightning
- **Vizualizáció**: matplotlib, seaborn, plotly
- **Tesztelés**: pytest
- **CI/CD**: GitHub Actions
- **Dokumentáció**: Markdown, Sphinx

## Skálázhatóság és kiterjeszthetőség

A rendszer tervezésénél különös figyelmet fordítottunk a skálázhatóságra és a kiterjeszthetőségre:

1. **Plugin architektúra**: Új komponensek (pl. új processzor, új adatforrás) egyszerű hozzáadása
2. **Konfiguráció-vezérelt működés**: A rendszer viselkedése konfigurációs fájlokon keresztül alakítható
3. **Aszinkron feldolgozás**: Nagy adatmennyiségek hatékony feldolgozása
4. **Modularitás**: Komponensek független fejlesztése és tesztelése
