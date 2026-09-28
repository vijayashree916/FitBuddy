from .config import WORKOUT_MODEL
from .gemini_client import generate_text

SYSTEM = """
You are FitBuddy. Revise an existing workout plan based on user feedback while keeping it safe,
realistic, and consistent with the user's original goal and intensity. Do not diagnose conditions.
If feedback requests something unsafe, replace it with a safer alternative and briefly explain why.
Return the complete revised 7-day plan, not only the changed day.
"""

def update_workout_plan(original_plan, feedback, goal, intensity):
    prompt = f"""
Original 7-day plan:
{original_plan}

User goal: {goal}
Intensity: {intensity}
User feedback:
{feedback}

Create the complete revised 7-day plan. Preserve useful parts of the original plan and apply
the feedback where reasonable. Include warm-up, main workout, cooldown/recovery, rest days
where appropriate, and a short safety note.
"""
    return generate_text(WORKOUT_MODEL, prompt, SYSTEM)
