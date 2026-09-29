# FitBuddy Project Phases

This directory organizes the FitBuddy project lifecycle into eight phases. The complete
runnable application is inside `05-project-development/`, with its backend in `app/`,
templates in `templates/`, static assets in `static/`, and tests in `tests/`.

1. [Brainstorming & Ideation](01-brainstorming-ideation/README.md)
2. [Requirement Analysis](02-requirement-analysis/README.md)
3. [Project Design](03-project-design/README.md)
4. [Project Planning](04-project-planning/README.md)
5. [Project Development](05-project-development/README.md)
6. [Project Testing](06-project-testing/README.md)
7. [Project Documentation](07-project-documentation/README.md)
8. [Project Demonstration](08-project-demonstration/README.md)

## How to run the project

Run these commands from the repository root in Windows PowerShell:

```powershell
cd project-phases/05-project-development
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and configure `GEMINI_API_KEY`, `ADMIN_PASSWORD`, and `SESSION_SECRET`.
Keep `.env` private; it must not be pushed to GitHub.

Start the development server:

```powershell
uvicorn app.main:app --reload
```

Open these URLs in a browser:

- Application: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs
- Admin login: http://127.0.0.1:8000/admin-login
- Health check: http://127.0.0.1:8000/health

Run the automated tests from the same development directory:

```powershell
python -m pytest -q
```
