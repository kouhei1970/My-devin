"""
Core Configuration System
Handles loading and managing configuration from YAML files and environment variables
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    """LLM Provider Settings"""
    provider: str = Field(default="lm-studio", description="LLM provider to use")
    default_model: str = Field(default="qwen2.5-coder-32b-instruct")

    # LM Studio settings
    lm_studio_base_url: str = Field(default="http://localhost:1234/v1")
    lm_studio_api_key: str = Field(default="lm-studio")
    lm_studio_timeout: int = Field(default=300)

    # Ollama settings
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_timeout: int = Field(default=300)

    model_config = SettingsConfigDict(
        env_prefix="",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


class APISettings(BaseSettings):
    """API Server Settings"""
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    workers: int = Field(default=4)

    model_config = SettingsConfigDict(env_prefix="API_")


class EmbeddedSettings(BaseSettings):
    """Embedded Development Settings"""
    enabled: bool = Field(default=True, alias="EMBEDDED_MODE")
    default_rtos: str = Field(default="freertos")
    target_mcu: str = Field(default="stm32f4", alias="TARGET_MCU")
    cpp_standard: str = Field(default="c++17", alias="CPP_STANDARD")
    optimization: str = Field(default="O2", alias="OPTIMIZATION")

    model_config = SettingsConfigDict(env_prefix="")


class Config:
    """
    Main Configuration Manager
    Loads configuration from:
    1. config/default.yaml
    2. Environment variables (.env)
    3. Runtime overrides
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration

        Args:
            config_path: Path to YAML config file (default: config/default.yaml)
        """
        self.config_path = config_path or Path("config/default.yaml")
        self.config_data: Dict[str, Any] = {}

        # Load configuration
        self._load_yaml()

        # Initialize settings with Pydantic
        self.llm = LLMSettings()
        self.api = APISettings()
        self.embedded = EmbeddedSettings()

    def _load_yaml(self) -> None:
        """Load configuration from YAML file"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = yaml.safe_load(f) or {}
        else:
            print(f"Warning: Config file not found: {self.config_path}")
            self.config_data = {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key (supports dot notation)

        Args:
            key: Configuration key (e.g., "llm.provider")
            default: Default value if key not found

        Returns:
            Configuration value

        Example:
            >>> config.get("llm.provider")
            'lm-studio'
            >>> config.get("embedded_development.default_rtos")
            'freertos'
        """
        keys = key.split('.')
        value = self.config_data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value if value is not None else default

    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration as dictionary"""
        return {
            "provider": self.llm.provider,
            "default_model": self.llm.default_model,
            "lm_studio": {
                "base_url": self.llm.lm_studio_base_url,
                "api_key": self.llm.lm_studio_api_key,
                "timeout": self.llm.lm_studio_timeout,
            },
            "ollama": {
                "base_url": self.llm.ollama_base_url,
                "timeout": self.llm.ollama_timeout,
            }
        }

    def get_embedded_config(self) -> Dict[str, Any]:
        """Get embedded development configuration"""
        embedded_config = self.get("embedded_development", {})

        return {
            "enabled": self.embedded.enabled,
            "default_rtos": embedded_config.get("default_rtos", self.embedded.default_rtos),
            "target_mcu": self.embedded.target_mcu,
            "cpp_standard": self.embedded.cpp_standard,
            "optimization": self.embedded.optimization,
            "rtos": embedded_config.get("rtos", {}),
            "targets": embedded_config.get("targets", {}),
            "peripherals": embedded_config.get("peripherals", {}),
            "memory": embedded_config.get("memory", {}),
            "realtime": embedded_config.get("realtime", {}),
        }

    def get_code_generation_config(self) -> Dict[str, Any]:
        """Get code generation configuration"""
        return self.get("code_generation", {})

    def get_model_params(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get model-specific parameters

        Args:
            model_name: Model name (uses default if None)

        Returns:
            Model parameters (temperature, max_tokens, etc.)
        """
        model = model_name or self.llm.default_model
        models_config = self.get("llm.models", {})

        # Try exact match first
        if model in models_config:
            return models_config[model]

        # Try normalized name (replace : with -)
        normalized = model.replace(':', '-')
        if normalized in models_config:
            return models_config[normalized]

        # Return defaults
        return {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 4096,
            "context_window": 32768,
        }

    def is_embedded_mode(self) -> bool:
        """Check if embedded development mode is enabled"""
        return self.embedded.enabled

    def get_primary_language(self) -> str:
        """Get primary programming language"""
        return self.get("code_generation.primary_language", "cpp")

    def get_supported_languages(self) -> list[str]:
        """Get list of supported programming languages"""
        return self.get("code_generation.languages", [
            "cpp", "c", "python", "typescript", "javascript",
            "go", "rust", "java"
        ])

    def get_cpp_settings(self) -> Dict[str, Any]:
        """Get C++ specific settings"""
        return self.get("code_generation.cpp", {
            "standard": "c++17",
            "exceptions": False,
            "rtti": False,
            "optimization": "O2",
            "warnings": "all",
        })

    def reload(self) -> None:
        """Reload configuration from file"""
        self._load_yaml()
        self.llm = LLMSettings()
        self.api = APISettings()
        self.embedded = EmbeddedSettings()

    def __repr__(self) -> str:
        return f"Config(provider={self.llm.provider}, embedded={self.embedded.enabled})"


# Global configuration instance
_config: Optional[Config] = None


def get_config(config_path: Optional[Path] = None) -> Config:
    """
    Get global configuration instance (singleton pattern)

    Args:
        config_path: Path to config file (only used on first call)

    Returns:
        Config instance
    """
    global _config

    if _config is None:
        _config = Config(config_path)

    return _config


def reload_config() -> Config:
    """Reload configuration from file"""
    global _config

    if _config is not None:
        _config.reload()
    else:
        _config = Config()

    return _config


# Example usage
if __name__ == "__main__":
    # Get configuration
    config = get_config()

    print("=== My-devin Configuration ===")
    print(f"LLM Provider: {config.llm.provider}")
    print(f"Default Model: {config.llm.default_model}")
    print(f"LM Studio URL: {config.llm.lm_studio_base_url}")
    print(f"Embedded Mode: {config.is_embedded_mode()}")
    print(f"Target MCU: {config.embedded.target_mcu}")
    print(f"Default RTOS: {config.embedded.default_rtos}")
    print(f"Primary Language: {config.get_primary_language()}")
    print(f"C++ Standard: {config.get_cpp_settings()['standard']}")

    print("\n=== Model Parameters ===")
    params = config.get_model_params()
    for key, value in params.items():
        print(f"{key}: {value}")

    print("\n=== Embedded Config ===")
    embedded = config.get_embedded_config()
    print(f"Default RTOS: {embedded['default_rtos']}")
    print(f"Target MCU: {embedded['target_mcu']}")
    print(f"C++ Standard: {embedded['cpp_standard']}")
