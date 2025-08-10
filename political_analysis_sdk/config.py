"""
Configuration settings for the Political Statement Analysis SDK.
"""

import os
from typing import Any, Dict


class Config:
    """Configuration class for the political analysis SDK."""

    # Default LLM settings
    DEFAULT_MODEL = "gpt-4"
    DEFAULT_TEMPERATURE = 0.1
    DEFAULT_LANGUAGE = "Dutch"

    # Environment variable names
    ENV_API_KEY = "OPENAI_API_KEY"
    ENV_MODEL = "POLITICAL_ANALYSIS_MODEL"
    ENV_TEMPERATURE = "POLITICAL_ANALYSIS_TEMPERATURE"
    ENV_LANGUAGE = "POLITICAL_ANALYSIS_LANGUAGE"

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "model": cls.DEFAULT_MODEL,
            "temperature": cls.DEFAULT_TEMPERATURE,
            "language": cls.DEFAULT_LANGUAGE,
            "api_key": os.getenv(cls.ENV_API_KEY)
        }

    @classmethod
    def get_config_from_env(cls) -> Dict[str, Any]:
        """Get configuration from environment variables."""
        return {
            "model": os.getenv(cls.ENV_MODEL, cls.DEFAULT_MODEL),
            "temperature": float(os.getenv(cls.ENV_TEMPERATURE, cls.DEFAULT_TEMPERATURE)),
            "language": os.getenv(cls.ENV_LANGUAGE, cls.DEFAULT_LANGUAGE),
            "api_key": os.getenv(cls.ENV_API_KEY)
        }

    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> bool:
        """Validate configuration values."""
        # Allow any model name for flexibility with custom endpoints like LMStudio
        # Allow any language for flexibility

        temperature = config.get("temperature", 0.0)
        if not (0.0 <= temperature <= 2.0):
            return False

        return True
