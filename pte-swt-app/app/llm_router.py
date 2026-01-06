import subprocess
from app.llm_client import LocalLLMClient
from app.llm_ollama import OllamaClient


def gpu_available() -> bool:
    try:
        subprocess.run(
            ["nvidia-smi"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except Exception:
        return False


class LLMRouter:
    """
    Auto-selects:
    - vLLM (GPU)
    - Ollama (CPU)
    """

    def __init__(self):
        if gpu_available():
            print("✅ GPU detected → using vLLM")
            self.client = LocalLLMClient()
        else:
            print("⚠️ GPU not found → using Ollama")
            self.client = OllamaClient()

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        return self.client.chat(system_prompt, user_prompt)
