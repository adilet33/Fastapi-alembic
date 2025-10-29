# Tests

This directory contains unit tests for the FastAPI application.

## Running Tests Locally

1. Install test dependencies:
```bash
pip install -r requirements-test.txt
```

2. Run tests:
```bash
pytest tests/ -v
```

## CI/CD

Tests are automatically run on every push to any branch via GitHub Actions.
See `.github/workflows/test.yml` for the workflow configuration.

## Test Requirements

Tests require the following environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (default: HS256)

These are automatically set in the test configuration.
