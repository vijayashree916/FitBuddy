# Phase 5: Project Development

The implementation is organized as follows:

- Backend: `app/`
- HTML templates: `templates/`
- Static assets: `static/`
- Configuration template: `.env.example`
- Dependencies: `requirements.txt`
- Runtime entrypoint: `app.main:app`

## Run the application
```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in a browser.

## Security boundary
Keep `.env` local. It contains secrets and is excluded by `.gitignore`.
