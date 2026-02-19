# Módváltási Mátrix

## 📊 Teljes Módváltási Táblázat

| Mód | Sikeres → | Hiba → | Olvasás → | Speciális → |
|:----|:----------|:-------|:----------|:------------|
| **Architect** | Planner, Orchestrator | - | Reader, Search | - |
| **Planner** | Architect | - | Reader, Search | - |
| **Orchestrator** | Code-*, Debug-*, Test-*, Docs-*, QA, Review, Commit | - | Reader, Search | - |
| **Code-New** | Test-Unit | Debug-Simple, Debug-Complex | Reader, Search | Docs-API |
| **Code-Feature** | Test-Unit | Debug-Simple, Debug-Complex | Reader, Search | Docs-API |
| **Code-Refactor** | Test-Integration | Debug-Complex | Reader, Search | Docs-Arch |
| **Code-Fix** | Test-Unit | Debug-Complex | Reader, Search | - |
| **Code-Optimize** | Test-E2E | Debug-Performance | Reader, Search | Docs-Comment |
| **Code-Style** | QA | - | Reader, Search | - |
| **Debug-Simple** | Test-Unit | Debug-Complex | Reader, Search | Code-Fix |
| **Debug-Complex** | Test-Integration | - | Reader, Search | Code-Refactor |
| **Debug-Performance** | Test-E2E | - | Reader, Search | Code-Optimize |
| **Test-Unit** | QA | Debug-Simple | Reader, Search | Code-Fix |
| **Test-Integration** | QA | Debug-Complex | Reader, Search | Code-Refactor |
| **Test-Property** | QA | Debug-Complex | Reader, Search | Docs-API |
| **Test-E2E** | QA | Debug-Performance, Debug-Complex | Reader, Search | Docs-Guide |
| **Docs-API** | Review | - | Reader, Search | Code-New, Code-Feature |
| **Docs-Guide** | Review | - | Reader, Search | Test-E2E |
| **Docs-Arch** | Review | - | Reader, Search | Code-Refactor |
| **Docs-Comment** | Review | - | Reader, Search | Code-* |
| **QA** | Commit | Debug-Simple, Debug-Complex, Code-Style | Reader, Search | - |
| **Review** | Commit | Code-Refactor | Reader, Search | Docs-* |
| **Commit** | KÉSZ | - | Reader, Search | - |
| **Reader** | Válaszol | - | - | - |
| **Search** | Válaszol | - | - | - |

**Alapszabály:** Minden mód (kivéve Reader/Search) SOHA nem olvas közvetlenül → Mindig Reader/Search  
**Token Economy:** 90% megtakarítás (15k drágán → 1.5k drágán + 15k olcsón)

## 🔄 Mikor melyik módra válts?

### Olvasási Igény
```
"Hol van X?" / "Milyen modulok vannak?" → search
"Mi az X struktúrája?" / "Add meg X kódját" → reader
```

### Tervezési Igény
```
Nagy projekt (>1 hónap) → planner
Közepes/Kis projekt → orchestrator
```

### Implementációs Igény
```
Új modul (0→1) → code-new
Új funkció → code-feature
Refaktorálás → code-refactor
Optimalizálás → code-optimize
Formatting → code-style
```

### Hibakezelési Igény
```
Egyszerű (linter, import) → debug-simple
Komplex (logic, race) → debug-complex
Performance → debug-performance
```

### Tesztelési Igény
```
Unit → test-unit
Integration → test-integration
Property → test-property
E2E → test-e2e
```

### Dokumentációs Igény
```
API (docstring) → docs-api
Guide (README) → docs-guide
Arch (ADR) → docs-arch
Comment (inline) → docs-comment
```

### Minőségbiztosítási Igény
```
Linter/Type check → qa
Code review → review
Commit → commit
```

## 🎯 Delegálási Sablon

```
switch_mode: [target]
Üzenet: "[Mód]! [Parancs] [Részletek]"
```

## 💰 Token Economy

**Régi:** 15,000 token (drágán)  
**Új:** 1,500 token (drágán) + 15,000 token (olcsón Reader/Search)  
**Megtakarítás: 90%** ✅

## 🚨 Kritikus Szabályok

1. **Architect/Planner/Orchestrator SOHA NEM OLVAS fájlokat** (groups: [] vagy [read, command])
2. **Code-*/Debug-* MINDIG Reader/Search-t használ** (groups: [read, edit, command])
3. **Reader/Search SOHA NEM DELEGÁL** (csak válaszol)
4. **QA CSAK egyszerű hibákat javít** (komplex → Debug-*)
5. **Commit MINDIG utolsó lépés** (QA után)
