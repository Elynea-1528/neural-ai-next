#!/usr/bin/env python3
"""
Roo Code Model Beállítások Automatikus Frissítő Script

Ez a script frissíti a roo-code-settings.json fájlt az optimalizált
model allokációval (Hibrid: Sonnet + DeepSeek stratégia).

Használat:
    python update_roo_models.py

Figyelem:
    - Backup készül a jelenlegi beállításokról
    - Frissíti a model ID-kat, reasoning beállításokat ÉS az API key-t
    - Minden mód ugyanazt az API key-t használja: Narzie2012rohaN
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

# Egységes API key minden módhoz
UNIFIED_API_KEY = "Narzie2012rohaN"

# Új model allokáció (Hibrid: Sonnet + DeepSeek)
MODEL_UPDATES = {
    # TERVEZÉSI RÉTEG
    "architect": {
        "model": "claude-opus-4-6-thinking",
        "reasoning": True,
        "effort": "xhigh",
    },
    "planner": {
        "model": "kiro-claude-sonnet-4-5-agentic",
        "reasoning": True,
        "effort": "high",
    },
    
    # KOORDINÁCIÓ
    "orchestrator": {
        "model": "kiro-claude-sonnet-4-5-agentic",
        "reasoning": True,
        "effort": "high",
    },
    
    # IMPLEMENTÁCIÓS RÉTEG
    "code-new": {
        "model": "kiro-deepseek-3-2",  # Új modul: sima elég (egyszerű implementáció)
        "reasoning": True,
        "effort": "high",
    },
    "code-refactor": {
        "model": "claude-opus-4-6-thinking",  # Refaktorálás: Opus xhigh (komplex átgondolás)
        "reasoning": True,
        "effort": "xhigh",
    },
    "code-feature": {
        "model": "kiro-deepseek-3-2",  # Feature: sima elég (egyszerű hozzáadás, nem koordináció)
        "reasoning": True,
        "effort": "high",
    },
    "code-fix": {
        "model": "gemini-3-pro-high",
        "reasoning": True,
        "effort": "high",
    },
    "code-optimize": {
        "model": "claude-opus-4-6-thinking",
        "reasoning": True,
        "effort": "xhigh",
    },
    "code-style": {
        "model": "gemini-3-flash",
        "reasoning": False,
        "effort": None,
    },
    
    # DOKUMENTÁCIÓS RÉTEG
    "docs-api": {
        "model": "gemini-3-pro-high",
        "reasoning": True,
        "effort": "high",
    },
    "docs-guide": {
        "model": "kiro-claude-sonnet-4-5",
        "reasoning": True,
        "effort": "high",
    },
    "docs-arch": {
        "model": "claude-opus-4-6-thinking",
        "reasoning": True,
        "effort": "xhigh",
    },
    "docs-comment": {
        "model": "gemini-3-flash",
        "reasoning": False,
        "effort": None,
    },
    
    # TESZTELÉSI RÉTEG
    "test-unit": {
        "model": "gemini-3-pro-high",
        "reasoning": True,
        "effort": "high",
    },
    "test-integration": {
        "model": "kiro-claude-sonnet-4-5",
        "reasoning": True,
        "effort": "high",
    },
    "test-property": {
        "model": "claude-opus-4-6-thinking",
        "reasoning": True,
        "effort": "xhigh",
    },
    "test-e2e": {
        "model": "kiro-claude-sonnet-4-5",
        "reasoning": True,
        "effort": "high",
    },
    
    # KARBANTARTÁSI RÉTEG
    "debug-simple": {
        "model": "gemini-3-pro-high",
        "reasoning": True,
        "effort": "high",
    },
    "debug-complex": {
        "model": "claude-opus-4-6-thinking",
        "reasoning": True,
        "effort": "xhigh",
    },
    "debug-performance": {
        "model": "claude-opus-4-6-thinking",
        "reasoning": True,
        "effort": "xhigh",
    },
    
    # TÁMOGATÓ RÉTEG
    "qa": {
        "model": "gemini-3-flash",
        "reasoning": False,
        "effort": None,
    },
    "review": {
        "model": "kiro-claude-sonnet-4-5",
        "reasoning": True,
        "effort": "high",
    },
    "search": {
        "model": "gemini-3-pro-high",
        "reasoning": True,
        "effort": "high",
    },
    "commit": {
        "model": "gemini-3-flash",
        "reasoning": False,
        "effort": None,
    },
    "reader": {
        "model": "gemini-3-flash",
        "reasoning": False,
        "effort": None,
    },
}


def backup_settings(settings_path: Path) -> Path:
    """Backup készítése a jelenlegi beállításokról."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = settings_path.parent / f"roo-code-settings.backup.{timestamp}.json"
    shutil.copy2(settings_path, backup_path)
    print(f"✅ Backup készült: {backup_path}")
    return backup_path


def update_settings(settings_path: Path) -> None:
    """Frissíti a Roo Code beállításokat."""
    # Beállítások betöltése
    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)
    
    # API configs frissítése
    api_configs = settings["providerProfiles"]["apiConfigs"]
    
    # Profil név mapping (mode → profil név)
    MODE_TO_PROFILE = {
        "architect": "Architect (Opus 4.6)",
        "planner": "Planner (Sonnet 4.5)",
        "orchestrator": "Orchestrator (Sonnet 4.5)",
        "code-new": "Code-New (Deepseek 3.2)",
        "code-refactor": "Code-Refactor (Opus 4.6)",
        "code-feature": "Code-Feature (Deepseek 3.2)",
        "code-fix": "Code-Fix (Gemini Pro)",
        "code-optimize": "Code-Optimize (Opus 4.6)",
        "code-style": "Code-Style (Gemini Flash)",
        "docs-api": "Docs-API (Gemini Pro)",
        "docs-guide": "Docs-Guide (Sonnet 4.5)",
        "docs-arch": "Docs-Arch (Opus 4.6)",
        "docs-comment": "Docs-Comment (Gemini Flash)",
        "test-unit": "Test-Unit (Gemini Pro)",
        "test-integration": "Test-Integration (Sonnet 4.5)",
        "test-property": "Test-Property (Opus 4.6)",
        "test-e2e": "Test-E2E (Sonnet 4.5)",
        "debug-simple": "Debug-Simple (Gemini Pro)",
        "debug-complex": "Debug-Complex (Opus 4.6)",
        "debug-performance": "Debug-Performance (Opus 4.6)",
        "qa": "QA (Gemini Flash)",
        "review": "Review (Sonnet 4.5)",
        "search": "Search (Gemini Pro)",
        "commit": "Commit (Gemini Flash)",
        "reader": "Reader (Gemini Flash)",
    }
    
    updated_count = 0
    for mode, config in MODEL_UPDATES.items():
        # Profil név keresése
        profile_name = MODE_TO_PROFILE.get(mode)
        
        if not profile_name or profile_name not in api_configs:
            print(f"⚠️  Profil nem található: {mode} ({profile_name})")
            continue
        
        # Model ID frissítése
        old_model = api_configs[profile_name].get("openAiModelId", "N/A")
        api_configs[profile_name]["openAiModelId"] = config["model"]
        
        # API Key frissítése (EGYSÉGES)
        api_configs[profile_name]["openAiApiKey"] = UNIFIED_API_KEY
        
        # Reasoning beállítások frissítése
        api_configs[profile_name]["enableReasoningEffort"] = config["reasoning"]
        
        if config["reasoning"] and config["effort"]:
            api_configs[profile_name]["openAiCustomModelInfo"]["reasoningEffort"] = config["effort"]
        elif not config["reasoning"]:
            # Reasoning kikapcsolva: töröljük a reasoningEffort-ot
            if "reasoningEffort" in api_configs[profile_name].get("openAiCustomModelInfo", {}):
                del api_configs[profile_name]["openAiCustomModelInfo"]["reasoningEffort"]
        
        print(f"✅ {mode:20s} | {old_model:35s} → {config['model']:35s} | Reasoning: {config['reasoning']}")
        updated_count += 1
    
    # Frissített beállítások mentése
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Összesen {updated_count} mód frissítve!")
    print(f"✅ API Key frissítve: {UNIFIED_API_KEY}")
    print(f"✅ Beállítások mentve: {settings_path}")


def main():
    """Fő függvény."""
    settings_path = Path("roo-code-settings.json")
    
    if not settings_path.exists():
        print(f"❌ Hiba: {settings_path} nem található!")
        return
    
    print("🔄 Roo Code Model Beállítások Frissítése")
    print("=" * 80)
    print()
    
    # Backup készítése
    backup_path = backup_settings(settings_path)
    print()
    
    # Beállítások frissítése
    print("🔄 Model allokáció frissítése...")
    print()
    update_settings(settings_path)
    print()
    
    print("=" * 80)
    print("✅ Frissítés sikeres!")
    print()
    print("📝 Következő lépések:")
    print("   1. Nyisd meg a Roo Code UI-t")
    print("   2. Ellenőrizd a frissített beállításokat")
    print("   3. Teszteld az új model allokációt")
    print()
    print(f"💾 Backup: {backup_path}")


if __name__ == "__main__":
    main()
