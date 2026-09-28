from functools import lru_cache
from .config import (
    GEMINI_API_KEY, GEMINI_MAX_OUTPUT_TOKENS, GEMINI_TEMPERATURE
)

@lru_cache(maxsize=1)
def get_client():
    from google import genai
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "Gemini API key is not configured. Add GEMINI_API_KEY to your .env file."
        )
    return genai.Client(api_key=GEMINI_API_KEY)

def generate_text(model: str, prompt: str, system_instruction: str) -> str:
    from google.genai import types
    client = get_client()
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=GEMINI_TEMPERATURE,
            max_output_tokens=GEMINI_MAX_OUTPUT_TOKENS,
        ),
    )
    text = response.text
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
