# Neural AI Next - Core Komponensek Fejlesztési Kontextus

## 1. Rendszerszintű Dokumentáció
- [Rendszer Architektúra](../../docs/architecture/overview.md)
- [Hierarchikus Rendszer](../../docs/architecture/hierarchical_system/overview.md)
- [Modell Struktúra](../../docs/models/hierarchical/structure.md)
- [Dimenzió Processzorok](../../docs/processors/dimensions/overview.md)

## 2. Core Komponensek

### 2.1 Base Komponens
- [Áttekintés és használat](../../docs/components/base/README.md)
- [API Dokumentáció](../../docs/components/base/api.md)
- [Architektúra](../../docs/components/base/architecture.md)
- [Fejlesztési Checklist](../../docs/components/base/development_checklist.md)
- [Példák](../../docs/components/base/examples.md)
- [Változások](../../docs/components/base/CHANGELOG.md)

### 2.2 Config Komponens
- [Áttekintés és használat](../../docs/components/config/README.md)
- [API Dokumentáció](../../docs/components/config/api.md)
- [Architektúra](../../docs/components/config/architecture.md)
- [Tervezési Specifikáció](../../docs/components/config/design_spec.md)
- [Fejlesztési Checklist](../../docs/components/config/development_checklist.md)
- [Példák](../../docs/components/config/examples.md)
- [Közreműködés](../../docs/components/config/CONTRIBUTING.md)
- [Változások](../../docs/components/config/CHANGELOG.md)

### 2.3 Logger Komponens
- [Áttekintés és használat](../../docs/components/logger/README.md)
- [API Dokumentáció](../../docs/components/logger/api.md)
- [Architektúra](../../docs/components/logger/architecture.md)
- [Tervezési Specifikáció](../../docs/components/logger/design_spec.md)
- [Fejlesztési Checklist](../../docs/components/logger/development_checklist.md)
- [Példák](../../docs/components/logger/examples.md)
- [Közreműködés](../../docs/components/logger/CONTRIBUTING.md)
- [Változások](../../docs/components/logger/CHANGELOG.md)

### 2.4 Storage Komponens
- [Áttekintés és használat](../../docs/components/storage/README.md)
- [API Dokumentáció](../../docs/components/storage/api.md)
- [Architektúra](../../docs/components/storage/architecture.md)
- [Tervezési Specifikáció](../../docs/components/storage/design_spec.md)
- [Fejlesztési Checklist](../../docs/components/storage/development_checklist.md)
- [Példák](../../docs/components/storage/examples.md)
- [Változások](../../docs/components/storage/CHANGELOG.md)

## 3. Fejlesztési Útmutatók
- [Egységes Fejlesztési Útmutató](../../docs/development/unified_development_guide.md)
- [Komponens Fejlesztési Útmutató](../../docs/development/component_development_guide.md)
- [Implementációs Útmutató](../../docs/development/implementation_guide.md)
- [Code Review Útmutató](../../docs/development/code_review_guide.md)
- [Teljesítmény Optimalizáció](../../docs/development/performance_optimization.md)
- [Hibakezelés](../../docs/development/error_handling.md)
- [Core Függőségek](../../docs/development/core_dependencies.md)
- [Fejlesztési Státusz](../../docs/development/DEVELOPMENT_STATUS.md)

## 4. Template és Példák
- [Komponens Template](../../docs/templates/component_template.py)
- [Interfész Template](../../docs/templates/interface_template.py)
- [Modul Template](../../docs/templates/module_template.py)
- [Test Template](../../docs/templates/test_template.py)
- [Processor Template](../../docs/templates/processor_template.py)
- [Config Template](../../docs/templates/config_template.py)
- [Storage Template](../../docs/templates/storage_template.py)
- [Collector Template](../../docs/templates/collector_template.py)
- [Model Template](../../docs/templates/model_template.py)

## 5. Aktuális Feladatok

### 5.1 Dokumentációs Standardizálás ✓
- [Standardizálási Terv](../../docs/issues/documentation_standardization.md)
- ✓ Egységes dokumentációs struktúra kialakítva
- ✓ CI/CD pipeline bővítve dokumentáció ellenőrzéssel
- ✓ Formázási szabályok implementálva

### 5.2 Template Kód Fejlesztés
- [Részletes terv](../../docs/issues/template_code_fixes.md)

#### 5.2.1 Magas prioritású feladatok
- [ ] Undefined nevek javítása
- [ ] Hiányzó típusannotációk pótlása
- [ ] Kritikus docstring hibák javítása

#### 5.2.2 Közepes prioritású feladatok
- [ ] Import tisztítás
- [ ] Kivétel osztályok implementálása
- [ ] Docstring formázási hibák javítása

#### 5.2.3 Alacsony prioritású feladatok
- [ ] Biztonsági fejlesztések
- [ ] Type stub fájlok létrehozása
- [ ] Dokumentáció frissítése

## 6. Könyvtár Struktúra

```
neural_ai/
├── core/                     # Core komponensek
│   ├── base/                # Alap infrastruktúra
│   ├── config/              # Konfigurációkezelés
│   ├── logger/              # Naplózás
│   └── storage/             # Adattárolás
├── collectors/              # Adatgyűjtők
├── processors/              # Adatfeldolgozók
├── models/                  # Modell definíciók
└── utils/                   # Segédeszközök

tests/                       # Tesztek
└── core/                    # Core tesztek

docs/                        # Dokumentáció
├── architecture/           # Rendszerarchitektúra
├── components/            # Komponens dokumentáció
├── development/          # Fejlesztői útmutatók
└── templates/            # Kód sablonok
```

## 7. Következő lépések

1. Template kód javítások:
   - Undefined nevek javítása
   - Típusannotációk pótlása
   - Import optimalizálás
   - Docstring formázás

2. CI/CD pipeline bővítés:
   - Típusellenőrzés bevezetése
   - Biztonsági scan konfigurálása
   - Teljes körű tesztelés automatizálása
