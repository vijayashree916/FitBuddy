# Phase 3: Project Design

## Architecture

```text
Browser or API client
        |
FastAPI routes and validation
        |
Gemini generators + SQLAlchemy persistence
        |
SQLite database
```

## Main components
- `app/main.py`: FastAPI setup, middleware, static files, and startup.
- `app/routes.py`: HTML and JSON route handlers.
- `app/schemas.py`: request validation.
- `app/database.py`: models and persistence.
- `app/gemini_*.py`: AI generation services.
- `templates/`: Jinja2 views.
- `static/`: CSS and images.

## Output
A maintainable component boundary and request-to-response flow.
