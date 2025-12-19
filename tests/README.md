# Tests

This directory contains unit tests for the FastAPI application.

## Running Tests Locally

1. Install main application dependencies:
```bash
pip install -r requirements.txt
```

2. Install test dependencies:
```bash
pip install -r requirements-test.txt
```

3. Run tests:
```bash
export $(cat .env.test | xargs)
pytest tests/ -v
```

## CI/CD

Tests are automatically run on every push to any branch via GitHub Actions.
See `.github/workflows/test.yml` for the workflow configuration.

## Test Requirements

Tests require the following environment variables:
- `DATABASE_URL` - Database connection string (SQLite for tests)
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (default: HS256)

These are defined in `.env.test` and automatically loaded during test execution.
