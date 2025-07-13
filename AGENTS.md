# Repository Guidelines

This project contains a FastAPI backend under `backend` and a React frontend under `frontend`.
The backend exposes asynchronous endpoints with error handling and uses a
`pydantic-settings` powered configuration module. Unit tests cover the report
routes and helper utilities.

## Pre-commit checks
- Run `pytest` from the `backend` folder.
- Run `npm run lint` from the `frontend` folder.

## Pull request notes
- Describe the main changes and confirm tests pass.
- Update `README.md` with any significant feature additions or removals.
