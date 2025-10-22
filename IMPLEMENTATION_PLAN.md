# 実装計画書
# My-devin: ローカルLLM自動開発プラットフォーム

**バージョン**: 1.0
**作成日**: 2025-10-22
**想定期間**: 22週間（約5.5ヶ月）

---

## 目次
1. [開発方針](#1-開発方針)
2. [技術アーキテクチャ詳細](#2-技術アーキテクチャ詳細)
3. [Phase 1: MVP実装](#3-phase-1-mvp実装)
4. [Phase 2: コア機能実装](#4-phase-2-コア機能実装)
5. [Phase 3: 高度機能実装](#5-phase-3-高度機能実装)
6. [Phase 4: 最終調整とリリース](#6-phase-4-最終調整とリリース)
7. [開発環境セットアップ](#7-開発環境セットアップ)
8. [テスト戦略](#8-テスト戦略)
9. [デプロイメント戦略](#9-デプロイメント戦略)

---

## 1. 開発方針

### 1.1 基本原則
- **アジャイル開発**: 2週間スプリント
- **MVP優先**: 最小限の機能で早期リリース
- **品質重視**: テスト駆動開発（TDD）
- **ドキュメント同時作成**: コードと同時にドキュメント更新
- **モジュラー設計**: 各コンポーネントを独立して開発・テスト可能に

### 1.2 開発環境
- **バージョン管理**: Git + GitHub
- **ブランチ戦略**: GitHub Flow
  - `main`: 常にリリース可能な状態
  - `develop`: 開発統合ブランチ
  - `feature/*`: 機能開発ブランチ
  - `hotfix/*`: 緊急修正ブランチ

### 1.3 コーディング規約
- **Python**: PEP 8 + Black + Ruff
- **TypeScript**: ESLint + Prettier
- **コミットメッセージ**: Conventional Commits形式
  ```
  feat: 新機能
  fix: バグ修正
  docs: ドキュメント
  refactor: リファクタリング
  test: テスト追加
  chore: その他
  ```

---

## 2. 技術アーキテクチャ詳細

### 2.1 ディレクトリ構造

```
my-devin/
├── backend/                    # Pythonバックエンド
│   ├── src/
│   │   ├── core/              # コアロジック
│   │   │   ├── __init__.py
│   │   │   ├── config.py      # 設定管理
│   │   │   ├── models.py      # データモデル
│   │   │   └── exceptions.py  # カスタム例外
│   │   ├── llm/               # LLM統合レイヤー
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # 抽象基底クラス
│   │   │   ├── ollama.py      # Ollama実装
│   │   │   ├── mlx.py         # MLX実装
│   │   │   ├── llamacpp.py    # llama.cpp実装
│   │   │   └── manager.py     # モデル管理
│   │   ├── services/          # ビジネスロジック
│   │   │   ├── code_generator.py
│   │   │   ├── code_analyzer.py
│   │   │   ├── refactoring.py
│   │   │   ├── git_service.py
│   │   │   └── project_service.py
│   │   ├── agents/            # エージェント機能
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py
│   │   │   ├── coding_agent.py
│   │   │   ├── debug_agent.py
│   │   │   └── workflow.py
│   │   ├── parsers/           # コードパーサー
│   │   │   ├── __init__.py
│   │   │   ├── python_parser.py
│   │   │   ├── typescript_parser.py
│   │   │   └── tree_sitter_wrapper.py
│   │   ├── api/               # REST API
│   │   │   ├── __init__.py
│   │   │   ├── main.py        # FastAPIアプリ
│   │   │   ├── routes/
│   │   │   │   ├── llm.py
│   │   │   │   ├── code.py
│   │   │   │   ├── project.py
│   │   │   │   └── agent.py
│   │   │   └── websocket.py   # WebSocket通信
│   │   └── utils/             # ユーティリティ
│   │       ├── file_utils.py
│   │       ├── git_utils.py
│   │       └── logger.py
│   ├── tests/                 # テスト
│   │   ├── unit/
│   │   ├── integration/
│   │   └── fixtures/
│   ├── pyproject.toml         # Python依存管理
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                  # Web UIフロントエンド
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   ├── Editor/
│   │   │   ├── ProjectBrowser/
│   │   │   └── Settings/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── stores/            # 状態管理（Zustand/Redux）
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md
│
├── cli/                       # CLIツール
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py            # エントリーポイント
│   │   ├── commands/
│   │   │   ├── chat.py
│   │   │   ├── generate.py
│   │   │   ├── analyze.py
│   │   │   └── config.py
│   │   └── ui/
│   │       ├── chat_ui.py
│   │       └── progress.py
│   ├── pyproject.toml
│   └── README.md
│
├── vscode-extension/          # VSCode拡張（Phase 3）
│   ├── src/
│   ├── package.json
│   └── README.md
│
├── shared/                    # 共通定義
│   ├── schemas/               # APIスキーマ
│   └── types/                 # 型定義
│
├── docs/                      # ドキュメント
│   ├── api/
│   ├── architecture/
│   ├── user-guide/
│   └── development/
│
├── scripts/                   # ビルド・デプロイスクリプト
│   ├── setup.sh
│   ├── install_models.sh
│   └── run_dev.sh
│
├── config/                    # 設定ファイル
│   ├── default.yaml
│   ├── models.yaml
│   └── prompts/
│
├── .github/                   # GitHub Actions
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
│
├── docker/                    # Docker設定（オプション）
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── README.md
├── LICENSE
├── .gitignore
└── CHANGELOG.md
```

### 2.2 データフロー

```
┌─────────┐
│  User   │
└────┬────┘
     │
     ↓
┌─────────────────────────────────┐
│  CLI / Web UI / VSCode          │
└────┬────────────────────────────┘
     │ HTTP/WebSocket
     ↓
┌─────────────────────────────────┐
│  FastAPI Server                 │
│  ┌──────────────────────────┐  │
│  │  API Routes              │  │
│  └──────────┬───────────────┘  │
│             ↓                   │
│  ┌──────────────────────────┐  │
│  │  Agent Engine            │  │
│  └──────────┬───────────────┘  │
│             ↓                   │
│  ┌──────────────────────────┐  │
│  │  Services                │  │
│  │  - Code Generator        │  │
│  │  - Analyzer              │  │
│  │  - Git Manager           │  │
│  └──────────┬───────────────┘  │
└─────────────┼───────────────────┘
              ↓
┌─────────────────────────────────┐
│  LLM Abstraction Layer          │
│  ┌────────┐ ┌─────┐ ┌────────┐ │
│  │ Ollama │ │ MLX │ │llamacpp│ │
│  └────┬───┘ └──┬──┘ └───┬────┘ │
└───────┼────────┼────────┼───────┘
        ↓        ↓        ↓
┌─────────────────────────────────┐
│  Local LLM Models               │
│  - Qwen3-coder 7B/14B/32B       │
│  - DeepSeek-Coder               │
│  - CodeLlama                    │
└─────────────────────────────────┘
```

---

## 3. Phase 1: MVP実装

**期間**: 4週間（スプリント1-2）
**目標**: 基本的なコード生成とLLM連携を実現

### 3.1 Sprint 1（Week 1-2）: LLM基盤構築

#### タスク詳細

**1.1 プロジェクトセットアップ**
- [ ] リポジトリ初期化
- [ ] ディレクトリ構造作成
- [ ] 依存関係定義（pyproject.toml, package.json）
- [ ] 開発環境設定（linter, formatter）
- [ ] CI/CD設定（GitHub Actions）

**1.2 LLM統合基盤**
```python
# backend/src/llm/base.py
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
        """テキスト生成"""
        pass

    @abstractmethod
    async def stream_generate(
        self,
        prompt: str,
        **kwargs
    ) -> AsyncIterator[str]:
        """ストリーミング生成"""
        pass

    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """モデル情報取得"""
        pass
```

**1.3 Ollama実装**
```python
# backend/src/llm/ollama.py
import httpx
from .base import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "qwen2.5-coder:32b"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434"

    async def generate(self, prompt: str, **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    **kwargs
                }
            )
            return response.json()["response"]

    async def stream_generate(self, prompt: str, **kwargs):
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": True,
                    **kwargs
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        yield data.get("response", "")
```

**1.4 設定管理**
```python
# backend/src/core/config.py
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    # LLM設定
    llm_provider: Literal["ollama", "mlx", "llamacpp"] = "ollama"
    default_model: str = "qwen2.5-coder:32b"

    # API設定
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # プロジェクト設定
    workspace_dir: str = "./workspace"

    # ログ設定
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
```

**1.5 テスト作成**
```python
# backend/tests/unit/test_ollama.py
import pytest
from src.llm.ollama import OllamaProvider

@pytest.mark.asyncio
async def test_ollama_generate():
    provider = OllamaProvider()
    result = await provider.generate("Write a Python function to add two numbers")
    assert "def" in result
    assert len(result) > 0
```

**成果物**:
- [ ] LLM抽象レイヤー実装
- [ ] Ollama統合完了
- [ ] 設定管理システム
- [ ] 基本テストスイート

### 3.2 Sprint 2（Week 3-4）: CLI基本機能

#### タスク詳細

**2.1 CLIフレームワーク構築**
```python
# cli/src/main.py
import typer
from rich.console import Console
from rich.markdown import Markdown

app = typer.Typer(name="my-devin")
console = Console()

@app.command()
def chat():
    """対話型チャットモード"""
    console.print("[bold blue]My-devin Chat Mode[/bold blue]")
    # 実装...

@app.command()
def generate(
    prompt: str = typer.Argument(..., help="生成プロンプト"),
    language: str = typer.Option("python", help="言語"),
    output: str = typer.Option(None, help="出力ファイル")
):
    """コード生成"""
    # 実装...

@app.command()
def analyze(
    path: str = typer.Argument(..., help="解析対象パス")
):
    """プロジェクト解析"""
    # 実装...

if __name__ == "__main__":
    app()
```

**2.2 コード生成サービス**
```python
# backend/src/services/code_generator.py
from typing import Optional
from ..llm.manager import LLMManager

class CodeGenerator:
    def __init__(self, llm_manager: LLMManager):
        self.llm = llm_manager

    async def generate_code(
        self,
        description: str,
        language: str = "python",
        context: Optional[str] = None
    ) -> str:
        """コード生成"""
        prompt = self._build_prompt(description, language, context)
        code = await self.llm.generate(prompt)
        return self._extract_code(code)

    def _build_prompt(self, description: str, language: str, context: Optional[str]) -> str:
        """プロンプト構築"""
        base_prompt = f"""Generate {language} code for the following task:

Task: {description}

Requirements:
- Write clean, well-documented code
- Follow {language} best practices
- Include error handling
"""
        if context:
            base_prompt += f"\nContext:\n{context}\n"

        base_prompt += f"\nGenerate only the {language} code, wrapped in triple backticks."
        return base_prompt

    def _extract_code(self, response: str) -> str:
        """コードブロック抽出"""
        import re
        pattern = r"```(?:\w+)?\n(.*?)\n```"
        matches = re.findall(pattern, response, re.DOTALL)
        return matches[0] if matches else response
```

**2.3 プロジェクト解析基礎**
```python
# backend/src/services/project_service.py
import os
from pathlib import Path
from typing import List, Dict

class ProjectAnalyzer:
    def __init__(self):
        self.ignore_patterns = [
            "__pycache__", "node_modules", ".git",
            "venv", ".venv", "dist", "build"
        ]

    def analyze_structure(self, root_path: str) -> Dict:
        """プロジェクト構造解析"""
        structure = {
            "root": root_path,
            "languages": self._detect_languages(root_path),
            "file_tree": self._build_tree(root_path),
            "stats": self._calculate_stats(root_path)
        }
        return structure

    def _detect_languages(self, root_path: str) -> List[str]:
        """使用言語検出"""
        extensions = set()
        for root, _, files in os.walk(root_path):
            if any(pattern in root for pattern in self.ignore_patterns):
                continue
            for file in files:
                ext = Path(file).suffix
                if ext:
                    extensions.add(ext)

        # 拡張子から言語マッピング
        lang_map = {
            ".py": "Python",
            ".ts": "TypeScript",
            ".js": "JavaScript",
            ".go": "Go",
            ".rs": "Rust",
            # 他の言語...
        }

        return [lang_map.get(ext, ext) for ext in extensions if ext in lang_map]
```

**成果物**:
- [ ] CLI基本コマンド（chat, generate, analyze）
- [ ] コード生成機能
- [ ] プロジェクト解析機能
- [ ] ドキュメント（使い方）

### 3.3 MVP完成チェックリスト

- [ ] Ollamaでモデルをロードし、推論可能
- [ ] CLIから「Pythonで2つの数を足す関数を作って」でコード生成
- [ ] プロジェクトディレクトリの構造を解析できる
- [ ] ユニットテストが全てパス
- [ ] READMEにセットアップ手順を記載

---

## 4. Phase 2: コア機能実装

**期間**: 6週間（スプリント3-5）
**目標**: マルチLLM対応、エージェント、Web UI

### 4.1 Sprint 3（Week 5-6）: マルチLLMバックエンド

**3.1 MLX統合**
```python
# backend/src/llm/mlx.py
from mlx_lm import load, generate
from .base import BaseLLMProvider

class MLXProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "mlx-community/Qwen2.5-Coder-32B-Instruct-8bit"):
        self.model, self.tokenizer = load(model_name)

    async def generate(self, prompt: str, **kwargs) -> str:
        max_tokens = kwargs.get("max_tokens", 2048)
        temperature = kwargs.get("temperature", 0.7)

        response = generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            temp=temperature
        )
        return response
```

**3.2 LLMマネージャー**
```python
# backend/src/llm/manager.py
from typing import Dict, Type
from .base import BaseLLMProvider
from .ollama import OllamaProvider
from .mlx import MLXProvider
from .llamacpp import LlamaCppProvider

class LLMManager:
    """LLMプロバイダーの統一管理"""

    _providers: Dict[str, Type[BaseLLMProvider]] = {
        "ollama": OllamaProvider,
        "mlx": MLXProvider,
        "llamacpp": LlamaCppProvider
    }

    def __init__(self, provider_name: str = "ollama", **kwargs):
        self.provider_name = provider_name
        self.provider = self._create_provider(provider_name, **kwargs)

    def _create_provider(self, name: str, **kwargs) -> BaseLLMProvider:
        if name not in self._providers:
            raise ValueError(f"Unknown provider: {name}")
        return self._providers[name](**kwargs)

    async def generate(self, prompt: str, **kwargs) -> str:
        return await self.provider.generate(prompt, **kwargs)

    async def stream_generate(self, prompt: str, **kwargs):
        async for chunk in self.provider.stream_generate(prompt, **kwargs):
            yield chunk

    def switch_provider(self, provider_name: str, **kwargs):
        """プロバイダー切り替え"""
        self.provider_name = provider_name
        self.provider = self._create_provider(provider_name, **kwargs)
```

**成果物**:
- [ ] MLX統合
- [ ] llama.cpp統合
- [ ] LLMマネージャー実装
- [ ] プロバイダー切り替え機能

### 4.2 Sprint 4（Week 7-9）: エージェント機能

**4.1 基本エージェント**
```python
# backend/src/agents/base_agent.py
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class AgentTask:
    id: str
    description: str
    status: AgentStatus
    result: Any = None
    error: str = None

class BaseAgent:
    """基本エージェントクラス"""

    def __init__(self, llm_manager, name: str = "Agent"):
        self.llm = llm_manager
        self.name = name
        self.status = AgentStatus.IDLE
        self.memory: List[Dict] = []

    async def execute_task(self, task: AgentTask) -> AgentTask:
        """タスク実行"""
        self.status = AgentStatus.THINKING

        try:
            # 計画立案
            plan = await self._create_plan(task.description)

            # 実行
            self.status = AgentStatus.EXECUTING
            result = await self._execute_plan(plan)

            task.status = AgentStatus.COMPLETED
            task.result = result
            self.status = AgentStatus.IDLE

        except Exception as e:
            task.status = AgentStatus.FAILED
            task.error = str(e)
            self.status = AgentStatus.IDLE

        return task

    async def _create_plan(self, task_description: str) -> List[Dict]:
        """計画作成"""
        prompt = f"""Given the task: {task_description}

Create a step-by-step plan to complete this task. Return the plan as a JSON array of steps.

Example format:
[
  {{"step": 1, "action": "analyze_requirements", "details": "..."}},
  {{"step": 2, "action": "write_code", "details": "..."}}
]
"""
        response = await self.llm.generate(prompt)
        # JSONパース処理
        return self._parse_plan(response)

    async def _execute_plan(self, plan: List[Dict]) -> Any:
        """計画実行"""
        results = []
        for step in plan:
            result = await self._execute_step(step)
            results.append(result)
            self.memory.append({"step": step, "result": result})
        return results

    async def _execute_step(self, step: Dict) -> Any:
        """ステップ実行（サブクラスで実装）"""
        raise NotImplementedError
```

**4.2 コーディングエージェント**
```python
# backend/src/agents/coding_agent.py
from .base_agent import BaseAgent
from ..services.code_generator import CodeGenerator
from ..services.git_service import GitService

class CodingAgent(BaseAgent):
    """コード生成特化エージェント"""

    def __init__(self, llm_manager):
        super().__init__(llm_manager, name="CodingAgent")
        self.code_generator = CodeGenerator(llm_manager)
        self.git_service = GitService()

    async def _execute_step(self, step: Dict) -> Any:
        action = step["action"]

        if action == "analyze_requirements":
            return await self._analyze_requirements(step["details"])
        elif action == "write_code":
            return await self._write_code(step["details"])
        elif action == "write_tests":
            return await self._write_tests(step["details"])
        elif action == "commit_changes":
            return await self._commit_changes(step["details"])
        else:
            raise ValueError(f"Unknown action: {action}")

    async def _write_code(self, details: Dict) -> str:
        """コード生成"""
        code = await self.code_generator.generate_code(
            description=details["description"],
            language=details.get("language", "python"),
            context=details.get("context")
        )

        # ファイルに保存
        file_path = details.get("file_path")
        if file_path:
            with open(file_path, "w") as f:
                f.write(code)

        return code
```

**成果物**:
- [ ] BaseAgent実装
- [ ] CodingAgent実装
- [ ] DebugAgent実装
- [ ] ワークフロー管理システム

### 4.3 Sprint 5（Week 10-11）: Web UI開発

**5.1 フロントエンドセットアップ**
```typescript
// frontend/src/services/api.ts
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export interface GenerateCodeRequest {
  description: string;
  language: string;
  context?: string;
}

export interface GenerateCodeResponse {
  code: string;
  explanation?: string;
}

export const codeService = {
  generate: async (request: GenerateCodeRequest): Promise<GenerateCodeResponse> => {
    const response = await api.post('/api/code/generate', request);
    return response.data;
  },

  analyze: async (code: string, language: string) => {
    const response = await api.post('/api/code/analyze', { code, language });
    return response.data;
  },
};
```

**5.2 チャットコンポーネント**
```tsx
// frontend/src/components/Chat/ChatInterface.tsx
import React, { useState } from 'react';
import { Send } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // WebSocket接続でストリーミング
      const ws = new WebSocket('ws://localhost:8000/ws/chat');

      ws.onopen = () => {
        ws.send(JSON.stringify({ message: input }));
      };

      let assistantMessage = '';
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        assistantMessage += data.chunk;

        setMessages(prev => {
          const newMessages = [...prev];
          const lastMessage = newMessages[newMessages.length - 1];

          if (lastMessage?.role === 'assistant') {
            lastMessage.content = assistantMessage;
          } else {
            newMessages.push({
              id: Date.now().toString(),
              role: 'assistant',
              content: assistantMessage,
              timestamp: new Date(),
            });
          }

          return newMessages;
        });
      };

      ws.onclose = () => {
        setIsLoading(false);
      };
    } catch (error) {
      console.error('Error:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900">
      {/* メッセージ一覧 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(msg => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-2xl p-4 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-100'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
      </div>

      {/* 入力エリア */}
      <div className="border-t border-gray-700 p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your message..."
            className="flex-1 bg-gray-800 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-6 py-2 flex items-center gap-2 disabled:opacity-50"
          >
            <Send size={20} />
            Send
          </button>
        </div>
      </div>
    </div>
  );
};
```

**成果物**:
- [ ] React + TypeScript + Viteセットアップ
- [ ] チャットインターフェース
- [ ] コードエディタ統合（Monaco）
- [ ] プロジェクトブラウザ

---

## 5. Phase 3: 高度機能実装

**期間**: 8週間（スプリント6-9）

### 5.1 高度コード解析（tree-sitter統合）
### 5.2 VSCode拡張機能開発
### 5.3 プラグインシステム構築
### 5.4 パフォーマンス最適化

詳細は各スプリントで展開...

---

## 6. Phase 4: 最終調整とリリース

**期間**: 4週間（スプリント10-11）

### 6.1 品質保証
- [ ] 全機能テスト
- [ ] パフォーマンステスト
- [ ] セキュリティ監査
- [ ] ユーザビリティテスト

### 6.2 ドキュメント完成
- [ ] APIドキュメント（OpenAPI）
- [ ] ユーザーガイド
- [ ] 開発者ガイド
- [ ] チュートリアル動画

### 6.3 リリース準備
- [ ] バージョン1.0パッケージング
- [ ] リリースノート作成
- [ ] GitHub Pages公開
- [ ] コミュニティ構築

---

## 7. 開発環境セットアップ

### 7.1 必須ツール

```bash
# Homebrew（パッケージマネージャー）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.11+
brew install python@3.11

# Node.js 20+
brew install node@20

# Ollama
brew install ollama

# Git
brew install git
```

### 7.2 プロジェクトセットアップ

```bash
# リポジトリクローン
git clone <repository-url>
cd my-devin

# バックエンドセットアップ
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# フロントエンドセットアップ
cd ../frontend
npm install

# CLIセットアップ
cd ../cli
pip install -e .

# モデルダウンロード
ollama pull qwen2.5-coder:32b
```

### 7.3 開発サーバー起動

```bash
# ターミナル1: バックエンド
cd backend
python -m uvicorn src.api.main:app --reload

# ターミナル2: フロントエンド
cd frontend
npm run dev

# ターミナル3: Ollama
ollama serve
```

---

## 8. テスト戦略

### 8.1 テストピラミッド

```
       /\
      /  \  E2E Tests (10%)
     /────\
    / Inte \  Integration Tests (30%)
   /  gration\
  /──────────\
 /   Unit     \  Unit Tests (60%)
/   Tests      \
────────────────
```

### 8.2 テストカバレッジ目標

- **ユニットテスト**: 80%以上
- **統合テスト**: 主要フロー全てカバー
- **E2Eテスト**: クリティカルパス全てカバー

### 8.3 テスト実行

```bash
# バックエンドテスト
cd backend
pytest tests/ -v --cov=src --cov-report=html

# フロントエンドテスト
cd frontend
npm test
npm run test:coverage

# E2Eテスト
npm run test:e2e
```

---

## 9. デプロイメント戦略

### 9.1 ローカルインストール

```bash
# PyPIパッケージとして配布
pip install my-devin

# または
brew install my-devin
```

### 9.2 バージョニング

- **セマンティックバージョニング**: MAJOR.MINOR.PATCH
- **リリースサイクル**:
  - Major: 年1回
  - Minor: 月1回
  - Patch: 週1回（必要に応じて）

---

## 10. 開発マイルストーン

| マイルストーン | 完了予定 | 主要成果物 |
|--------------|---------|-----------|
| M1: MVP | Week 4 | LLM統合、基本CLI |
| M2: コア機能 | Week 11 | マルチLLM、エージェント、Web UI |
| M3: 高度機能 | Week 19 | VSCode拡張、プラグイン |
| M4: v1.0リリース | Week 22 | 製品版リリース |

---

## 11. 次のステップ

1. **今すぐ開始**: プロジェクトディレクトリ作成
2. **Week 1**: LLM基盤実装
3. **継続的改善**: 毎スプリント終了時にレトロスペクティブ

---

**承認者**: ___________________
**日付**: ___________________
