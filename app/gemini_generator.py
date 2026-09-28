from .config import WORKOUT_MODEL
from .gemini_client import generate_text

SYSTEM = """
You are FitBuddy, a fitness-planning assistant. Create safe, practical, beginner-friendly
fitness plans. Do not diagnose medical conditions or prescribe treatment. Avoid extreme
calorie restriction, dangerous exercises, or unsafe claims. Encourage users with injuries,
medical conditions, pregnancy, or unusual symptoms to consult a qualified professional.
Return plain text with clear headings; do not use markdown tables.
"""

def generate_workout_gemini(username, age, weight, goal, intensity):
    prompt = f"""
Create a personalized 7-day workout plan for:
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Preferred intensity: {intensity}

Requirements:
- Cover Day 1 through Day 7.
- Each day must contain: Warm-up (5–10 min), Main Workout, and Cooldown/Recovery.
- Include exercise names and practical sets/reps or time.
- Include rest/recovery where appropriate.
- Match volume and intensity to the requested level.
- Keep the plan realistic for a general adult user.
- Add a short "Safety note" at the end.
"""
    return generate_text(WORKOUT_MODEL, prompt, SYSTEM)
