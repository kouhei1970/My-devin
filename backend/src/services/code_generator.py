"""
Code Generation Service
Handles code generation for various languages with embedded systems support
"""

import re
from typing import Optional, Dict, Any
from pathlib import Path

from ..llm.manager import LLMManager
from ..core.config import get_config


class CodeGenerator:
    """
    Code Generation Service
    Supports multiple languages with special focus on embedded C++
    """

    def __init__(self, llm_manager: Optional[LLMManager] = None):
        """
        Initialize Code Generator

        Args:
            llm_manager: LLM Manager instance (creates new if None)
        """
        self.llm = llm_manager or LLMManager()
        self.config = get_config()

    async def generate(
        self,
        description: str,
        language: Optional[str] = None,
        context: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate code from description

        Args:
            description: What the code should do
            language: Programming language (uses primary if None)
            context: Additional context
            **kwargs: Additional parameters (rtos, target, embedded, etc.)

        Returns:
            Generated code

        Example:
            >>> generator = CodeGenerator()
            >>> code = await generator.generate(
            ...     "LED blink task",
            ...     language="cpp",
            ...     rtos="freertos",
            ...     target="stm32f4"
            ... )
        """
        # Determine language
        if language is None:
            language = self.config.get_primary_language()

        language = language.lower()

        # Check if embedded mode for C/C++
        is_embedded = kwargs.get('embedded', self.config.is_embedded_mode())
        if language in ['cpp', 'c', 'c++'] and is_embedded:
            return await self._generate_embedded_cpp(
                description, context, **kwargs
            )

        # General code generation
        return await self._generate_general(
            description, language, context, **kwargs
        )

    async def _generate_embedded_cpp(
        self,
        description: str,
        context: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate embedded C++ code

        Args:
            description: Code description
            context: Additional context
            **kwargs: rtos, target, peripheral, etc.

        Returns:
            Generated C++ code
        """
        # Get embedded configuration
        embedded_config = self.config.get_embedded_config()
        cpp_config = self.config.get_cpp_settings()

        # Extract parameters
        rtos = kwargs.get('rtos', embedded_config['default_rtos'])
        target = kwargs.get('target', embedded_config['target_mcu'])
        peripheral = kwargs.get('peripheral')

        # Load system prompt
        system_prompt = self._load_embedded_prompt()

        # Build specific prompt
        prompt = f"""{system_prompt}

Target Configuration:
- RTOS: {rtos}
- Microcontroller: {target}
- C++ Standard: {cpp_config['standard']}
- Optimization: {cpp_config['optimization']}
"""

        if peripheral:
            prompt += f"- Peripheral: {peripheral}\n"

        prompt += f"""
Task: {description}
"""

        if context:
            prompt += f"\nAdditional Context:\n{context}\n"

        prompt += """
Requirements:
- Follow MISRA C++ guidelines where applicable
- No exceptions (-fno-exceptions)
- No RTTI (-fno-rtti)
- Use static memory allocation
- Include necessary headers
- Add brief comments for complex logic

Generate the C++ code:
"""

        # Generate code
        response = await self.llm.generate(prompt, **kwargs)

        # Extract code from response
        code = self._extract_code(response)

        return code

    async def _generate_general(
        self,
        description: str,
        language: str,
        context: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate code for general-purpose languages

        Args:
            description: Code description
            language: Programming language
            context: Additional context
            **kwargs: Additional parameters

        Returns:
            Generated code
        """
        prompt = f"""You are an expert {language} programmer.

Generate {language} code for the following task:

Task: {description}
"""

        if context:
            prompt += f"\nContext:\n{context}\n"

        prompt += f"""
Requirements:
- Write clean, well-documented code
- Follow {language} best practices
- Include error handling
- Add docstrings/comments

Generate only the {language} code:
"""

        response = await self.llm.generate(prompt, **kwargs)
        code = self._extract_code(response, language)

        return code

    def _load_embedded_prompt(self) -> str:
        """Load embedded C++ system prompt"""
        prompt_path = Path("config/prompts/embedded_cpp_system.md")

        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()

        # Fallback prompt
        return """You are an expert embedded systems engineer specializing in C++ development for microcontrollers and RTOS."""

    def _extract_code(self, response: str, language: Optional[str] = None) -> str:
        """
        Extract code from LLM response

        Args:
            response: LLM response text
            language: Programming language hint

        Returns:
            Extracted code
        """
        # Try to find code blocks with language specifier
        patterns = [
            r"```(?:cpp|c\+\+|c)\n(.*?)\n```",  # C++ code blocks
            r"```(?:python|py)\n(.*?)\n```",    # Python code blocks
            r"```(?:typescript|ts)\n(.*?)\n```",  # TypeScript code blocks
            r"```(?:\w+)?\n(.*?)\n```",         # Any code block
        ]

        for pattern in patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            if matches:
                return matches[0].strip()

        # If no code blocks found, try to extract code-like content
        lines = response.split('\n')
        code_lines = []
        in_code = False

        for line in lines:
            # Detect code start
            if any(keyword in line for keyword in ['#include', 'def ', 'class ', 'function ', 'void ', 'int ', 'const ']):
                in_code = True

            if in_code:
                # Skip obvious non-code lines
                if line.strip() and not line.startswith(('Note:', 'Explanation:', 'This code')):
                    code_lines.append(line)

        if code_lines:
            return '\n'.join(code_lines).strip()

        # Return original if can't extract
        return response.strip()

    async def generate_freertos_task(
        self,
        task_name: str,
        description: str,
        priority: int = 1,
        stack_size: int = 256,
        **kwargs
    ) -> str:
        """
        Generate FreeRTOS task code

        Args:
            task_name: Task name
            description: What the task should do
            priority: Task priority (relative to idle)
            stack_size: Stack size in words
            **kwargs: Additional parameters

        Returns:
            Generated FreeRTOS task code
        """
        full_description = f"""Create a FreeRTOS task named '{task_name}' that {description}.

Task Specifications:
- Task Name: {task_name}
- Priority: tskIDLE_PRIORITY + {priority}
- Stack Size: {stack_size} words
- Use static allocation (xTaskCreateStatic)

Include:
1. Task function implementation
2. Static stack and task buffer declarations
3. Task creation function
"""

        return await self._generate_embedded_cpp(
            full_description,
            rtos="freertos",
            **kwargs
        )

    async def generate_peripheral_driver(
        self,
        peripheral: str,
        operation: str,
        **kwargs
    ) -> str:
        """
        Generate peripheral driver code

        Args:
            peripheral: Peripheral type (uart, i2c, spi, gpio, etc.)
            operation: What operation to perform
            **kwargs: Additional parameters (target, pins, etc.)

        Returns:
            Generated driver code
        """
        target = kwargs.get('target', self.config.embedded.target_mcu)

        description = f"""Generate {peripheral.upper()} driver code for {target} that {operation}.

Include:
1. Peripheral initialization
2. HAL/LL function calls
3. Error handling
4. Pin configuration if relevant
"""

        return await self._generate_embedded_cpp(
            description,
            peripheral=peripheral,
            **kwargs
        )

    async def generate_interrupt_handler(
        self,
        interrupt_source: str,
        action: str,
        **kwargs
    ) -> str:
        """
        Generate interrupt service routine

        Args:
            interrupt_source: Interrupt source (timer, uart, gpio, etc.)
            action: What to do in the ISR
            **kwargs: Additional parameters

        Returns:
            Generated ISR code
        """
        description = f"""Generate an interrupt service routine (ISR) for {interrupt_source} that {action}.

Requirements:
- Minimal processing in ISR
- Defer heavy work to tasks using FreeRTOS primitives
- Proper interrupt flag clearing
- Use portYIELD_FROM_ISR if waking higher priority task

Include:
1. ISR function (extern "C")
2. Any required task notification or semaphore handling
3. Interrupt configuration
"""

        return await self._generate_embedded_cpp(
            description,
            **kwargs
        )


# Example usage
async def example_usage():
    """Example usage of Code Generator"""

    generator = CodeGenerator()

    # Example 1: FreeRTOS LED blink task
    print("=== FreeRTOS LED Blink Task ===")
    code = await generator.generate_freertos_task(
        task_name="ledTask",
        description="toggles LED on GPIO pin PA5 every 1000ms",
        priority=1,
        stack_size=128,
        target="stm32f4"
    )
    print(code)
    print("\n" + "="*50 + "\n")

    # Example 2: UART driver
    print("=== UART Driver ===")
    code = await generator.generate_peripheral_driver(
        peripheral="uart",
        operation="sends 'Hello World' at 115200 baud using UART2",
        target="stm32f4"
    )
    print(code)
    print("\n" + "="*50 + "\n")

    # Example 3: Timer interrupt
    print("=== Timer Interrupt Handler ===")
    code = await generator.generate_interrupt_handler(
        interrupt_source="TIM2 update",
        action="gives a binary semaphore to wake a processing task",
        target="stm32f4"
    )
    print(code)
    print("\n" + "="*50 + "\n")

    # Example 4: Python code (general)
    print("=== Python Binary Search ===")
    code = await generator.generate(
        description="implement binary search algorithm",
        language="python",
        embedded=False
    )
    print(code)


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
