import os
os.environ["GEMINI_API_KEY"] = "test-key"
os.environ["ADMIN_PASSWORD"] = "admin123"
os.environ["SESSION_SECRET"] = "test-secret"

from fastapi.testclient import TestClient
from app.main import app
import app.routes as routes

def fake_workout(*args):
    return "Day 1: Warm-up\nMain Workout: Squats 3x10\nCooldown: 5 min\nDay 2: Rest"

def fake_tip(*args):
    return "Stay hydrated and include balanced protein and fiber-rich foods."

def fake_update(*args):
    return "Updated Day 1: Cardio + strength\nDay 2: Rest\nSafety note: Progress gradually."

def test_home():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "FitBuddy" in response.text

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_generate_and_feedback(monkeypatch):
    monkeypatch.setattr(routes, "generate_workout_gemini", fake_workout)
    monkeypatch.setattr(routes, "generate_nutrition_tip_with_flash", fake_tip)
    monkeypatch.setattr(routes, "update_workout_plan", fake_update)

    with TestClient(app) as client:
        response = client.post("/generate-workout", data={
            "username": "Test User",
            "user_id": "test_user_001",
            "age": "25",
            "weight": "70",
            "goal": "muscle gain",
            "intensity": "medium",
        })
        assert response.status_code == 200
        assert "Day 1" in response.text

        response = client.post("/submit-feedback", data={
            "user_id": "test_user_001",
            "feedback": "Add more cardio",
        })
        assert response.status_code == 200
        assert "Updated Day 1" in response.text

def test_admin_login(monkeypatch):
    with TestClient(app) as client:
        response = client.post("/admin-login", data={"password": "wrong"})
        assert response.status_code == 401

        response = client.post("/admin-login", data={"password": "admin123"}, follow_redirects=False)
        assert response.status_code == 303
        assert response.headers["location"] == "/view-all-users"

        response = client.get("/view-all-users")
        assert response.status_code == 200
