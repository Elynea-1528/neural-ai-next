🛡️ NEURAL AI MASTER PROTOCOL (v3.0 - CONSOLIDATED)
0. ⚠️ KRITIKUS KÖRNYEZET ÉS KONTEXTUS (HARD CONSTRAINTS)
Környezeti Változók
Python Path: /home/elynea/miniconda3/envs/neural-ai-next/bin/python

Környezet: Conda neural-ai-next

Parancsfuttatás: Minden parancsot a fenti teljes útvonallal kell futtatni a konzisztencia érdekében.

Kontextus Menedzsment (100k Limit)
HARD LIMIT: 100,000 token.

Szabály: Mivel a modell memóriája (context window) véges (128k), a 100k elérésekor KÖTELEZŐ:

Lezárni az aktuális fájl szerkesztését.

Frissíteni a QA_STATUS.md-t.

Új "Task" indítását kérni a folytatáshoz.

Tilalom: Tilos a limitig elmenni, mert az orchestrator elveszíti a dokumentációs fonalat.

I. ARCHITEKTÚRA ÉS VÉGREHAJTÁSI STRATÉGIA (HIBRID)
Architektúrális Alapelvek
Core: BaseFactory és Container osztályok.

Dynamic DI: A logger, config és storage komponensek dinamikusan injektáltak.

TILTOTT: A dinamikus importokat statikusra cserélni a linter kedvéért.

MEGOLDÁS: Használj if TYPE_CHECKING: blokkot, Protocol-t vagy cast-ot a típusbiztonsághoz, de a futásidejű logikát ne törd el!

Végrehajtási Sorrend (Sorrendtartás Kötelező!)
A körkörös függőségek elkerülése érdekében:

PHASE 1: Base Abstracts (A Szülők)

neural_ai/core/base/exceptions.py

neural_ai/core/base/interfaces.py

neural_ai/core/base/singleton.py

neural_ai/core/base/lazy_loading.py

neural_ai/core/base/core_components.py

PHASE 2: Core Implementations (Az Alkatrészek)

neural_ai/core/config/ (teljes mappa)

neural_ai/core/logger/ (teljes mappa)

neural_ai/core/storage/ (teljes mappa)

PHASE 3: Integration (Az Összerakás)

neural_ai/collectors/

neural_ai/core/base/container.py

neural_ai/core/base/factory.py (Ez zárja a sort!)

scripts/

templates/ (Legacy óvatosság)

II. ÁLTALÁNOS VISELKEDÉSI SZABÁLYOK
1. Nyelv (Language)
KIZÁRÓLAG MAGYAR: Minden kommunikáció, kódkomment, docstring, commit üzenet, hibaüzenet és dokumentáció magyar nyelven íródik.

Stílus: Professzionális, szakmai, precíz. Nincs "szerintem", csak tények.

2. Szakmai Szigorúság
Zéró Tolerancia: Nincs "majd később javítom". Ha hiba van, javítjuk.

Problems Tab: A szerkesztés végén a Problems fülnek (linter output) üresnek kell lennie.

Teljesség: Nincs félkész kód.

III. KÓDOLÁSI ÉS MINŐSÉGBIZTOSÍTÁSI STANDARDOK
1. Type Safety (Típusbiztonság)
Mindenhol: Minden függvény, metódus, paraméter és visszatérési érték típusos (type hint).

Szigor: Any használata csak végső esetben, indoklással.

Eszközök: Pylance (Strict), Mypy.

2. Dokumentáció (Docstrings)
Formátum: Google Style Docstring.

Tartalom: Leírás, Args, Returns, Raises, Példa.

Szinkronizáció: Ha a kód változik, a docs/ mappában lévő markdown fájlt is frissíteni kell (vagy létrehozni, ha nincs).

3. Tesztelés
Követelmény: 100% Code Coverage.

Állapot: Minden tesztnek zöldnek kell lennie (PASS).

Hiány: Ha nincs teszt, vagy alacsony a lefedettség -> ÍRJ TESZTET.

Tiltott: @pytest.mark.skip (kivéve OS-specifikus okok).

4. Kód Biztonság
Bare Except: except: TILOS. Helyette: except ValueError:, except Exception as e:.

Hardcoded Path: Tilos. Használj pathlib-et vagy config fájlt.

IV. ATOMI MUNKAOLYAMAT (WORKFLOW)
Egyszerre KIZÁRÓLAG 1 FÁJLON dolgozz. Minden fájlra futtasd le ezt a ciklust:

A Feladat Ellenőrzőlistája (Checklist)
Analízis:

Fájl megnyitása, értelmezése.

Jelenlegi hibák futtatása (ruff, mypy).

Refaktorálás (Code/Debug Mode):

Import Higiénia: Rendezd (Std -> 3rd -> Local), töröld a nem használtakat.

Type Safety: Javítsd a típusokat, kezeld a DI-t (TYPE_CHECKING).

Code Safety: Bare except-ek irtása.

Docstring: Írd át/pótold magyar Google style docstringre.

Dokumentáció Szinkronizálás:

Ellenőrizd: Van docs/.../fajlnev.md?

Ha VAN: Frissítsd.

Ha NINCS: Hozd létre.

Verifikáció (Quality Gate):

.../bin/python -m ruff check [fájl] -> Kell legyen: 0 hiba.

.../bin/python -m mypy [fájl] -> Kell legyen: 0 hiba.

.../bin/python -m pytest [teszt_fájl] -> Kell legyen: PASS & 100% cov.

Atomi Commit:

Csak ha a fenti verifikáció sikeres.

Formátum: type(scope): leírás (pl. refactor(core): base_factory.py típusjavítás és magyarítás).

Adminisztráció:

QA_STATUS.md frissítése (✅ pipálás).

V. INDÍTÁS
létrehoztam/ellenőriztem a QA_STATUS.md-t.
Készen állok. Indíthatom az első Taskot?
