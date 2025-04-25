# Dokumentációs Egységesítés

## Áttekintés

A core komponensek dokumentációját egységesíteni kell a `.roo/prompts/conventions.md`-ben meghatározott szabványok szerint.

## Szükséges változtatások

### 1. Fájlnév egységesítés ✓
- [x] api.md és api_reference.md egységesítése api.md néven
- [x] technical_spec.md tartalom egyesítése design_spec.md-vel
- [x] examples.md hozzáadása ahol hiányzik
- [x] development_checklist.md hozzáadása ahol hiányzik

### 2. Könyvtár struktúra minden komponensnél ✓
```
/docs/components/[komponens_név]/
  ├── README.md                 # Áttekintés és használati útmutató
  ├── api.md                    # API dokumentáció
  ├── architecture.md           # Architektúra leírás
  ├── design_spec.md           # Tervezési specifikáció
  ├── development_checklist.md # Fejlesztési checklist
  ├── examples.md              # Használati példák
  └── CHANGELOG.md             # Változások követése
```

### 3. Komponens specifikus feladatok

#### Base komponens
- [x] examples.md létrehozása
- [x] api.md formátum frissítése
- [x] README.md egységesítése

#### Config komponens
- [x] api_reference.md átnevezése api.md-re
- [x] technical_spec.md egyesítése design_spec.md-vel
- [x] examples.md létrehozása
- [x] development_checklist.md létrehozása
- [x] README.md egységesítése

#### Logger komponens
- [x] api_reference.md átnevezése api.md-re
- [x] technical_spec.md egyesítése design_spec.md-vel
- [x] examples.md létrehozása
- [x] development_checklist.md létrehozása
- [x] README.md egységesítése

#### Storage komponens
- [x] Jelenlegi struktúra megfelel a szabványnak
- [x] README.md egységesítése
- [x] Tartalmi felülvizsgálat végrehajtva

### 4. Tartalmi követelmények

#### README.md ✓
- [x] Egységes struktúra minden komponensnél
- [x] Áttekintés
- [x] Főbb funkciók
- [x] Gyors kezdés
- [x] Linkek további dokumentációhoz

#### API dokumentáció ✓
- [x] Egységes formátum
- [x] Teljes interfész dokumentáció
- [x] Példakódok minden metódushoz
- [x] Kivételek dokumentálása

#### Architektúra dokumentáció ✓
- [x] Komponens diagram
- [x] Függőségi struktúra
- [x] Belső felépítés
- [x] Integrációs pontok

#### Design specifikáció ✓
- [x] Követelmények
- [x] Tervezési döntések
- [x] Adatformátumok
- [x] Hibakezelés
- [x] Teljesítmény megfontolások

## Elvárt formázás

### Docstring formátum (Google style) ✓
```python
def method(param: Type) -> ReturnType:
    """Rövid leírás.

    Részletes leírás több
    sorban.

    Args:
        param: Paraméter leírása

    Returns:
        Visszatérési érték leírása

    Raises:
        ExceptionType: Kivétel leírása
    """
```

### Markdown formázás ✓
- [x] H1 címek csak dokumentum címhez
- [x] H2 fő szekciókhoz
- [x] H3 alszekciókhoz
- [x] Kódblokkok syntax highlightinggal
- [x] Táblázatok fejléccel
- [x] Lista hierarchia max 3 szint

## Végrehajtási terv

1. [x] Fájlrendszer struktúra egységesítése
2. [x] Tartalom migrálása az új struktúrába
3. [x] Tartalmi felülvizsgálat és frissítés
4. [x] Review és jóváhagyás
5. [ ] CI/CD dokumentáció ellenőrzés bevezetése

## Következő lépések

1. CI/CD pipeline bővítése dokumentáció ellenőrzéssel:
   - Markdown lint
   - Docstring ellenőrzés
   - Link validáció
   - Formázási szabályok ellenőrzése

2. Automatikus dokumentáció generálás bevezetése:
   - API dokumentáció generálás docstringekből
   - Changelog automatikus generálása commit üzenetekből
   - Példakódok tesztelése
