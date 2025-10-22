"""
Unit tests for configuration system
"""

import pytest
from pathlib import Path
import tempfile
import yaml

from src.core.config import Config, get_config, reload_config


class TestConfig:
    """Test configuration system"""

    def test_default_config_loading(self):
        """Test loading default configuration"""
        config = Config()

        assert config.llm.provider in ["lm-studio", "ollama", "mlx"]
        assert config.llm.default_model is not None
        assert config.api.port == 8000

    def test_get_method_with_dot_notation(self):
        """Test get method with dot notation"""
        config = Config()

        # Test getting nested values
        provider = config.get("llm.provider")
        assert provider is not None

        # Test default value
        nonexistent = config.get("nonexistent.key", "default")
        assert nonexistent == "default"

    def test_get_llm_config(self):
        """Test getting LLM configuration"""
        config = Config()

        llm_config = config.get_llm_config()

        assert "provider" in llm_config
        assert "default_model" in llm_config
        assert "lm_studio" in llm_config
        assert "base_url" in llm_config["lm_studio"]

    def test_get_embedded_config(self):
        """Test getting embedded development configuration"""
        config = Config()

        embedded_config = config.get_embedded_config()

        assert "default_rtos" in embedded_config
        assert "target_mcu" in embedded_config
        assert "cpp_standard" in embedded_config

    def test_get_model_params(self):
        """Test getting model parameters"""
        config = Config()

        params = config.get_model_params()

        assert "temperature" in params
        assert "max_tokens" in params
        assert params["temperature"] > 0
        assert params["max_tokens"] > 0

    def test_is_embedded_mode(self):
        """Test embedded mode detection"""
        config = Config()

        # Should be bool
        assert isinstance(config.is_embedded_mode(), bool)

    def test_get_primary_language(self):
        """Test getting primary language"""
        config = Config()

        lang = config.get_primary_language()

        assert isinstance(lang, str)
        assert len(lang) > 0

    def test_get_supported_languages(self):
        """Test getting supported languages"""
        config = Config()

        langs = config.get_supported_languages()

        assert isinstance(langs, list)
        assert len(langs) > 0
        assert "cpp" in langs or "c++" in langs

    def test_get_cpp_settings(self):
        """Test getting C++ settings"""
        config = Config()

        cpp_settings = config.get_cpp_settings()

        assert "standard" in cpp_settings
        assert "exceptions" in cpp_settings
        assert "rtti" in cpp_settings

    def test_custom_config_file(self):
        """Test loading custom config file"""
        # Create temporary config
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                "llm": {
                    "provider": "test-provider",
                    "default_model": "test-model"
                }
            }
            yaml.dump(config_data, f)
            temp_path = Path(f.name)

        try:
            config = Config(config_path=temp_path)

            assert config.get("llm.provider") == "test-provider"
            assert config.get("llm.default_model") == "test-model"

        finally:
            temp_path.unlink()

    def test_singleton_pattern(self):
        """Test global config singleton"""
        config1 = get_config()
        config2 = get_config()

        assert config1 is config2

    def test_reload_config(self):
        """Test reloading configuration"""
        config = reload_config()

        assert config is not None
        assert config.llm.provider is not None


class TestLLMSettings:
    """Test LLM settings"""

    def test_lm_studio_defaults(self):
        """Test LM Studio default settings"""
        config = Config()

        assert config.llm.lm_studio_base_url == "http://localhost:1234/v1"
        assert config.llm.lm_studio_api_key == "lm-studio"
        assert config.llm.lm_studio_timeout == 300

    def test_ollama_defaults(self):
        """Test Ollama default settings"""
        config = Config()

        assert config.llm.ollama_base_url == "http://localhost:11434"
        assert config.llm.ollama_timeout == 300


class TestEmbeddedSettings:
    """Test embedded development settings"""

    def test_default_rtos(self):
        """Test default RTOS setting"""
        config = Config()

        assert config.embedded.default_rtos in [
            "freertos", "zephyr", "mbed_os", "riot"
        ]

    def test_target_mcu(self):
        """Test target MCU setting"""
        config = Config()

        target = config.embedded.target_mcu

        assert isinstance(target, str)
        assert len(target) > 0

    def test_cpp_standard(self):
        """Test C++ standard setting"""
        config = Config()

        standard = config.embedded.cpp_standard

        assert standard in ["c++11", "c++14", "c++17", "c++20"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
