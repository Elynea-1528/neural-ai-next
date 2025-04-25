# Neural-AI Copilot Prompt Kontextus

## 1. Rendszerszintű Dokumentáció
- [Rendszer Architektúra](../../docs/architecture/overview.md)
- [Hierarchikus Rendszer Áttekintés](../../docs/architecture/hierarchical_system/overview.md)
- [Hierarchikus Modell Struktúra](../../docs/models/hierarchical/structure.md)
- [Dimenzió Processzorok](../../docs/processors/dimensions/overview.md)

## 2. Core Komponensek

### 2.1 Base Komponens
- [Áttekintés és API](../../docs/components/base/api.md)
- [Architektúra](../../docs/components/base/architecture.md)
- [Fejlesztési checklist](../../docs/components/base/development_checklist.md)

### 2.2 Config Komponens
- [Áttekintés](../../docs/components/config/README.md)
- [API Dokumentáció](../../docs/components/config/api.md)
- [Architektúra](../../docs/components/config/architecture.md)
- [Tervezési Specifikáció](../../docs/components/config/design_spec.md)
- [Közreműködési Útmutató](../../docs/components/config/CONTRIBUTING.md)

### 2.3 Logger Komponens
- [Áttekintés](../../docs/components/logger/README.md)
- [API Dokumentáció](../../docs/components/logger/api.md)
- [Architektúra](../../docs/components/logger/architecture.md)
- [Tervezési Specifikáció](../../docs/components/logger/design_spec.md)
- [Közreműködési Útmutató](../../docs/components/logger/CONTRIBUTING.md)

### 2.4 Storage Komponens
- [Áttekintés](../../docs/components/storage/README.md)
- [API Dokumentáció](../../docs/components/storage/api.md)
- [Architektúra](../../docs/components/storage/architecture.md)
- [Tervezési Specifikáció](../../docs/components/storage/design_spec.md)
- [Példák](../../docs/components/storage/examples.md)
- [Fejlesztési Checklist](../../docs/components/storage/development_checklist.md)

## 3. Collector Komponensek
- [MT5 Collector Dokumentáció](../../docs/components/collectors/mt5/design_spec.md)

## 4. Fejlesztési Útmutatók
- [Egységes Fejlesztési Útmutató](../../docs/development/unified_development_guide.md)
- [Komponens Fejlesztési Útmutató](../../docs/development/component_development_guide.md)
- [Code Review Útmutató](../../docs/development/code_review_guide.md)
- [Teljesítmény Optimalizációs Útmutató](../../docs/development/performance_optimization.md)
- [Hibakezelési Útmutató](../../docs/development/error_handling.md)

## 5. GitHub Workflow
- [Issue Template-ek](../../.github/ISSUE_TEMPLATE/)
- [Pull Request Template](../../.github/PULL_REQUEST_TEMPLATE.md)
- [CI Workflow](../../.github/workflows/ci.yml)
- [Release Workflow](../../.github/workflows/release.yml)
- [Nightly Build Workflow](../../.github/workflows/nightly.yml)

## 6. Template Referenciák
- [Komponens Template](../../docs/templates/component_template.py)
- [Interfész Template](../../docs/templates/interface_template.py)
- [Modul Template](../../docs/templates/module_template.py)
- [Test Template](../../docs/templates/test_template.py)
- [Processor Template](../../docs/templates/processor_template.py)
- [Config Template](../../docs/templates/config_template.py)
- [Collector Template](../../docs/templates/collector_template.py)
- [Storage Template](../../docs/templates/storage_template.py)
- [Model Template](../../docs/templates/model_template.py)

## 7. Dokumentációs Standardok
- [Dokumentációs Struktúra](../../docs/issues/documentation_standardization.md)
- [Template Fixes](../../docs/issues/template_fixes.md)

## 8. Projekt Hierarchia

/neural-ai-next
├── neural_ai/                       # Fő kódkönyvtár
│   ├── core/                        # Core komponensek
│   │   ├── base/                   # Alap infrastruktúra
│   │   ├── config/                 # Konfigurációkezelés
│   │   ├── logger/                 # Naplózás
│   │   └── storage/                # Adattárolás
│   ├── collectors/                  # Adatgyűjtők
│   ├── processors/                  # Adatfeldolgozók
│   ├── models/                      # Modell definíciók
│   ├── trainers/                    # Modell tanítók
│   ├── evaluators/                  # Kiértékelők
│   └── utils/                       # Segédeszközök
├── tests/                           # Tesztek
├── docs/                            # Dokumentáció
├── configs/                         # Konfigurációs fájlok
├── data/                            # Adatok
├── logs/                            # Logfájlok
├── models/                          # Modellek mentései
├── examples/                        # Példakódok
└── notebooks/                       # Jupyter notebookok
