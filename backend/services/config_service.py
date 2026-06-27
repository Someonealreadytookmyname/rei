import json
import os
from pathlib import Path

# Config file lives at project root
CONFIG_PATH = Path(__file__).parent.parent.parent / "config.json"

DEFAULT_CONFIG = {
    "llm_mode": "local",         # "local" or "api"
    "api_provider": "openai",    # "openai", "gemini", "anthropic", "huggingface"
    "openai_api_key": "",
    "gemini_api_key": "",
    "anthropic_api_key": "",
    "huggingface_api_key": "",
    "openai_model": "gpt-4o-mini",
    "gemini_model": "gemini-2.0-flash",
    "anthropic_model": "claude-sonnet-4-20250514",
    "huggingface_model": "meta-llama/Meta-Llama-3-8B-Instruct",
    "ollama_model": "qwen3:4b",
    "embedding_mode": "local",   # "local" or "api"
    "embedding_api_key": "",
}


def load_config() -> dict:
    """Load config from disk, creating defaults if missing."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                saved = json.load(f)
            # Merge with defaults so new keys are always present
            merged = {**DEFAULT_CONFIG, **saved}
            return merged
        except (json.JSONDecodeError, IOError):
            pass
    return dict(DEFAULT_CONFIG)


def save_config(config: dict) -> None:
    """Persist config to disk."""
    # Only save known keys
    to_save = {k: config.get(k, v) for k, v in DEFAULT_CONFIG.items()}
    with open(CONFIG_PATH, "w") as f:
        json.dump(to_save, f, indent=2)


def update_config(updates: dict) -> dict:
    """Merge updates into existing config and save."""
    config = load_config()
    config.update({k: v for k, v in updates.items() if k in DEFAULT_CONFIG})
    save_config(config)
    return config
