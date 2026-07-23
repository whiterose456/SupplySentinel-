import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

for env_path in [
    BASE_DIR / ".env.testing",
    BASE_DIR / ".env",
    BASE_DIR.parent / ".env",
    BASE_DIR.parent.parent / ".env",
]:
    if env_path.exists():
        load_dotenv(env_path, override=True)


def _read_setting(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value.strip().strip('"').strip("'")
    return default


api_key = _read_setting("DASHSCOPE_API_KEY", "OPENAI_API_KEY")
base_url = _read_setting(
    "DASHSCOPE_BASE_URL",
    "OPENAI_BASE_URL",
    default="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)
model_name = _read_setting("MODEL_NAME", default="qwen-plus")


class SimpleMessage:
    def __init__(self, content: str):
        self.content = content


class SimpleLLM:
    def __init__(self, temperature: float = 0.0):
        self.temperature = temperature

    def invoke(self, messages: Any):
        if isinstance(messages, str):
            content = messages
        elif messages:
            last_message = messages[-1]
            content = getattr(last_message, "content", str(last_message))
        else:
            content = "Hello from the fallback LLM"
        return SimpleMessage(content)


def get_llm(temperature: float = 0.0):
    """Return a working LLM object, falling back to a local stub when no key is configured."""
    if not api_key:
        return SimpleLLM(temperature=temperature)

    try:
        from openai import OpenAI
    except Exception:
        return SimpleLLM(temperature=temperature)

    client = OpenAI(api_key=api_key, base_url=base_url)
    return _OpenAICompat(client, model_name=model_name, temperature=temperature)


class _OpenAICompat:
    def __init__(self, client: Any, model_name: str, temperature: float = 0.0):
        self._client = client
        self._model_name = model_name
        self.temperature = temperature

    def invoke(self, messages: Any):
        completion = self._client.chat.completions.create(
            model=self._model_name,
            messages=[{"role": "user", "content": str(messages)}],
        )
        return SimpleMessage(completion.choices[0].message.content)