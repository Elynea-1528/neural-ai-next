# 📊 Részletes Mód Összehasonlítás (JELENLEGI vs ÚJ)

**Verzió:** 5.0 FINAL | **Dátum:** 2026-02-12

---

## 🎯 Összefoglaló

Ez a dokumentum tartalmazza az ÖSSZES mód (25 db) részletes beállításait:
- **JELENLEGI:** A roo-code-settings.json-ban lévő beállítások
- **ÚJ:** A script által frissített beállítások

**Fő változások:**
1. ✅ API Key egységesítés: `Narzie2012rohaN` (minden mód)
2. ✅ Model ID frissítések (11 mód)
3. ✅ Reasoning beállítások frissítése (5 mód)

---

## 📋 25 Mód Részletes Táblázata

### Jelmagyarázat:
- ✅ = Nincs változás
- ⚠️ = Változik
- 🔴 = Kritikus változás

---


## 1. Architect (Opus 4.6)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ |
| **openAiApiKey** | `Architect-Opus-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `xhigh` | `xhigh` | ✅ |
| **modelTemperature** | `0.7` | `0.7` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 2. Planner (Opus 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `claude-opus-4-6-thinking` | `kiro-claude-sonnet-4-5-agentic` | 🔴 |
| **openAiApiKey** | `Planner-Opus-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `xhigh` | `high` | ⚠️ |
| **modelTemperature** | `0.7` | `0.7` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 3. Orchestrator (Sonnet 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5-agentic` | 🔴 |
| **openAiApiKey** | `Orchestrator-Sonnet-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.5` | `0.5` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 4. Code-New (Sonnet 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-claude-sonnet-4-5-thinking` | `kiro-deepseek-3-2` | 🔴 |
| **openAiApiKey** | `Code-New-Sonnet-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 5. Code-Refactor (Opus 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ |
| **openAiApiKey** | `Code-Refactor-Opus-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `xhigh` | `xhigh` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 6. Code-Feature (Sonnet 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-claude-sonnet-4-5-thinking` | `kiro-deepseek-3-2` | 🔴 |
| **openAiApiKey** | `Code-Feature-Sonnet-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 7. Code-Fix (Gemini Pro)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-3-pro-preview` | `gemini-3-pro-high` | ⚠️ |
| **openAiApiKey** | `Code-Fix-Gemini-Pro` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.2` | `0.2` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `1000000` | `1000000` | ✅ |

---

## 8. Code-Optimize (Opus 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ |
| **openAiApiKey** | `Code-Optimize-Opus-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `xhigh` | `xhigh` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 9. Code-Style (Gemini Flash)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-3-flash-preview` | `gemini-3-flash` | ⚠️ |
| **openAiApiKey** | `Code-Style-Gemini-Flash` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `false` | 🔴 |
| **reasoningEffort** | `high` | (törlődik) | 🔴 |
| **modelTemperature** | `0.1` | `0.1` | ✅ |
| **maxTokens** | `4000` | `4000` | ✅ |
| **contextWindow** | `1000000` | `1000000` | ✅ |

---

## 10. Docs-API (Gemini Pro)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-3-pro-preview` | `gemini-3-pro-high` | ⚠️ |
| **openAiApiKey** | `Docs-API-Gemini-Pro` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.5` | `0.5` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `1000000` | `1000000` | ✅ |

---

## 11. Docs-Guide (Sonnet 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` | ⚠️ |
| **openAiApiKey** | `Docs-Guide-Sonnet-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.6` | `0.6` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 12. Docs-Arch (Opus 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ |
| **openAiApiKey** | `Docs-Arch-Opus-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `xhigh` | `xhigh` | ✅ |
| **modelTemperature** | `0.6` | `0.6` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 13. Docs-Comment (Gemini Flash)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-3-flash-preview` | `gemini-3-flash` | ⚠️ |
| **openAiApiKey** | `Docs-Comment-Gemini-Flash` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `false` | 🔴 |
| **reasoningEffort** | `high` | (törlődik) | 🔴 |
| **modelTemperature** | `0.4` | `0.4` | ✅ |
| **maxTokens** | `4000` | `4000` | ✅ |
| **contextWindow** | `1000000` | `1000000` | ✅ |

---


## 14. Test-Unit (Gemini Pro)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-3-pro-preview` | `gemini-3-pro-high` | ⚠️ |
| **openAiApiKey** | `Test-Unit-Gemini-Pro` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `1000000` | `1000000` | ✅ |

---

## 15. Test-Integration (Sonnet 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` | ⚠️ |
| **openAiApiKey** | `Test-Integration-Sonnet-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 16. Test-Property (Opus 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ |
| **openAiApiKey** | `Test-Property-Opus-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `xhigh` | `xhigh` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 17. Test-E2E (Sonnet 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` | ⚠️ |
| **openAiApiKey** | `Test-E2E-Sonnet-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 18. Debug-Simple (Gemini Pro)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-3-pro-preview` | `gemini-3-pro-high` | ⚠️ |
| **openAiApiKey** | `Debug-Simple-Gemini-Pro` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.2` | `0.2` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `1000000` | `1000000` | ✅ |

---

## 19. Debug-Complex (Opus 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ |
| **openAiApiKey** | `Debug-Complex-Opus-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `xhigh` | `xhigh` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 20. Debug-Performance (Opus 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `claude-opus-4-6-thinking` | `claude-opus-4-6-thinking` | ✅ |
| **openAiApiKey** | `Debug-Performance-Opus-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `xhigh` | `xhigh` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 21. QA (Gemini Flash)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-3-flash-preview` | `gemini-3-flash` | ⚠️ |
| **openAiApiKey** | `QA-Gemini-Flash` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `false` | 🔴 |
| **reasoningEffort** | `high` | (törlődik) | 🔴 |
| **modelTemperature** | `0.2` | `0.2` | ✅ |
| **maxTokens** | `4000` | `4000` | ✅ |
| **contextWindow** | `1000000` | `1000000` | ✅ |

---

## 22. Review (Sonnet 4.5)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` | ⚠️ |
| **openAiApiKey** | `Review-Sonnet-4-5` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.5` | `0.5` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `200000` | `200000` | ✅ |

---

## 23. Search (Gemini Pro)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-3-pro-preview` | `gemini-3-pro-high` | ⚠️ |
| **openAiApiKey** | `Search-Gemini-Pro` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `true` | ✅ |
| **reasoningEffort** | `high` | `high` | ✅ |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `8000` | `8000` | ✅ |
| **contextWindow** | `1000000` | `1000000` | ✅ |

---

## 24. Commit (Gemini Flash)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-3-flash-preview` | `gemini-3-flash` | ⚠️ |
| **openAiApiKey** | `Commit-Gemini-Flash` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `false` | 🔴 |
| **reasoningEffort** | `high` | (törlődik) | 🔴 |
| **modelTemperature** | `0.2` | `0.2` | ✅ |
| **maxTokens** | `4000` | `4000` | ✅ |
| **contextWindow** | `1000000` | `1000000` | ✅ |

---

## 25. Reader (Gemini Flash)

| Paraméter | JELENLEGI | ÚJ | Változás |
|:----------|:----------|:---|:---------|
| **openAiModelId** | `gemini-3-flash-preview` | `gemini-3-flash` | ⚠️ |
| **openAiApiKey** | `Reader-Gemini-Flash` | `Narzie2012rohaN` | ⚠️ |
| **enableReasoningEffort** | `true` | `false` | 🔴 |
| **reasoningEffort** | `high` | (törlődik) | 🔴 |
| **modelTemperature** | `0.3` | `0.3` | ✅ |
| **maxTokens** | `4000` | `4000` | ✅ |
| **contextWindow** | `1000000` | `1000000` | ✅ |

---


## 📊 Változások Összesítése

### API Key Változások (25 mód - MIND):
**ELŐTTE:** Egyedi API key-ek minden módnál
**UTÁNA:** `Narzie2012rohaN` (egységes)

| Mód | Régi API Key | Új API Key |
|:----|:-------------|:-----------|
| 1. architect | `Architect-Opus-4-5` | `Narzie2012rohaN` |
| 2. planner | `Planner-Opus-4-5` | `Narzie2012rohaN` |
| 3. orchestrator | `Orchestrator-Sonnet-4-5` | `Narzie2012rohaN` |
| 4. code-new | `Code-New-Sonnet-4-5` | `Narzie2012rohaN` |
| 5. code-refactor | `Code-Refactor-Opus-4-5` | `Narzie2012rohaN` |
| 6. code-feature | `Code-Feature-Sonnet-4-5` | `Narzie2012rohaN` |
| 7. code-fix | `Code-Fix-Gemini-Pro` | `Narzie2012rohaN` |
| 8. code-optimize | `Code-Optimize-Opus-4-5` | `Narzie2012rohaN` |
| 9. code-style | `Code-Style-Gemini-Flash` | `Narzie2012rohaN` |
| 10. docs-api | `Docs-API-Gemini-Pro` | `Narzie2012rohaN` |
| 11. docs-guide | `Docs-Guide-Sonnet-4-5` | `Narzie2012rohaN` |
| 12. docs-arch | `Docs-Arch-Opus-4-5` | `Narzie2012rohaN` |
| 13. docs-comment | `Docs-Comment-Gemini-Flash` | `Narzie2012rohaN` |
| 14. test-unit | `Test-Unit-Gemini-Pro` | `Narzie2012rohaN` |
| 15. test-integration | `Test-Integration-Sonnet-4-5` | `Narzie2012rohaN` |
| 16. test-property | `Test-Property-Opus-4-5` | `Narzie2012rohaN` |
| 17. test-e2e | `Test-E2E-Sonnet-4-5` | `Narzie2012rohaN` |
| 18. debug-simple | `Debug-Simple-Gemini-Pro` | `Narzie2012rohaN` |
| 19. debug-complex | `Debug-Complex-Opus-4-5` | `Narzie2012rohaN` |
| 20. debug-performance | `Debug-Performance-Opus-4-5` | `Narzie2012rohaN` |
| 21. qa | `QA-Gemini-Flash` | `Narzie2012rohaN` |
| 22. review | `Review-Sonnet-4-5` | `Narzie2012rohaN` |
| 23. search | `Search-Gemini-Pro` | `Narzie2012rohaN` |
| 24. commit | `Commit-Gemini-Flash` | `Narzie2012rohaN` |
| 25. reader | `Reader-Gemini-Flash` | `Narzie2012rohaN` |

---

### Model ID Változások (11 mód):

#### Gemini Model Név Javítások (6 mód):
| Mód | Régi | Új |
|:----|:-----|:---|
| code-fix | `gemini-3-pro-preview` | `gemini-3-pro-high` |
| docs-api | `gemini-3-pro-preview` | `gemini-3-pro-high` |
| test-unit | `gemini-3-pro-preview` | `gemini-3-pro-high` |
| debug-simple | `gemini-3-pro-preview` | `gemini-3-pro-high` |
| search | `gemini-3-pro-preview` | `gemini-3-pro-high` |
| code-style | `gemini-3-flash-preview` | `gemini-3-flash` |
| docs-comment | `gemini-3-flash-preview` | `gemini-3-flash` |
| qa | `gemini-3-flash-preview` | `gemini-3-flash` |
| commit | `gemini-3-flash-preview` | `gemini-3-flash` |
| reader | `gemini-3-flash-preview` | `gemini-3-flash` |

#### Agentic Suffix Hozzáadása (2 mód):
| Mód | Régi | Új |
|:----|:-----|:---|
| planner | `claude-opus-4-6-thinking` | `kiro-claude-sonnet-4-5-agentic` |
| orchestrator | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5-agentic` |

#### DeepSeek Bevezetése (2 mód):
| Mód | Régi | Új |
|:----|:-----|:---|
| code-new | `gemini-claude-sonnet-4-5-thinking` | `kiro-deepseek-3-2` |
| code-feature | `gemini-claude-sonnet-4-5-thinking` | `kiro-deepseek-3-2` |

#### Kiro API Használat (4 mód):
| Mód | Régi | Új |
|:----|:-----|:---|
| docs-guide | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` |
| test-integration | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` |
| test-e2e | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` |
| review | `gemini-claude-sonnet-4-5-thinking` | `kiro-claude-sonnet-4-5` |

---

### Reasoning Változások (5 mód):

#### Reasoning Kikapcsolása (5 mód):
| Mód | Régi | Új | Indoklás |
|:----|:-----|:---|:---------|
| code-style | `true` (high) | `false` | Mechanikus formázás |
| docs-comment | `true` (high) | `false` | Inline kommentek |
| qa | `true` (high) | `false` | Linter futtatás |
| commit | `true` (high) | `false` | Commit üzenet |
| reader | `true` (high) | `false` | Fájl olvasás |

#### Reasoning Effort Változás (1 mód):
| Mód | Régi | Új | Indoklás |
|:----|:-----|:---|:---------|
| planner | `xhigh` | `high` | Sonnet: high elég |

---

## 🎯 Kritikus Változások Összefoglalása

### 🔴 Kritikus (Model ID + Reasoning):
1. **planner:** Opus → Sonnet Agentic (kvóta spórolás)
2. **orchestrator:** Sonnet Thinking → Sonnet Agentic (agentic reasoning)
3. **code-new:** Sonnet → DeepSeek (kód írás)
4. **code-feature:** Sonnet → DeepSeek (kód írás)
5. **code-style:** Reasoning kikapcsolva (mechanikus)
6. **docs-comment:** Reasoning kikapcsolva (mechanikus)
7. **qa:** Reasoning kikapcsolva (mechanikus)
8. **commit:** Reasoning kikapcsolva (mechanikus)
9. **reader:** Reasoning kikapcsolva (mechanikus)

### ⚠️ Közepes (Model ID vagy API Key):
1. **code-fix:** Model név javítás (gemini-3-pro-high)
2. **docs-api:** Model név javítás (gemini-3-pro-high)
3. **docs-guide:** Kiro API használat
4. **test-unit:** Model név javítás (gemini-3-pro-high)
5. **test-integration:** Kiro API használat
6. **test-e2e:** Kiro API használat
7. **debug-simple:** Model név javítás (gemini-3-pro-high)
8. **search:** Model név javítás (gemini-3-pro-high)
9. **review:** Kiro API használat

### ✅ Minimális (Csak API Key):
1. **architect:** API Key → `Narzie2012rohaN`
2. **code-refactor:** API Key → `Narzie2012rohaN`
3. **code-optimize:** API Key → `Narzie2012rohaN`
4. **docs-arch:** API Key → `Narzie2012rohaN`
5. **test-property:** API Key → `Narzie2012rohaN`
6. **debug-complex:** API Key → `Narzie2012rohaN`
7. **debug-performance:** API Key → `Narzie2012rohaN`

---

## 🚀 Script Futtatása

```bash
python update_roo_models.py
```

**Mit csinál:**
1. ✅ Backup készítés (automatikus)
2. ✅ Model ID frissítés (11 mód)
3. ✅ API Key frissítés (25 mód → `Narzie2012rohaN`)
4. ✅ Reasoning beállítások frissítése (6 mód)
5. ✅ JSON mentés (formázott)

---

**Státusz:** ✅ VÉGLEGES | **Verzió:** 5.0 FINAL | **Dátum:** 2026-02-12
