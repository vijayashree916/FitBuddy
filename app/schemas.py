from pydantic import BaseModel, Field, field_validator

ALLOWED_GOALS = {"weight loss", "muscle gain", "general wellness", "flexibility", "endurance"}
ALLOWED_INTENSITIES = {"low", "medium", "high"}

class UserInput(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    user_id: str = Field(min_length=2, max_length=100, pattern=r"^[A-Za-z0-9_-]+$")
    age: int = Field(ge=18, le=100)
    weight: float = Field(gt=20, le=400)
    goal: str
    intensity: str

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, value):
        value = value.strip().lower()
        if value not in ALLOWED_GOALS:
            raise ValueError(f"Goal must be one of: {', '.join(sorted(ALLOWED_GOALS))}")
        return value

    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value):
        value = value.strip().lower()
        if value not in ALLOWED_INTENSITIES:
            raise ValueError("Intensity must be low, medium, or high")
        return value

class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=2, max_length=100)
    feedback: str = Field(min_length=3, max_length=1000)
