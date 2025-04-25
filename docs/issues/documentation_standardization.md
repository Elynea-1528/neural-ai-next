# Dokumentációs Egységesítés

## Áttekintés

A core komponensek dokumentációját egységesíteni kell a `.roo/prompts/conventions.md`-ben meghatározott szabványok szerint.

## Szükséges változtatások

### 1. Fájlnév egységesítés
- [ ] api.md és api_reference.md egységesítése api.md néven
- [ ] technical_spec.md tartalom egyesítése design_spec.md-vel
- [ ] examples.md hozzáadása ahol hiányzik
- [ ] development_checklist.md hozzáadása ahol hiányzik

### 2. Könyvtár struktúra minden komponensnél:
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
- [ ] examples.md létrehozása
- [ ] api.md formátum frissítése

#### Config komponens
- [ ] api_reference.md átnevezése api.md-re
- [ ] technical_spec.md egyesítése design_spec.md-vel
- [ ] examples.md létrehozása
- [ ] development_checklist.md létrehozása

#### Logger komponens
- [ ] api_reference.md átnevezése api.md-re
- [ ] technical_spec.md egyesítése design_spec.md-vel
- [ ] examples.md létrehozása
- [ ] development_checklist.md létrehozása

#### Storage komponens
- [ ] Jelenlegi struktúra megfelel a szabványnak, csak tartalmi felülvizsgálat szükséges

### 4. Tartalmi követelmények

#### README.md
- [ ] Egységes struktúra minden komponensnél
- [ ] Áttekintés
- [ ] Főbb funkciók
- [ ] Gyors kezdés
- [ ] Linkek további dokumentációhoz

#### API dokumentáció
- [ ] Egységes formátum
- [ ] Teljes interfész dokumentáció
- [ ] Példakódok minden metódushoz
- [ ] Kivételek dokumentálása

#### Architektúra dokumentáció
- [ ] Komponens diagram
- [ ] Függőségi struktúra
- [ ] Belső felépítés
- [ ] Integrációs pontok

#### Design specifikáció
- [ ] Követelmények
- [ ] Tervezési döntések
- [ ] Adatformátumok
- [ ] Hibakezelés
- [ ] Teljesítmény megfontolások

## Elvárt formázás

### Docstring formátum (Google style)
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

### Markdown formázás
- H1 címek csak dokumentum címhez
- H2 fő szekciókhoz
- H3 alszekciókhoz
- Kódblokkok syntax highlightinggal
- Táblázatok fejléccel
- Lista hierarchia max 3 szint

## Végrehajtási terv

1. Fájlrendszer struktúra egységesítése
2. Tartalom migrálása az új struktúrába
3. Tartalmi felülvizsgálat és frissítés
4. Review és jóváhagyás
5. CI/CD dokumentáció ellenőrzés bevezetése
