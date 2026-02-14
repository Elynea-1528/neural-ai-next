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
    
    updated_count = 0
    for mode, config in MODEL_UPDATES.items():
        # Profil név keresése (pl. "Architect (Opus 4.5)")
        profile_name = None
        for name in api_configs.keys():
            if mode.replace("-", " ").title() in name or mode.title() in name:
                profile_name = name
                break
        
        if not profile_name:
            print(f"⚠️  Profil nem található: {mode}")
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
