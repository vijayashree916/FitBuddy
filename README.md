# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 web application that uses Gemini to generate a personalized
7-day workout plan, a concise nutrition/recovery tip, and revised plans from user feedback.
SQLite + SQLAlchemy store users and original/updated plans.

## Project phases

The project lifecycle is organized in [project-phases/README.md](project-phases/README.md):

1. Brainstorming & Ideation
2. Requirement Analysis
3. Project Design
4. Project Planning
5. Project Development
6. Project Testing
7. Project Documentation
8. Project Demonstration

## Architecture

Browser → FastAPI/Jinja2 → Gemini AI
                    ↓
               SQLite/SQLAlchemy

Main routes:
- `GET /` – user form
- `POST /generate-workout` – generate and store plan
- `POST /submit-feedback` – revise an existing plan
- `GET /admin-login` – admin login
- `GET /view-all-users` – protected admin dashboard
- `GET /docs` – FastAPI Swagger documentation
- `GET /health` – health check

JSON APIs:
- `POST /api/generate-workout`
- `POST /api/submit-feedback`
- `GET /api/users`

## Setup

The runnable project is in `project-phases/05-project-development/`. Run the setup and
application commands from that directory.

### Windows PowerShell

```powershell
cd project-phases/05-project-development
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and set `GEMINI_API_KEY` and a strong `ADMIN_PASSWORD`.

Run:

```powershell
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/admin-login

### Windows CMD

```cmd
cd project-phases\05-project-development
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

### macOS / Linux

```bash
cd project-phases/05-project-development
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Testing

The test suite uses a fake Gemini layer, so it does not require a real API call.

```bash
cd project-phases/05-project-development
python -m pytest -q
```

For a live Gemini test, configure `.env`, start the server, submit the form, and verify
that a 7-day plan and nutrition tip appear.

## Notes

The original project documentation describes Gemini 1.5 Pro and Gemini Flash and the
`google-generativeai` package. This implementation keeps the same architectural roles but
uses the newer `google-genai` SDK. Model names are environment variables so they can be
changed without editing application code.

FitBuddy is an educational/general fitness application. It should not be treated as a
medical service.
