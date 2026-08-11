# NEURAL AI NEXT – ARCHITECTURE DECISIONS & PRODUCT VISION

**Verzió:** 1.0 | **Dátum:** 2026-08-11 | **Státusz:** ✅ ACTIVE SSOT

> **Ez a dokumentum az egész termék architektúrájának, döntéseinek és roadmap-jének az egyetlen forrása (SSOT).**
> Ha a session újraindul, **ez a fájl állítja vissza a kontextust.**

---

## 🎯 TERMÉK VÍZIÓ – "AUTONOM KERESKEDÉSI ÖKOLÓGIA"

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  NEURAL AI NEXT = 25 év TICK adat → D1-D15 dimenziók → 6 rétegű AI piramis → │
│  Autonom döntéshozatal → Backtest/Marketplace → 24/7 Live                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Nem egy bot. Egy ökoszisztéma.** 3-5 év horizontál.

---

## 🏗️ RENDSZER ARCHITEKTÚRA (SSOT: `docs/development/architecture_standards.md` v4.0)

### 5 Réteg – Strict DDD (Domain-Driven Design)

| Réteg | Mappa | Felelősség | Tilos hivatkozni |
|-------|-------|------------|------------------|
| **1. Presentation** | `neural_ai/ui` | Streamlit (View + ViewModel) | - |
| **2. Domain** | `neural_ai/processors` | **AGY** – Dimenziók, Pipeline | `ui` |
| **3. Persistence** | `neural_ai/data` | Parquet IO, SQL, Ingestion | `ui`, `processors` |
| **4. Input** | `neural_ai/collectors` | JForex Bi5, MT5, IBKR | `ui`, `processors`, `data` |
| **5. Infrastructure** | `neural_ai/core` | Config, Log, EventBus, DB, DI | *Mindenre* (alappal) |

**Függőség iránya:** Kizárólag **fentről lefelé** (Presentation → Domain → Persistence → Input → Infrastructure)

### Atomic Unit Pattern (Minden Modul)

```
modul/
├── interfaces/        # ABC – Exportált (Szerződés)
├── implementations/   # Konkrét – Rejtett (__init__.py ÜRES!)
├── exceptions/        # Saját, típusos hibák
├── factory.py         # EGYETLEN belépési pont + Pydantic Config
└── __init__.py        # CSAK Factory + Interface export!
```

**Szabály:** Factory-ban KONKRÉT osztály import, kívülről CSAK Interface látszik.

---

## 📊 ADAT PIPELINE (L0-L4) – SSOT: `docs/planning/technical_design/01_processor_architecture.md`

```
L0 RAW TICK (.bi5) → L1 OHLCV → L2 ALIGNED → L3 FEATURES (D1-D15) → L4 DATASETS (.pt)
     Dukascopy          Resampler    TimeAlign      Feature Engine      Window/Label
     25 év                                                          Kaggle Export
```

| Réteg | Folyamat | Tárolás | Formátum |
|-------|----------|---------|----------|
| **L0** | Bi5 decode (LZMA) | `data/raw/{symbol}/{date}.bi5` | Native binary |
| **L1** | Tick → OHLCV (Polars) | `data/resampled/{symbol}/{tf}/` | Partitioned Parquet |
| **L2** | Gap fill + Market hours | `data/aligned/{symbol}/{tf}/` | Parquet |
| **L3** | D1-D15 processzorok | `data/features/{symbol}/{dim}/{tf}/` | Parquet per dimenzió |
| **L4** | WindowGenerator + Labels | `data/datasets/{symbol}/{ver}/` | PyTorch `.pt` tenszorok |

**Kimenet:** `data/datasets/{symbol}/{version}/{features,labels,meta}.pt` → AI bemenet

---

## ⚙️ PROCESSZOR MOTOR – D1-D15 DIMENZIÓK

**SSOT:** `docs/processors/dimensions/overview.md`

Minden processzor:
- **Input:** Polars DataFrame (time-aligned OHLCV + Bid/Mid)
- **Process:** Polars Expr (zero-copy, no Python loops)
- **Output:** Feature DataFrame (ugyanannyi sor, új oszlopok)
- **Config:** Pydantic `DimensionConfig` per dimenzió

| Dimenzió | Cél | Timeframe-k | Státusz |
|----------|-----|-------------|---------|
| **D1** | Base Data (Log Return, Z-Score, Shadows) | All | 🟡 WIP |
| **D2** | Support/Resistance | H1-H4-D1 / M1-M15 | ⏳ |
| **D3** | Trend (MACD, ADX) | H1-H4 | ⏳ |
| **D4** | Volatilitás (ATR, Bollinger) | M15-H4 | ⏳ |
| **D5** | Volumen (Delta, OBV, VP) | M15-D1 | ⏳ |
| **D6** | Piaci Microstructure | Tick-M1 | ⏳ |
| **D7** | Korreláció (Cross-asset) | H1-D1 | ⏳ |
| **D8** | Sentiment/News | H1-D1 | ⏳ |
| **D9** | Divergenciák (RSI, MACD) | M15-H4 | ⏳ |
| **D10** | Kitörések/Retestek | M15-H1 | ⏳ |
| **D11** | Összetett Minták | All | ⏳ |
| **D12** | Rendszer/Meta | All | ⏳ |
| **D13** | Kockázatkezelés | M5-H1 | ⏳ |
| **D14-D15** | Speciális/Experimental | - | 💡 |

**Kritikus szabály (SSOT):** **MID PRICE** = AI bemenet (Log Return), **BID PRICE** = Execution/Chart only.

---

## 🧠 AI MODELL PIRAMIS (6 RÉTEG)

**SSOT:** `docs/models/hierarchical/structure.md` + `docs/architecture/hierarchical_system/overview.md`

```
┌────────────────────────────────────────────────────────────────────┐
│ L6 META-LEARNING: Architecture Search, Strategy Developer, SysOpt │
├────────────────────────────────────────────────────────────────────┤
│ L5 DECISION: Signal Gen → Validator → Executor (Entry/Mgmt/Exit) │
├────────────────────────────────────────────────────────────────────┤
│ L4 CURIOSITY: Pattern Discovery, Strategy Gen, Risk Adaptation  │
├────────────────────────────────────────────────────────────────────┤
│ L3 META: Regime Detect, Risk Calc, Performance Optimizer        │
├────────────────────────────────────────────────────────────────────┤
│ L2 SPECIALIST: Trend, Volatility, Correlation Analyzers         │
├────────────────────────────────────────────────────────────────────┤
│ L1 BASE: Micro (WaveNetICM), Scalp (DualHeadGRU), Intra (QuantumLSTM)│
└────────────────────────────────────────────────────────────────────┘
```

### Modelltípusok per Szint

| Szint | Modell | Input Timeframes | ICM Focus |
|-------|--------|------------------|-----------|
| **L1 Micro** | WaveNetICM | Tick + M1 | Microstructure |
| **L1 Scalp** | DualHeadGRU | M1 + M5 | Rapid Adaptation |
| **L1 Intra** | QuantumLSTM | M15 + H1 | Trend Discovery |
| **L2 Trend** | MultiTimeframeTrendDetector | H1-H4-D1 | - |
| **L2 Volatility** | VolatilityRegimeDetector | M15-H4 | - |
| **L2 Correlation** | CrossAssetCorrelator | H1-D1 | - |
| **L3 Meta** | Regime/Risk/Performance | All dims | - |
| **L4 Curiosity** | Pattern/Strategy/Risk | All | Exploration |

**ICM (Intrinsic Curiosity Module):** Ösztönös mintázat felfedezés, strategy generation, risk adaptation.

---

## 🛠️ INFRASTRUKTÚRA & TECH STACK

| Komponens | Technológia | Verió | Megjegyzés |
|-----------|-------------|-------|------------|
| **Language** | Python | 3.12 | Strict typing |
| **Data Engine** | Polars | ≥0.20 | Expr only, no loops |
| **AI Framework** | PyTorch + Lightning | 2.5.1 / 2.5.5 | CUDA 12.1 |
| **Backtest** | VectorBT Pro | latest | Event-driven |
| **Message Bus** | ZeroMQ | latest | In-process, no broker |
| **Config** | YAML + Pydantic | v2 | SOPS encrypted secrets |
| **DB (dev)** | SQLite + aiosqlite | - | Alembic ready |
| **DB (prod)** | PostgreSQL | 15+ | Connection pool |
| **Logging** | Structlog | latest | JSON structured |
| **Monitoring** | systemd + journalctl | - | Prometheus later |

**NEM TECH STACK:** ❌ Docker, ❌ Kubernetes, ❌ NATS/RabbitMQ (most), ❌ Streamlit prod-ban

---

## 🚀 DEPLOYMENT STRATÉGIA – NATÍV LINUX (NO DOCKER)

### Szerver Architektúra

```
Server: Ubuntu 24.04 LTS
├── systemd services:
│   ├── neural-ai-live.service       # main.py live (Restart=always)
│   ├── neural-ai-dashboard.service  # Streamlit dev only (opcionális)
│   ├── neural-ai-download.timer     # Periodikus adatfrissítés
│   └── neural-ai-backup.timer       # DB backup
├── ~/miniconda3/envs/neural-ai-next/    # Isolated Python env
├── /opt/neural-ai-next/                # Deploy directory (rsync target)
├── /var/log/neural-ai/                 # Structured logs (journalctl)
└── /etc/neural-ai/                     # Runtime configs (decrypted SOPS)
```

### Config & Secrets Management

```
configs/
├── base.yaml                    # COMMITTED – közös beállítások
├── development.yaml             # COMMITTED – dev felülírások
├── production.yaml              # COMMITTED – prod felülírások
├── secrets.yaml.sops            # COMMITTED – TITKOSÍTOTT (SOPS)
└── collectors/
    ├── jforex_live.yaml
    └── mt5.yaml
```

**Merge sorrend (utolsó nyer):**
`base.yaml` → `{env}.yaml` → `secrets.yaml` (SOPS decrypt) → `.env.{env}` → `os.environ`

### Secrets: SOPS + age

| Miért SOPS? | Hogyan? |
|-------------|---------|
| Titkosított YAML a repóban | `sops -e configs/secrets.yaml > configs/secrets.yaml.sops` |
| Age kulcsok (publikus/privát) | `age-keygen -o age.key` |
| Nincs szerver-oldali vault | `age.key` csak deployer gépen + serveren |
| CI/CD-barát | GitHub Actions: `SOPS_AGE_KEY` secret |

### Deploy: SSH + rsync (Egyszerű, NEM Docker)

```bash
# deploy/scripts/deploy.sh
rsync -avz --exclude='.git' --exclude='__pycache__' ./ user@server:/opt/neural-ai-next/
ssh user@server "cd /opt/neural-ai-next && sops -d configs/secrets.yaml.sops > configs/secrets.yaml && conda activate neural-ai-next && pip install -e .[trader] && alembic upgrade head && sudo systemctl restart neural-ai-live"
```

---

## 🔐 LICENC STRATÉGIA

| Fázis | Licenc | Indok |
|-------|--------|-------|
| **Most (Core)** | **MIT** | Open source, community, contribution, bárki használhatja |
| **Később (Marketplace)** | **Dual: MIT + BSL** | Core = MIT, Strategy Packs/Model Weights = BSL/Proprietary |
| **Enterprise** | Custom/Proprietary | Ha teljes rendszer eladás |

**Döntés:** **MIT most** – open source, community building. Ha Marketplace elindul → dual licensing.

---

## 📊 DASHBOARD & UI STRATÉGIA

| Környezet | Technológia | Cél |
|-----------|-------------|-----|
| **Dev (Most)** | **Streamlit** + **Jupyter** | Gyors prototípus, processor debug, data quality check |
| **Production** | **SvelteKit/Next.js + WebSocket** | Auth, real-time, multi-user, audit trail |

**Streamlit:** Csak dev tool (`python main.py dashboard`), **NEM production UI**. Production UI = külön repo (`neural-ai-ui`), TypeScript, WebSocket, OAuth/JWT.

**Jupyter:** Mély elemzés, backtest vizualizáció, strategy research (`jupyter lab`).

---

## 🤝 GITHUB & COLLABORATION

### Repository (Monorepo)

```
neural-ai-next/
├── .github/workflows/ci.yml          # Ruff, Mypy, Pyright, PyTest
├── .github/workflows/deploy.yml      # Deploy staging/prod
├── .github/CODEOWNERS                # Review requirements per layer
├── .sops.yaml                        # SOPS rules
├── docs/                             # SSOT + Generated docs
├── neural_ai/                        # Source (DDD layers)
├── tests/                            # Mirror structure
├── scripts/                          # Install, deploy, generate
├── deploy/                           # Systemd, scripts, configs
├── configs/                          # YAML + SOPS
├── data/                             # .gitignore
├── models/                           # .gitignore
├── .env.example                      # Template only
├── pyproject.toml                    # Deps + tools
├── README.md                         # MIT, quickstart, SOPS docs
├── LICENSE                           # MIT
└── CHANGELOG.md
```

### Branch Strategy

```
main (protected) ←── release/vX.Y.Z ←── develop ←── feature/*
                        │
                        └── hotfix/* (main-ből)
```

### Collaboration Rules (Ha csatlakozik valaki)

1. **Code Owners** – review requirements per layer
2. **Conventional Commits** – `feat(processor): add d3 trend logic`
3. **Atomic Commits** – 1 logikai változás = 1 commit
4. **QA Gate** – PR nem merge-elhető ha nem zöld: Ruff + Mypy + Pyright + PyTest
5. **Documentation** – Mirror docs kötelező (`docs/components/...`)

---

## 🗺️ ROADMAP (Prioritizált)

| Fázis | Idő | Cél | Státusz |
|-------|-----|-----|---------|
| **0. Foundation** | Most | Config Loader, SOPS, Systemd, Deploy, README, CI | 🔄 **60%** |
| **1. Data Pipeline** | 2-4 hét | L0-L4 teljes, D1-D3 processzorok | 🔄 **40%** |
| **2. Base AI** | 1-2 hónap | L1 Base Analyzers (WaveNetICM, GRU, LSTM) | ⏳ |
| **3. Specialist AI** | 2-3 hónap | L2 Trend/Vol/Corr + L3 Meta | ⏳ |
| **4. Curiosity** | 3-4 hónap | L4 ICM Pattern Discovery + Strategy Gen | ⏳ |
| **5. Decision** | 4-5 hónap | L5 Signal → Position → Exit | ⏳ |
| **6. Meta-Learning** | 5-6 hónap | L6 Architecture/Search/Evolve | ⏳ |
| **7. Marketplace** | 6+ hónap | Strategy Packs, Licensing, Revenue | 💡 |

---

## 📋 JELENLEGI ÁLLAPOT (2026-08-11)

### ✅ KÉSZ
- [x] SSOT dokumentumok (7 db) – teljes
- [x] DDD architektúra + Atomic Unit pattern
- [x] Data pipeline spec (L0-L4)
- [x] D1-D15 dimenziók spec
- [x] 6 rétegű AI piramis spec
- [x] Install script (`scripts/install.py`) – CUDA detektálás, AVX2, Polars/PyArrow
- [x] Config merge koncepció (YAML → .env → env vars)
- [x] SOPS + age secrets koncepció
- [x] Systemd + rsync deployment koncepció
- [x] MIT licenc döntés
- [x] Streamlit dev-only, TS production UI
- [x] ZeroMQ message bus (no broker)
- [x] Alembic ready (de nem futtatva most)
- [x] ZeroMQ not NATS/RabbitMQ

### 🔄 FOLYAMATBAN (Phase 0 – Foundation)
- [ ] `ConfigLoader` class (`neural_ai/core/config/loader.py`)
- [ ] SOPS decrypt integráció config loaderbe
- [ ] Systemd service fájlok (3 db + timer)
- [ ] Deploy scripts (`deploy/scripts/{provision,deploy,backup,migrate}.sh`)
- [ ] README.md (MIT, quickstart, SOPS docs)
- [ ] GitHub Actions CI (ruff, mypy, pyright, pytest)
- [ ] `.sops.yaml` + `age` keygen docs
- [ ] `ARCHITECTURE_DECISIONS.md` ← **EZ A FÁJL**

### 🔴 VULNERABLE (TASK_TREE alapján)
- `neural_ai/core/__init__.py` – 2 failed test
- `scripts/audit_architecture_detailed.py` – 3 Pylance hiba
- `core/base/implementations/singleton.py` – 1 Pylance hiba

---

## 🎯 DÖNTÉSEK ÖSSZEFOGLALÓ (Q&A-ból)

| Kérdés | Döntés | Indok |
|--------|--------|-------|
| **Alembic** | Van, de **NEM FUTTATJUK MOST** | SQLite dev, prod PostgreSQL később |
| **NATS/RabbitMQ** | **NEM KELL MOST** | ZeroMQ elég single-node-ra |
| **Dashboard** | **Streamlit DEV-ben**, TS production UI később | Streamlit = dev tool |
| **Licenc** | **MIT most**, dual licensing (MIT+BSL) Marketplace-nél | Open source community |
| **Dev UI** | **Streamlit + Jupyter** kombó | Gyors iteráció + mély elemzés |
| **Docker** | **NEM** | systemd + venv natív Linux |
| **Secrets** | **SOPS + age** | Titkosított YAML repóban, age kulcsok |
| **Message Bus** | **ZeroMQ** | In-process, no broker, no hostolás |
| **DB (dev)** | SQLite | Egyszerű, file-based |
| **DB (prod)** | PostgreSQL | Alembic migration ready |

---

## 🎯 KÖVETKEZŐ LÉPÉS – ARCHITECT PARANCS

> **"Tervezd meg a Phase 0 (Foundation) implementációját: Config Loader + SOPS decrypt + Systemd services + Deploy scripts + README.md (MIT license, quickstart, SOPS docs) + GitHub Actions CI. NO DOCKER, systemd + venv, MIT license, Streamlit dev-only. Meglévő SSOT dokumentumok alapján."**

---

## 📎 CSATOLÁNYOK / HIVATKOZÁSOK

- `docs/processors/dimensions/overview.md` – D1-D15 spec
- `docs/planning/technical_design/01_processor_architecture.md` – Pipeline arch
- `docs/models/hierarchical/structure.md` – AI piramis
- `docs/architecture/hierarchical_system/overview.md` – Rendszer áttekintés
- `docs/development/architecture_standards.md` – Codex v4.0
- `docs/development/custom-instructions.md` – Kernel v8.0
- `docs/development/TASK_TREE.md` – Granular dashboard

---

**EZ A DOKUMENTUM A PROJEKT MEMÓRIÁJA. HA ÚJRAINDULUNK, EZ VISSZAÁLLÍTJA A KONTEXTSZT.**
