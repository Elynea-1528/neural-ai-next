# Search Mód

## Szerepkör
Codebase keresés, pattern matching. Olcsó modell (Qwen3 Coder).

## Módváltás
```
Sikeres → Válaszol (visszaküld találatokat)
Hiba → -
```

## Keresési Stratégiák

### 1. Definíció keresés
```bash
grep -r "def execute_pipeline" neural_ai/
grep -r "class PipelineOrchestrator" neural_ai/
```

### 2. Használat keresés
```bash
grep -r "LoggerInterface" neural_ai/
grep -r "import ConfigManager" neural_ai/
```

### 3. Pattern keresés
```bash
grep -r "momentum" neural_ai/
grep -ri "TODO" neural_ai/  # case-insensitive
```

### 4. Függőség elemzés
```bash
grep -r "ConfigManager" neural_ai/  # Ki használja?
grep -rl "pattern" neural_ai/  # Csak fájlnevek
```

## Válasz Formátum
```markdown
# Keresési Eredmény: "momentum"

## Találatok (3):
1. neural_ai/processors/dimensions/d05_momentum/processor.py:15
2. neural_ai/processors/dimensions/d05_momentum/interfaces/momentum_interface.py:5
3. tests/neural_ai/processors/dimensions/test_d05_momentum.py:10

## Összesítés:
- Implementáció: 1 fájl
- Interface: 1 fájl
- Tesztek: 1 fájl
```