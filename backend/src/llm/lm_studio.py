"""
LM Studio Provider
OpenAI互換APIを使用してLM Studioと統合
"""

from typing import AsyncIterator, Dict, Any, Optional
from openai import AsyncOpenAI
from .base import BaseLLMProvider


class LMStudioProvider(BaseLLMProvider):
    """LM Studio用LLMプロバイダー（OpenAI互換API）"""

    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1",
        api_key: str = "lm-studio",
        model_name: str = "qwen2.5-coder-32b-instruct",
        timeout: int = 300,
    ):
        """
        Args:
            base_url: LM StudioのベースURL（デフォルト: http://localhost:1234/v1）
            api_key: APIキー（LM Studioではダミーキーでも動作）
            model_name: 使用するモデル名
            timeout: タイムアウト（秒）
        """
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name
        self.timeout = timeout

        # OpenAIクライアント初期化（LM Studio互換）
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> str:
        """
        テキスト生成（非ストリーミング）

        Args:
            prompt: 入力プロンプト
            temperature: 温度パラメータ（0.0-2.0）
            max_tokens: 最大トークン数
            **kwargs: その他のパラメータ

        Returns:
            生成されたテキスト
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False,
                **kwargs
            )

            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"LM Studio generation failed: {e}")

    async def stream_generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        ストリーミングテキスト生成

        Args:
            prompt: 入力プロンプト
            temperature: 温度パラメータ
            max_tokens: 最大トークン数
            **kwargs: その他のパラメータ

        Yields:
            生成されたテキストチャンク
        """
        try:
            stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            raise RuntimeError(f"LM Studio streaming failed: {e}")

    async def get_model_info(self) -> Dict[str, Any]:
        """
        モデル情報を取得

        Returns:
            モデル情報の辞書
        """
        try:
            # 利用可能なモデル一覧を取得
            models = await self.client.models.list()

            model_list = [model.id for model in models.data]

            return {
                "provider": "lm-studio",
                "base_url": self.base_url,
                "current_model": self.model_name,
                "available_models": model_list,
                "timeout": self.timeout,
            }

        except Exception as e:
            return {
                "provider": "lm-studio",
                "base_url": self.base_url,
                "current_model": self.model_name,
                "error": str(e),
            }

    async def health_check(self) -> bool:
        """
        LM Studioサーバーのヘルスチェック

        Returns:
            サーバーが正常ならTrue
        """
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False

    async def list_models(self) -> list[str]:
        """
        利用可能なモデル一覧を取得

        Returns:
            モデル名のリスト
        """
        try:
            models = await self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            raise RuntimeError(f"Failed to list models: {e}")

    async def generate_code(
        self,
        description: str,
        language: str = "python",
        context: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        コード生成専用メソッド

        Args:
            description: コードの説明
            language: プログラミング言語
            context: 追加のコンテキスト
            **kwargs: その他のパラメータ

        Returns:
            生成されたコード
        """
        system_prompt = f"""You are an expert {language} programmer.
Generate clean, well-documented, and efficient code.
Follow best practices and include error handling where appropriate."""

        user_prompt = f"""Generate {language} code for the following task:

Task: {description}"""

        if context:
            user_prompt += f"\n\nContext:\n{context}"

        user_prompt += f"\n\nGenerate only the {language} code without explanations."

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2048),
                stream=False,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"Code generation failed: {e}")


# 使用例
async def example_usage():
    """LM Studio Providerの使用例"""

    # プロバイダー初期化
    provider = LMStudioProvider(
        base_url="http://localhost:1234/v1",
        model_name="qwen2.5-coder-32b-instruct"
    )

    # ヘルスチェック
    is_healthy = await provider.health_check()
    print(f"LM Studio Health: {is_healthy}")

    # モデル一覧取得
    models = await provider.list_models()
    print(f"Available models: {models}")

    # コード生成
    code = await provider.generate_code(
        description="Create a function to calculate fibonacci numbers",
        language="python"
    )
    print(f"Generated code:\n{code}")

    # ストリーミング生成
    print("\nStreaming generation:")
    async for chunk in provider.stream_generate("Explain what is a binary tree"):
        print(chunk, end="", flush=True)
    print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
