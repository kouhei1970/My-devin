"""
LLM Manager
Manages multiple LLM providers and provides unified interface
"""

from typing import AsyncIterator, Dict, Any, Optional, Type
from ..core.config import get_config
from .base import BaseLLMProvider
from .lm_studio import LMStudioProvider


class LLMManager:
    """
    LLM Provider Manager
    Handles multiple LLM backends with unified interface
    """

    # Registry of available providers
    _providers: Dict[str, Type[BaseLLMProvider]] = {
        "lm-studio": LMStudioProvider,
        "lmstudio": LMStudioProvider,
    }

    def __init__(
        self,
        provider_name: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize LLM Manager

        Args:
            provider_name: Provider to use (default: from config)
            model_name: Model to use (default: from config)
            **kwargs: Additional provider-specific arguments
        """
        self.config = get_config()

        # Determine provider and model
        self.provider_name = provider_name or self.config.llm.provider
        self.model_name = model_name or self.config.llm.default_model

        # Create provider instance
        self.provider = self._create_provider(**kwargs)

    def _create_provider(self, **kwargs) -> BaseLLMProvider:
        """
        Create LLM provider instance

        Args:
            **kwargs: Provider-specific arguments

        Returns:
            LLM provider instance

        Raises:
            ValueError: If provider not found
        """
        provider_name_normalized = self.provider_name.lower().replace('_', '-')

        if provider_name_normalized not in self._providers:
            available = ", ".join(self._providers.keys())
            raise ValueError(
                f"Unknown LLM provider: {self.provider_name}. "
                f"Available providers: {available}"
            )

        provider_class = self._providers[provider_name_normalized]

        # Get provider-specific configuration
        if provider_name_normalized in ["lm-studio", "lmstudio"]:
            provider_kwargs = {
                "base_url": kwargs.get(
                    "base_url",
                    self.config.llm.lm_studio_base_url
                ),
                "api_key": kwargs.get(
                    "api_key",
                    self.config.llm.lm_studio_api_key
                ),
                "model_name": self.model_name,
                "timeout": kwargs.get(
                    "timeout",
                    self.config.llm.lm_studio_timeout
                ),
            }
        else:
            provider_kwargs = kwargs

        return provider_class(**provider_kwargs)

    async def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate text (non-streaming)

        Args:
            prompt: Input prompt
            temperature: Temperature parameter (uses model default if None)
            max_tokens: Maximum tokens (uses model default if None)
            **kwargs: Additional parameters

        Returns:
            Generated text
        """
        # Get model defaults
        model_params = self.config.get_model_params(self.model_name)

        # Use defaults if not specified
        temperature = temperature if temperature is not None else model_params.get("temperature", 0.7)
        max_tokens = max_tokens if max_tokens is not None else model_params.get("max_tokens", 2048)

        return await self.provider.generate(
            prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

    async def stream_generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        Generate text (streaming)

        Args:
            prompt: Input prompt
            temperature: Temperature parameter
            max_tokens: Maximum tokens
            **kwargs: Additional parameters

        Yields:
            Text chunks
        """
        # Get model defaults
        model_params = self.config.get_model_params(self.model_name)

        temperature = temperature if temperature is not None else model_params.get("temperature", 0.7)
        max_tokens = max_tokens if max_tokens is not None else model_params.get("max_tokens", 2048)

        async for chunk in self.provider.stream_generate(
            prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        ):
            yield chunk

    async def generate_code(
        self,
        description: str,
        language: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate code

        Args:
            description: Code description/requirements
            language: Programming language (uses primary if None)
            **kwargs: Additional parameters

        Returns:
            Generated code
        """
        # Determine language
        if language is None:
            language = self.config.get_primary_language()

        # Check if provider has generate_code method
        if hasattr(self.provider, 'generate_code'):
            return await self.provider.generate_code(
                description=description,
                language=language,
                **kwargs
            )

        # Fallback to generic generate
        prompt = self._build_code_prompt(description, language, **kwargs)
        return await self.generate(prompt, **kwargs)

    def _build_code_prompt(
        self,
        description: str,
        language: str,
        context: Optional[str] = None,
        **kwargs
    ) -> str:
        """Build code generation prompt"""
        embedded_mode = kwargs.get('embedded', self.config.is_embedded_mode())

        if embedded_mode and language.lower() in ['cpp', 'c', 'c++']:
            # Use embedded C++ system prompt
            system_context = self._get_embedded_cpp_context()
        else:
            system_context = f"You are an expert {language} programmer."

        prompt = f"""{system_context}

Generate {language} code for the following task:

Task: {description}
"""

        if context:
            prompt += f"\nContext:\n{context}\n"

        prompt += f"\nGenerate only the {language} code with minimal explanation."

        return prompt

    def _get_embedded_cpp_context(self) -> str:
        """Get embedded C++ system prompt context"""
        embedded_config = self.config.get_embedded_config()
        cpp_config = self.config.get_cpp_settings()

        return f"""You are an expert embedded systems engineer specializing in C++ development.

Target Configuration:
- RTOS: {embedded_config['default_rtos']}
- MCU: {embedded_config['target_mcu']}
- C++ Standard: {cpp_config['standard']}
- Exceptions: {'enabled' if cpp_config['exceptions'] else 'disabled'}
- RTTI: {'enabled' if cpp_config['rtti'] else 'disabled'}

Follow these guidelines:
- Use static memory allocation
- No exceptions (use error codes)
- No RTTI
- MISRA C++ compliant when possible
- Optimize for memory and performance
- Include necessary headers
"""

    async def get_model_info(self) -> Dict[str, Any]:
        """Get current model information"""
        return await self.provider.get_model_info()

    async def health_check(self) -> bool:
        """Check if LLM provider is healthy"""
        return await self.provider.health_check()

    def switch_provider(
        self,
        provider_name: str,
        model_name: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Switch to a different LLM provider

        Args:
            provider_name: New provider name
            model_name: New model name (optional)
            **kwargs: Provider-specific arguments
        """
        self.provider_name = provider_name
        if model_name:
            self.model_name = model_name

        self.provider = self._create_provider(**kwargs)

    def switch_model(self, model_name: str) -> None:
        """
        Switch to a different model (same provider)

        Args:
            model_name: New model name
        """
        self.model_name = model_name

        # Recreate provider with new model
        self.provider = self._create_provider()

    @classmethod
    def register_provider(
        cls,
        name: str,
        provider_class: Type[BaseLLMProvider]
    ) -> None:
        """
        Register a new LLM provider

        Args:
            name: Provider name
            provider_class: Provider class (must inherit from BaseLLMProvider)
        """
        if not issubclass(provider_class, BaseLLMProvider):
            raise TypeError(
                f"{provider_class} must inherit from BaseLLMProvider"
            )

        cls._providers[name.lower()] = provider_class

    @classmethod
    def list_providers(cls) -> list[str]:
        """Get list of available provider names"""
        return list(cls._providers.keys())

    def __repr__(self) -> str:
        return f"LLMManager(provider={self.provider_name}, model={self.model_name})"


# Example usage
async def example_usage():
    """Example usage of LLM Manager"""

    # Create manager (uses config defaults)
    manager = LLMManager()

    print(f"Using: {manager}")

    # Health check
    is_healthy = await manager.health_check()
    print(f"LLM Server Health: {'✓' if is_healthy else '✗'}")

    if not is_healthy:
        print("Error: LLM server is not available")
        return

    # Get model info
    info = await manager.get_model_info()
    print(f"\nModel Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")

    # Generate code (embedded C++)
    print("\n=== Generating FreeRTOS Task ===")
    code = await manager.generate_code(
        description="Create a FreeRTOS task that blinks an LED every 1 second on GPIO pin PA5",
        language="cpp",
        embedded=True
    )
    print(code)

    # Streaming generation
    print("\n=== Streaming Generation ===")
    print("Explain FreeRTOS queues: ", end="", flush=True)
    async for chunk in manager.stream_generate("Explain FreeRTOS queues in 2 sentences"):
        print(chunk, end="", flush=True)
    print()

    # Switch model
    print("\n=== Switching Model ===")
    manager.switch_model("qwen2.5-coder-14b-instruct")
    print(f"Now using: {manager.model_name}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
