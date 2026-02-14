# 🎯 Roo Code - 25 Mód TELJES Beállítási Táblázat

**Verzió:** 3.0 | **Dátum:** 2026-02-05

---

## 📋 Közös Beállítások (Minden Módhoz)

| Paraméter | Érték | Megjegyzés |
|:----------|:------|:-----------|
| **API Provider** | OpenAI Compatible | Antigravity proxy |
| **Base URL** | `http://127.0.0.1:8317/v1` | Localhost proxy |
| **API Key** | `sk-bhyHlTRPU6hG9pVVw42FvLCkZMAqPj1VV3NpIPDqEmUh0` | Antigravity API key |
| **Image Support** | ❌ Does not support images | Backend projekt, nincs UI |
| **Prompt Caching** | ✅ Supports prompt caching | 83% token megtakarítás |
| **Enable R1 model parameters** | ❌ Disabled | Csak DeepSeek R1-hez kell! |
| **Enable streaming** | ✅ Enabled | Valós idejű válasz |
| **Include max output tokens** | ✅ Enabled | Token limit beállítás |
| **Use Azure** | ❌ Disabled | Nem Azure API |
| **Set Azure API version** | ❌ Disabled | Nem Azure API |
| **Input Price** | 0 | Ingyenes (proxy) |
| **Output Price** | 0 | Ingyenes (proxy) |
| **Cache Reads Price** | 0 | Ingyenes (proxy) |
| **Cache Writes Price** | 0 | Ingyenes (proxy) |
| **Rate limit** | 0s | Nincs rate limit |
| **Error & Repetition Limit** | 3 | Max 3 újrapróbálkozás |
| **Enable todo list tool** | ✅ Enabled | Task tracking |

---

## 🏗️ TERVEZÉSI RÉTEG (2 mód)

### 1. architect
| Paraméter | Érték | Megjegyzés |
|:----------|:------|:-----------|
| **Configuration Profile** | Architect (Opus 4.5) | Profil név |
| **Model** | `claude-opus-4-5` | Antigravity model ID |
| **Context Window** | 200000 tokens | Claude max context |
| **Enable Reasoning Effort** | ✅ Enabled | Extended thinking |
| **Model Reasoning Effort** | Extra High | Legmagasabb szint |
| **Max Output Tokens** | 8000 | Komplex tervezéshez |
| **Use custom temperature** | ✅ Enabled | Egyedi hőmérséklet |
| **Temperature** | 0.7 | Kreatív tervezés |
| **Input Price** | 0 | Proxy: ingyenes |
| **Output Price** | 0 | Proxy: ingyenes |
| **Cache Reads Price** | 0 | Proxy: ingyenes |
| **Cache Writes Price** | 0 | Proxy: ingyenes |

### 2. planner
| Paraméter | Érték | Megjegyzés |
|:----------|:------|:-----------|
| **Configuration Profile** | Planner (Opus 4.5) | Profil név |
| **Model** | `claude-opus-4-5` | Antigravity model ID |
| **Context Window** | 200000 tokens | Claude max context |
| **Enable Reasoning Effort** | ✅ Enabled | Extended thinking |
| **Model Reasoning Effort** | Extra High | Legmagasabb szint |
| **Max Output Tokens** | 8000 | Komplex tervezéshez |
| **Use custom temperature** | ✅ Enabled | Egyedi hőmérséklet |
| **Temperature** | 0.7 | Kreatív tervezés |
| **Input Price** | 0 | Proxy: ingyenes |
| **Output Price** | 0 | Proxy: ingyenes |
| **Cache Reads Price** | 0 | Proxy: ingyenes |
| **Cache Writes Price** | 0 | Proxy: ingyenes |

---

## 🎼 KOORDINÁCIÓ (1 mód)

### 3. orchestrator
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Orchestrator (Sonnet 4.5) |
| **Model** | `claude-sonnet-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.5 |

---

## 💻 IMPLEMENTÁCIÓS RÉTEG (6 mód)

### 4. code-new
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Code-New (Sonnet 4.5) |
| **Model** | `claude-sonnet-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

### 5. code-refactor
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Code-Refactor (Opus 4.5) |
| **Model** | `claude-opus-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | Extra High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

### 6. code-feature
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Code-Feature (Sonnet 4.5) |
| **Model** | `claude-sonnet-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

### 7. code-fix
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Code-Fix (Gemini Pro) |
| **Model** | `gemini-3-pro-preview` |
| **Context Window** | 1000000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.2 |

### 8. code-optimize
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Code-Optimize (Opus 4.5) |
| **Model** | `claude-opus-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | Extra High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

### 9. code-style
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Code-Style (Gemini Flash) |
| **Model** | `gemini-3-flash-preview` |
| **Context Window** | 1000000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 4000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.1 |

---

## 📝 DOKUMENTÁCIÓS RÉTEG (4 mód)

### 10. docs-api
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Docs-API (Gemini Pro) |
| **Model** | `gemini-3-pro-preview` |
| **Context Window** | 1000000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.5 |

### 11. docs-guide
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Docs-Guide (Sonnet 4.5) |
| **Model** | `claude-sonnet-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.6 |

### 12. docs-arch
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Docs-Arch (Opus 4.5) |
| **Model** | `claude-opus-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | Extra High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.6 |

### 13. docs-comment
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Docs-Comment (Gemini Flash) |
| **Model** | `gemini-3-flash-preview` |
| **Context Window** | 1000000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 4000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.4 |

---

## 🧪 TESZTELÉSI RÉTEG (4 mód)

### 14. test-unit
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Test-Unit (Gemini Pro) |
| **Model** | `gemini-3-pro-preview` |
| **Context Window** | 1000000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

### 15. test-integration
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Test-Integration (Sonnet 4.5) |
| **Model** | `claude-sonnet-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

### 16. test-property
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Test-Property (Opus 4.5) |
| **Model** | `claude-opus-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | Extra High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

### 17. test-e2e
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Test-E2E (Sonnet 4.5) |
| **Model** | `claude-sonnet-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

---

## 🔧 KARBANTARTÁSI RÉTEG (3 mód)

### 18. debug-simple
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Debug-Simple (Gemini Pro) |
| **Model** | `gemini-3-pro-preview` |
| **Context Window** | 1000000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.2 |

### 19. debug-complex
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Debug-Complex (Opus 4.5) |
| **Model** | `claude-opus-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | Extra High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

### 20. debug-performance
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Debug-Performance (Opus 4.5) |
| **Model** | `claude-opus-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | Extra High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

---

## 📖 TÁMOGATÓ RÉTEG (5 mód)

### 21. qa
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | QA (Gemini Flash) |
| **Model** | `gemini-3-flash-preview` |
| **Context Window** | 1000000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 4000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.2 |

### 22. review
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Review (Sonnet 4.5) |
| **Model** | `claude-sonnet-4-5` |
| **Context Window** | 200000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.5 |

### 23. search
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Search (Gemini Pro) |
| **Model** | `gemini-3-pro-preview` |
| **Context Window** | 1000000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 8000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

### 24. commit
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Commit (Gemini Flash) |
| **Model** | `gemini-3-flash-preview` |
| **Context Window** | 1000000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 4000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.2 |

### 25. reader
| Paraméter | Érték |
|:----------|:------|
| **Configuration Profile** | Reader (Gemini Flash) |
| **Model** | `gemini-3-flash-preview` |
| **Context Window** | 1000000 tokens |
| **Enable Reasoning Effort** | ✅ Enabled |
| **Model Reasoning Effort** | High |
| **Max Output Tokens** | 4000 |
| **Use custom temperature** | ✅ Enabled |
| **Temperature** | 0.3 |

---

## 📊 Gyors Összesítő Táblázat

| # | Mód | Model | Reasoning | Temp | Max Tokens | Context |
|:--|:----|:------|:----------|:-----|:-----------|:--------|
| 1 | architect | claude-opus-4-5 | Extra High | 0.7 | 8000 | 200k |
| 2 | planner | claude-opus-4-5 | Extra High | 0.7 | 8000 | 200k |
| 3 | orchestrator | claude-sonnet-4-5 | High | 0.5 | 8000 | 200k |
| 4 | code-new | claude-sonnet-4-5 | High | 0.3 | 8000 | 200k |
| 5 | code-refactor | claude-opus-4-5 | Extra High | 0.3 | 8000 | 200k |
| 6 | code-feature | claude-sonnet-4-5 | High | 0.3 | 8000 | 200k |
| 7 | code-fix | gemini-3-pro-preview | High | 0.2 | 8000 | 1M |
| 8 | code-optimize | claude-opus-4-5 | Extra High | 0.3 | 8000 | 200k |
| 9 | code-style | gemini-3-flash-preview | High | 0.1 | 4000 | 1M |
| 10 | docs-api | gemini-3-pro-preview | High | 0.5 | 8000 | 1M |
| 11 | docs-guide | claude-sonnet-4-5 | High | 0.6 | 8000 | 200k |
| 12 | docs-arch | claude-opus-4-5 | Extra High | 0.6 | 8000 | 200k |
| 13 | docs-comment | gemini-3-flash-preview | High | 0.4 | 4000 | 1M |
| 14 | test-unit | gemini-3-pro-preview | High | 0.3 | 8000 | 1M |
| 15 | test-integration | claude-sonnet-4-5 | High | 0.3 | 8000 | 200k |
| 16 | test-property | claude-opus-4-5 | Extra High | 0.3 | 8000 | 200k |
| 17 | test-e2e | claude-sonnet-4-5 | High | 0.3 | 8000 | 200k |
| 18 | debug-simple | gemini-3-pro-preview | High | 0.2 | 8000 | 1M |
| 19 | debug-complex | claude-opus-4-5 | Extra High | 0.3 | 8000 | 200k |
| 20 | debug-performance | claude-opus-4-5 | Extra High | 0.3 | 8000 | 200k |
| 21 | qa | gemini-3-flash-preview | High | 0.2 | 4000 | 1M |
| 22 | review | claude-sonnet-4-5 | High | 0.5 | 8000 | 200k |
| 23 | search | gemini-3-pro-preview | High | 0.3 | 8000 | 1M |
| 24 | commit | gemini-3-flash-preview | High | 0.2 | 4000 | 1M |
| 25 | reader | gemini-3-flash-preview | High | 0.3 | 4000 | 1M |

---

## 🎯 Beállítási Lépések

1. **Providers → Configuration Profile → "+" gomb**
2. **Add meg a profil nevét** (pl. "Architect (Opus 4.5)")
3. **Állítsd be a paramétereket** a fenti táblázat szerint
4. **Mentsd el** a profilt
5. **Ismételd meg** mind a 25 módhoz
6. **Custom Modes → Rendeld hozzá** a profilokat a módokhoz

---

**Minden sikert a beállításhoz!** 🚀
