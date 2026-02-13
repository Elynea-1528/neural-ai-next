# 🎯 Kvóta-Optimalizált Modell Allokáció Terv (Hibrid: Sonnet + DeepSeek)

**Verzió:** 4.0 | **Dátum:** 2026-02-12

---

## 🎯 Áttekintés

Ez a dokumentum a Neural AI Next projekt 25 módjának kvóta-optimalizált modell allokációját tartalmazza. A stratégia **hibrid megközelítést** alkalmaz: Claude Sonnet koordinációhoz/dokumentációhoz, DeepSeek kód íráshoz, Gemini rutin feladatokhoz.

**Egységes API Key:** `Narzie2012rohaN` (minden mód ugyanazt használja)

**Kvóta Limitek:**
- **Antigravity (korlátozott):** Opus 4.6, Gemini Pro
- **Kiro Sonnet (korlátozott):** Sonnet 4.5, Sonnet 4.5 Agentic
- **Kiro DeepSeek (korlátozott):** DeepSeek 3.2
- **Gemini Flash/Pro (bőséges):** Flash, Pro High

---

## 🔄 RÉGI vs ÚJ Beállítások (Teljes Összehasonlítás)

### 🏗️ TERVEZÉSI RÉTEG (2 mód)

#### 1. architect
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ Nincs változás |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Architect-Opus-4-5` | `Architect-Opus-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | xhigh | xhigh | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.7 | 0.7 | ✅ Nincs változás |

#### 2. planner
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `claude-opus-4-6-thinking` | `kiro-claude-sonnet-4-5-agentic` | ⚠️ **VÁLTOZÁS** (kvóta spórolás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Planner-Opus-4-5` | `Planner-Sonnet-4-5-Agentic` | ⚠️ **VÁLTOZÁS** |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | xhigh | high | ⚠️ **VÁLTOZÁS** (Sonnet: high) |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.7 | 0.7 | ✅ Nincs változás |


### 🎼 KOORDINÁCIÓ (1 mód)

#### 3. orchestrator
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5-agentic` | ⚠️ **VÁLTOZÁS** (agentic reasoning) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Orchestrator-Sonnet-4-5` | `Orchestrator-Sonnet-4-5-Agentic` | ⚠️ **VÁLTOZÁS** |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.5 | 0.5 | ✅ Nincs változás |

---

### 💻 IMPLEMENTÁCIÓS RÉTEG (6 mód)

#### 4. code-new
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-claude-sonnet-4-5-thinking` | `kiro-deepseek-3-2` | ⚠️ **VÁLTOZÁS** (DeepSeek kód írás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Code-New-Sonnet-4-5` | `Code-New-DeepSeek-3-2` | ⚠️ **VÁLTOZÁS** |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

#### 5. code-refactor
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ Nincs változás |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Code-Refactor-Opus-4-5` | `Code-Refactor-Opus-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | xhigh | xhigh | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

#### 6. code-feature
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-claude-sonnet-4-5-thinking` | `kiro-deepseek-3-2` | ⚠️ **VÁLTOZÁS** (DeepSeek sima) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Code-Feature-Sonnet-4-5` | `Code-Feature-DeepSeek-3-2` | ⚠️ **VÁLTOZÁS** |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

#### 7. code-fix
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-3-pro-preview` | `gemini-3-pro-high` | ⚠️ **VÁLTOZÁS** (model név javítás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Code-Fix-Gemini-Pro` | `Code-Fix-Gemini-Pro` | ✅ Nincs változás |
| **Context Window** | 1000000 | 1000000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.2 | 0.2 | ✅ Nincs változás |


#### 8. code-optimize
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ Nincs változás |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Code-Optimize-Opus-4-5` | `Code-Optimize-Opus-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | xhigh | xhigh | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

#### 9. code-style
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-3-flash-preview` | `gemini-3-flash` | ⚠️ **VÁLTOZÁS** (model név javítás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Code-Style-Gemini-Flash` | `Code-Style-Gemini-Flash` | ✅ Nincs változás |
| **Context Window** | 1000000 | 1000000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ❌ false | ⚠️ **VÁLTOZÁS** (mechanikus feladat) |
| **Reasoning Effort** | high | - | ⚠️ **VÁLTOZÁS** (kikapcsolva) |
| **Max Tokens** | 4000 | 4000 | ✅ Nincs változás |
| **Temperature** | 0.1 | 0.1 | ✅ Nincs változás |

---

### 📝 DOKUMENTÁCIÓS RÉTEG (4 mód)

#### 10. docs-api
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-3-pro-preview` | `gemini-3-pro-high` | ⚠️ **VÁLTOZÁS** (model név javítás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Docs-API-Gemini-Pro` | `Docs-API-Gemini-Pro` | ✅ Nincs változás |
| **Context Window** | 1000000 | 1000000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.5 | 0.5 | ✅ Nincs változás |

#### 11. docs-guide
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` | ⚠️ **VÁLTOZÁS** (Kiro API) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Docs-Guide-Sonnet-4-5` | `Docs-Guide-Sonnet-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.6 | 0.6 | ✅ Nincs változás |

#### 12. docs-arch
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ Nincs változás |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Docs-Arch-Opus-4-5` | `Docs-Arch-Opus-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | xhigh | xhigh | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.6 | 0.6 | ✅ Nincs változás |

#### 13. docs-comment
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-3-flash-preview` | `gemini-3-flash` | ⚠️ **VÁLTOZÁS** (model név javítás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Docs-Comment-Gemini-Flash` | `Docs-Comment-Gemini-Flash` | ✅ Nincs változás |
| **Context Window** | 1000000 | 1000000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ❌ false | ⚠️ **VÁLTOZÁS** (mechanikus feladat) |
| **Reasoning Effort** | high | - | ⚠️ **VÁLTOZÁS** (kikapcsolva) |
| **Max Tokens** | 4000 | 4000 | ✅ Nincs változás |
| **Temperature** | 0.4 | 0.4 | ✅ Nincs változás |


---

### 🧪 TESZTELÉSI RÉTEG (4 mód)

#### 14. test-unit
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-3-pro-preview` | `gemini-3-pro-high` | ⚠️ **VÁLTOZÁS** (model név javítás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Test-Unit-Gemini-Pro` | `Test-Unit-Gemini-Pro` | ✅ Nincs változás |
| **Context Window** | 1000000 | 1000000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

#### 15. test-integration
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` | ⚠️ **VÁLTOZÁS** (Kiro API) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Test-Integration-Sonnet-4-5` | `Test-Integration-Sonnet-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

#### 16. test-property
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ Nincs változás |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Test-Property-Opus-4-5` | `Test-Property-Opus-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | xhigh | xhigh | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

#### 17. test-e2e
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` | ⚠️ **VÁLTOZÁS** (Kiro API) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Test-E2E-Sonnet-4-5` | `Test-E2E-Sonnet-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

---

### 🔧 KARBANTARTÁSI RÉTEG (3 mód)

#### 18. debug-simple
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-3-pro-preview` | `gemini-3-pro-high` | ⚠️ **VÁLTOZÁS** (model név javítás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Debug-Simple-Gemini-Pro` | `Debug-Simple-Gemini-Pro` | ✅ Nincs változás |
| **Context Window** | 1000000 | 1000000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.2 | 0.2 | ✅ Nincs változás |

#### 19. debug-complex
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ Nincs változás |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Debug-Complex-Opus-4-5` | `Debug-Complex-Opus-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | xhigh | xhigh | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

#### 20. debug-performance
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ Nincs változás |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Debug-Performance-Opus-4-5` | `Debug-Performance-Opus-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | xhigh | xhigh | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |


---

### 📖 TÁMOGATÓ RÉTEG (5 mód)

#### 21. qa
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-3-flash-preview` | `gemini-3-flash` | ⚠️ **VÁLTOZÁS** (model név javítás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `QA-Gemini-Flash` | `QA-Gemini-Flash` | ✅ Nincs változás |
| **Context Window** | 1000000 | 1000000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ❌ false | ⚠️ **VÁLTOZÁS** (mechanikus feladat) |
| **Reasoning Effort** | high | - | ⚠️ **VÁLTOZÁS** (kikapcsolva) |
| **Max Tokens** | 4000 | 4000 | ✅ Nincs változás |
| **Temperature** | 0.2 | 0.2 | ✅ Nincs változás |

#### 22. review
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` | ⚠️ **VÁLTOZÁS** (Kiro API) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Review-Sonnet-4-5` | `Review-Sonnet-4-5` | ✅ Nincs változás |
| **Context Window** | 200000 | 200000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.5 | 0.5 | ✅ Nincs változás |

#### 23. search
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-3-pro-preview` | `gemini-3-pro-high` | ⚠️ **VÁLTOZÁS** (model név javítás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Search-Gemini-Pro` | `Search-Gemini-Pro` | ✅ Nincs változás |
| **Context Window** | 1000000 | 1000000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ✅ true | ✅ Nincs változás |
| **Reasoning Effort** | high | high | ✅ Nincs változás |
| **Max Tokens** | 8000 | 8000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

#### 24. commit
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-3-flash-preview` | `gemini-3-flash` | ⚠️ **VÁLTOZÁS** (model név javítás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Commit-Gemini-Flash` | `Commit-Gemini-Flash` | ✅ Nincs változás |
| **Context Window** | 1000000 | 1000000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ❌ false | ⚠️ **VÁLTOZÁS** (mechanikus feladat) |
| **Reasoning Effort** | high | - | ⚠️ **VÁLTOZÁS** (kikapcsolva) |
| **Max Tokens** | 4000 | 4000 | ✅ Nincs változás |
| **Temperature** | 0.2 | 0.2 | ✅ Nincs változás |

#### 25. reader
| Paraméter | RÉGI | ÚJ | Változás |
|:----------|:-----|:---|:---------|
| **Model** | `gemini-3-flash-preview` | `gemini-3-flash` | ⚠️ **VÁLTOZÁS** (model név javítás) |
| **Base URL** | `http://127.0.0.1:8310/v1` | `http://127.0.0.1:8310/v1` | ✅ Nincs változás |
| **API Key** | `Reader-Gemini-Flash` | `Reader-Gemini-Flash` | ✅ Nincs változás |
| **Context Window** | 1000000 | 1000000 | ✅ Nincs változás |
| **Enable Reasoning** | ✅ true | ❌ false | ⚠️ **VÁLTOZÁS** (mechanikus feladat) |
| **Reasoning Effort** | high | - | ⚠️ **VÁLTOZÁS** (kikapcsolva) |
| **Max Tokens** | 4000 | 4000 | ✅ Nincs változás |
| **Temperature** | 0.3 | 0.3 | ✅ Nincs változás |

---

## 📊 Összesítő Táblázat (ÚJ Beállítások)

| # | Mód | Model | API | Reasoning | Temp | Max Tokens | Context |
|:--|:----|:------|:----|:----------|:-----|:-----------|:--------|
| 1 | architect | claude-opus-4-6-thinking | Kiro | xhigh | 0.7 | 8000 | 200k |
| 2 | planner | kiro-claude-sonnet-4-5-agentic | Kiro | high | 0.7 | 8000 | 200k |
| 3 | orchestrator | kiro-claude-sonnet-4-5-agentic | Kiro | high | 0.5 | 8000 | 200k |
| 4 | code-new | kiro-deepseek-3-2 | Kiro | high | 0.3 | 8000 | 200k |
| 5 | code-refactor | claude-opus-4-6-thinking | Kiro | xhigh | 0.3 | 8000 | 200k |
| 6 | code-feature | kiro-deepseek-3-2 | Kiro | high | 0.3 | 8000 | 200k |
| 7 | code-fix | gemini-3-pro-high | Kiro | high | 0.2 | 8000 | 1M |
| 8 | code-optimize | claude-opus-4-6-thinking | Kiro | xhigh | 0.3 | 8000 | 200k |
| 9 | code-style | gemini-3-flash | Kiro | disabled | 0.1 | 4000 | 1M |
| 10 | docs-api | gemini-3-pro-high | Kiro | high | 0.5 | 8000 | 1M |
| 11 | docs-guide | kiro-claude-sonnet-4-5 | Kiro | high | 0.6 | 8000 | 200k |
| 12 | docs-arch | claude-opus-4-6-thinking | Kiro | xhigh | 0.6 | 8000 | 200k |
| 13 | docs-comment | gemini-3-flash | Kiro | disabled | 0.4 | 4000 | 1M |
| 14 | test-unit | gemini-3-pro-high | Kiro | high | 0.3 | 8000 | 1M |
| 15 | test-integration | kiro-claude-sonnet-4-5 | Kiro | high | 0.3 | 8000 | 200k |
| 16 | test-property | claude-opus-4-6-thinking | Kiro | xhigh | 0.3 | 8000 | 200k |
| 17 | test-e2e | kiro-claude-sonnet-4-5 | Kiro | high | 0.3 | 8000 | 200k |
| 18 | debug-simple | gemini-3-pro-high | Kiro | high | 0.2 | 8000 | 1M |
| 19 | debug-complex | claude-opus-4-6-thinking | Kiro | xhigh | 0.3 | 8000 | 200k |
| 20 | debug-performance | claude-opus-4-6-thinking | Kiro | xhigh | 0.3 | 8000 | 200k |
| 21 | qa | gemini-3-flash | Kiro | disabled | 0.2 | 4000 | 1M |
| 22 | review | kiro-claude-sonnet-4-5 | Kiro | high | 0.5 | 8000 | 200k |
| 23 | search | gemini-3-pro-high | Kiro | high | 0.3 | 8000 | 1M |
| 24 | commit | gemini-3-flash | Kiro | disabled | 0.2 | 4000 | 1M |
| 25 | reader | gemini-3-flash | Kiro | disabled | 0.3 | 4000 | 1M |


---

## 🎯 Kvóta Elosztás Stratégia

| Forrás | Modellek | Módok (Darab) | Használat |
|:-------|:---------|:--------------|:----------|
| **Antigravity Opus (korlátozott)** | claude-opus-4-6-thinking | 7 | Kritikus döntések (architect, refactor, optimize, arch, property, debug-complex, debug-performance) |
| **Kiro Sonnet (korlátozott)** | kiro-claude-sonnet-4-5 / agentic | 6 | Koordináció, dokumentáció, tesztek (planner, orchestrator, docs-guide, test-integration, test-e2e, review) |
| **Kiro DeepSeek (korlátozott)** | kiro-deepseek-3-2 / agentic | 2 | Kód írás (code-new, code-feature) |
| **Gemini Pro (bőséges)** | gemini-3-pro-high | 5 | Rutin feladatok (code-fix, docs-api, test-unit, debug-simple, search) |
| **Gemini Flash (bőséges)** | gemini-3-flash | 5 | Mechanikus feladatok (code-style, docs-comment, qa, commit, reader) |

---

## 🔑 Kritikus Változások Összefoglalása

### Model Név Javítások (11 mód):
1. `gemini-3-pro-preview` → `gemini-3-pro-high` (6 mód: code-fix, docs-api, test-unit, debug-simple, search)
2. `gemini-3-flash-preview` → `gemini-3-flash` (5 mód: code-style, docs-comment, qa, commit, reader)

### Agentic Suffix Hozzáadása (2 mód):
1. **planner:** `claude-opus-4-6-thinking` → `kiro-claude-sonnet-4-5-agentic` (kvóta spórolás + agentic reasoning)
2. **orchestrator:** `gemini-claude-sonnet-4-5-thinking` → `kiro-claude-sonnet-4-5-agentic` (agentic reasoning)

### DeepSeek Bevezetése (2 mód):
1. **code-new:** `gemini-claude-sonnet-4-5-thinking` → `kiro-deepseek-3-2` (új modul létrehozás)
2. **code-feature:** `gemini-claude-sonnet-4-5-thinking` → `kiro-deepseek-3-2` (funkció hozzáadás)

### Kiro API Használat (4 mód):
1. **docs-guide:** `gemini-claude-sonnet-4-5-thinking` → `kiro-claude-sonnet-4-5`
2. **test-integration:** `gemini-claude-sonnet-4-5-thinking` → `kiro-claude-sonnet-4-5`
3. **test-e2e:** `gemini-claude-sonnet-4-5-thinking` → `kiro-claude-sonnet-4-5`
4. **review:** `gemini-claude-sonnet-4-5-thinking` → `kiro-claude-sonnet-4-5`

### Thinking Kikapcsolása (5 mód):
1. **code-style:** Mechanikus feladat (formatting)
2. **docs-comment:** Mechanikus feladat (inline kommentek)
3. **qa:** Mechanikus feladat (linter futtatás)
4. **commit:** Mechanikus feladat (git commit)
5. **reader:** Mechanikus feladat (fájl olvasás)

---

## 🚀 Következő Lépések

1. **Script Futtatása:** `python update_roo_models.py` (automatikusan frissíti a beállításokat)
2. **Roo Code UI Ellenőrzés:** Nyisd meg a Roo Code UI-t és ellenőrizd a frissített beállításokat
3. **Tesztelés:** Minden mód kipróbálása egyszerű feladatokkal
4. **Monitoring:** Kvóta használat figyelése (Antigravity vs Kiro vs Gemini)

---

## 📚 Kapcsolódó Dokumentumok

- **[FINAL_MODEL_ALLOCATION.md](FINAL_MODEL_ALLOCATION.md):** Teljes áttekintés (model, reasoning, temperature egy helyen)
- **[ROO_CODE_FULL_SETTINGS.md](ROO_CODE_FULL_SETTINGS.md):** Teljes Roo Code UI beállítási táblázat
- **[hierarchical_agent_system.md](hierarchical_agent_system.md):** 25 mód részletes leírása

---

## 📝 Megjegyzések

- **Egységes API Key:** `Narzie2012rohaN` (minden mód ugyanazt használja)
- **DeepSeek Context:** 200k (ellenőrizve a Kiro API-ból)
- **DeepSeek Max Tokens:** 8000 (megfelelő kód íráshoz)
- **Gemini Model Név:** `gemini-3-pro-high` (a "high" a reasoning effort level része a Kiro API-ban)
- **Thinking Disabled:** Flash modelleknél mechanikus feladatoknál (token spórolás)
- **Agentic Suffix Logika:**
  - **KELL:** Planner, Orchestrator (multi-step reasoning, koordináció)
  - **NEM KELL:** Code-New, Code-Feature (egyszerű implementáció, egy feladat)
  - **Indoklás:** Agentic = több lépésben gondolkodik, több alternatívát mérlegelget
  - **Code-Feature:** Meglévő modulhoz funkció hozzáadása = egyszerű implementáció (nem koordináció!)

---

**Verzió:** 5.0 FINAL | **Utolsó Frissítés:** 2026-02-12 | **Státusz:** ✅ VÉGLEGES

