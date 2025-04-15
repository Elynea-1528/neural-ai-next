# Neural-AI Copilot Prompt Kontextus

## 1. Rendszerszintű Dokumentáció
- [Rendszer Architektúra](../../docs/architecture/overview.md)
- [Hierarchikus Rendszer Áttekintés](../../docs/architecture/hierarchical_system/overview.md)
- [Hierarchikus Modell Struktúra](../../docs/models/hierarchical/structure.md)
- [Dimenzió Processzorok](../../docs/processors/dimensions/overview.md)

## 2. Core Komponensek
- [Logger Dokumentáció](../../docs/components/logger/design_spec.md)
- [Konfiguráció Dokumentáció](../../docs/components/config/design_spec.md)
- [Storage Dokumentáció](../../docs/components/storage/design_spec.md)

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

## 7. Projekt Hierarchia

/neural-ai-next
├── neural_ai/                       # Fő kódkönyvtár
│   ├── __init__.py
│   ├── collectors/                  # Adatgyűjtők
│   │   ├── __init__.py
│   │   ├── interfaces/
│   │   ├── mt5_collector.py
│   │   └── utils/
│   ├── processors/                  # Adatfeldolgozók dimenziónként csoportosítva
│   │   ├── __init__.py
│   │   ├── base_processor.py
│   │   ├── d1_price_action/
│   │   ├── d2_support_resistance/
│   │   ├── d3_trend/
│   │   └── ...                      # Többi dimenzió processzor
│   ├── models/                      # Modell definíciók
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── hierarchical/            # Hierarchikus modellek
│   │   ├── specialists/             # Specializált elemzők
│   │   └── meta_analyzers/          # Meta-elemzők
│   ├── trainers/                    # Modell tanítók
│   │   ├── __init__.py
│   │   ├── base_trainer.py
│   │   └── lightning_trainers/
│   ├── evaluators/                  # Kiértékelők
│   │   ├── __init__.py
│   │   └── metrics/
│   ├── core/                        # Alapvető komponensek
│   │   ├── __init__.py
│   │   ├── logger/                  # Logger rendszer
│   │   ├── config/                  # Konfigurációkezelés
│   │   └── storage/                 # Adattárolás
│   └── utils/                       # Segédeszközök
│       ├── __init__.py
│       └── visualization/
├── mql5/                            # MetaTrader kliens kód
│   ├── Experts/
│   └── Include/
├── tests/                           # Tesztek
│   ├── collectors/
│   ├── processors/
│   ├── models/
│   └── core/
├── docs/                            # Dokumentáció
│   ├── README.md
│   ├── architecture/
│   ├── components/
│   └── api/
├── configs/                         # Konfigurációs fájlok
│   ├── app/                         # Alkalmazás konfigurációk
│   ├── collectors/
│   └── processors/
├── data/                            # Adatok
│   ├── raw/                         # Nyers adatok
│   ├── processed/                   # Feldolgozott adatok
│   └── features/                    # Feature adatok
├── logs/                            # Logfájlok
│   ├── app/
│   └── training/
├── models/                          # Modellek mentései
│   ├── checkpoints/
│   └── exported/
├── examples/                        # Példakódok
└── notebooks/                       # Jupyter notebookok
