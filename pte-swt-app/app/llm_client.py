from openai import OpenAI


class LocalLLMClient:
    """
    vLLM OpenAI-compatible client (localhost)
    """

    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:8000/v1",
            api_key="EMPTY",  # required by SDK, ignored by vLLM
        )

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            temperature=0,
            top_p=1,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return resp.choices[0].message.content.strip()
