from google import genai
from ops_copilot.config import GEMINI_API_KEY, DEFAULT_MODEL


def get_gemini_client():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set.")
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_reply(prompt: str, temperature: float = 0.2) -> str:
    client = get_gemini_client()
    resp = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config={"temperature": temperature},
    )
    return resp.text
