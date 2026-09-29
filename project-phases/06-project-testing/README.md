# Phase 6: Project Testing

## Automated tests
The test suite covers:

- Home page rendering.
- Health endpoint response.
- Workout generation and feedback submission.
- Admin authentication and dashboard access.

Run the tests from the project root:

```powershell
python -m pytest -q
```

The test suite uses fake Gemini functions and does not require a live API key.

## Output
A repeatable regression check for the main user workflows.
