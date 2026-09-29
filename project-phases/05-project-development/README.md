# Phase 5: Project Development

This directory contains the complete runnable FitBuddy project. Run commands from this
directory so Python imports and relative database paths resolve correctly.

The implementation is organized as follows:

- Backend: `app/`
- HTML templates: `templates/`
- Static assets: `static/`
- Configuration template: `.env.example`
- Dependencies: `requirements.txt`
- Runtime entrypoint: `app.main:app`
- Tests: `tests/`

## Run the application
```powershell
cd project-phases/05-project-development
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in a browser.

## Security boundary
Keep `.env` local. It contains secrets and is excluded by `.gitignore`.

## Run tests

```powershell
python -m pytest -q
```
