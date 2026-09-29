from .config import TIP_MODEL
from .gemini_client import generate_text

SYSTEM = """
You are FitBuddy's nutrition and recovery assistant. Give concise, general wellness guidance,
not medical diagnosis or individualized medical nutrition treatment. Avoid unsafe dieting advice.
"""

def generate_nutrition_tip_with_flash(goal):
    prompt = f"""
Give one concise nutrition or recovery tip for a user whose fitness goal is "{goal}".
Keep it practical, evidence-informed, and easy to follow. Mention hydration, balanced meals,
protein/fiber, sleep, or recovery only when relevant. Maximum 120 words.
"""
    return generate_text(TIP_MODEL, prompt, SYSTEM)
