"""
LLM Provider Base Class
全てのLLMプロバイダーが実装すべき抽象基底クラス
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Dict, Any


class BaseLLMProvider(ABC):
    """LLMプロバイダーの抽象基底クラス"""

    @abstractmethod
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
            **kwargs: プロバイダー固有のパラメータ

        Returns:
            生成されたテキスト

        Raises:
            RuntimeError: 生成に失敗した場合
        """
        pass

    @abstractmethod
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
            **kwargs: プロバイダー固有のパラメータ

        Yields:
            生成されたテキストのチャンク

        Raises:
            RuntimeError: 生成に失敗した場合
        """
        pass

    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """
        モデル情報を取得

        Returns:
            モデル情報を含む辞書:
                - provider: プロバイダー名
                - model: モデル名
                - その他プロバイダー固有の情報
        """
        pass

    async def health_check(self) -> bool:
        """
        ヘルスチェック（オプション）

        Returns:
            サーバーが正常ならTrue

        Note:
            デフォルト実装はTrueを返す。
            各プロバイダーで必要に応じてオーバーライド。
        """
        return True
