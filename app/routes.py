from pathlib import Path
from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool

from .config import ADMIN_PASSWORD
from .database import (
    get_db, save_user, save_plan, get_user, get_original_plan,
    update_plan, get_all_users, delete_user
)
from .schemas import UserInput, FeedbackRequest
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
router = APIRouter()

def render_error(request, message, status_code=400):
    return templates.TemplateResponse(
        request,
        "error.html",
        {"request": request, "message": message},
        status_code=status_code,
    )

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = UserInput(
            username=username, user_id=user_id, age=age, weight=weight,
            goal=goal, intensity=intensity
        )
        user = save_user(db, **data.model_dump())
        workout = await run_in_threadpool(
            generate_workout_gemini,
            data.username, data.age, data.weight, data.goal, data.intensity
        )
        tip = await run_in_threadpool(generate_nutrition_tip_with_flash, data.goal)
        plan = save_plan(db, user, workout, tip)
        return templates.TemplateResponse(
            request,
            "result.html",
            {
                "request": request,
                "user": user,
                "plan": plan,
                "display_plan": plan.original_plan,
                "is_updated": False,
            },
        )
    except ValidationError as exc:
        return render_error(request, str(exc), 422)
    except Exception as exc:
        return render_error(request, f"Could not generate the plan: {exc}", 500)

@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = FeedbackRequest(user_id=user_id, feedback=feedback)
        plan = get_original_plan(db, data.user_id)
        if not plan:
            return render_error(request, "No plan was found for this user.", 404)

        user = plan.user
        base_plan = plan.updated_plan or plan.original_plan
        revised = await run_in_threadpool(
            update_workout_plan, base_plan, data.feedback, user.goal, user.intensity
        )
        update_plan(db, plan, revised, data.feedback)

        return templates.TemplateResponse(
            request,
            "result.html",
            {
                "request": request,
                "user": user,
                "plan": plan,
                "display_plan": revised,
                "is_updated": True,
            },
        )
    except ValidationError as exc:
        return render_error(request, str(exc), 422)
    except Exception as exc:
        return render_error(request, f"Could not update the plan: {exc}", 500)

@router.get("/admin-login", response_class=HTMLResponse)
def admin_login(request: Request):
    return templates.TemplateResponse(request, "admin_login.html", {"request": request})

@router.post("/admin-login")
def admin_login_submit(request: Request, password: str = Form(...)):
    if password != ADMIN_PASSWORD:
        return templates.TemplateResponse(
            request,
            "admin_login.html",
            {"request": request, "error": "Invalid admin password."},
            status_code=401,
        )
    request.session["is_admin"] = True
    return RedirectResponse("/view-all-users", status_code=303)

@router.get("/admin-logout")
def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

def require_admin(request: Request):
    if not request.session.get("is_admin"):
        raise HTTPException(status_code=303, headers={"Location": "/admin-login"})

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    users = get_all_users(db)
    return templates.TemplateResponse(
        request,
        "all_users.html",
        {"request": request, "users": users},
    )

@router.post("/admin/delete-user/{user_id}")
def admin_delete_user(
    user_id: str,
    request: Request,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    delete_user(db, user_id)
    return RedirectResponse("/view-all-users", status_code=303)

# JSON API endpoints for API testing / future frontend clients.
@router.post("/api/generate-workout")
async def api_generate_workout(data: UserInput, db: Session = Depends(get_db)):
    user = save_user(db, **data.model_dump())
    workout = await run_in_threadpool(
        generate_workout_gemini,
        data.username, data.age, data.weight, data.goal, data.intensity
    )
    tip = await run_in_threadpool(generate_nutrition_tip_with_flash, data.goal)
    plan = save_plan(db, user, workout, tip)
    return {
        "user_id": user.user_id,
        "plan_id": plan.id,
        "workout_plan": workout,
        "nutrition_tip": tip,
    }

@router.post("/api/submit-feedback")
async def api_submit_feedback(data: FeedbackRequest, db: Session = Depends(get_db)):
    plan = get_original_plan(db, data.user_id)
    if not plan:
        raise HTTPException(status_code=404, detail="User plan not found")
    user = plan.user
    base_plan = plan.updated_plan or plan.original_plan
    revised = await run_in_threadpool(
        update_workout_plan, base_plan, data.feedback, user.goal, user.intensity
    )
    update_plan(db, plan, revised, data.feedback)
    return {
        "user_id": user.user_id,
        "plan_id": plan.id,
        "updated_plan": revised,
        "feedback": data.feedback,
    }

@router.get("/api/users")
def api_users(db: Session = Depends(get_db)):
    return [
        {
            "user_id": u.user_id,
            "username": u.username,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
            "created_at": u.created_at,
            "plans": len(u.plans),
        }
        for u in get_all_users(db)
    ]

@router.get("/health")
def health():
    return {"status": "ok", "service": "FitBuddy"}
