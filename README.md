# FastAPI with Alembic

A FastAPI application with PostgreSQL database and Alembic migrations for managing user authentication and task management.

## Features

- User authentication with JWT tokens
- Task management system
- PostgreSQL database with async SQLAlchemy
- Database migrations with Alembic
- Token blacklisting for logout functionality

## Prerequisites

Before running this application, make sure you have:

- Python 3.9 or higher
- PostgreSQL database server
- pip (Python package manager)

## Dependencies

The application uses the following main dependencies:

- **FastAPI** (0.111.0) - Modern web framework for building APIs
- **Uvicorn** (0.30.1) - ASGI server for running the application
- **SQLAlchemy** (2.0.31) - SQL toolkit and ORM
- **Alembic** (1.13.2) - Database migration tool
- **asyncpg** (0.29.0) - PostgreSQL adapter for async operations
- **Pydantic** (2.7.4) - Data validation using Python type annotations
- **python-jose** (3.3.0) - JWT token handling
- **passlib** (1.7.4) - Password hashing
- **python-decouple** (3.8) - Environment variable management

For a complete list of dependencies, see `requirements.txt`.

## Environment Variables

Create a `.env` file in the root directory of the project with the following variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database_name
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

You can copy the `.env.example` file as a starting point:
```bash
cp .env.example .env
```

Then edit the `.env` file with your actual configuration values.

### Environment Variable Descriptions

- **DATABASE_URL**: PostgreSQL connection string in the format `postgresql+asyncpg://username:password@host:port/database_name`
  - `username`: Your PostgreSQL username
  - `password`: Your PostgreSQL password
  - `host`: Database host (usually `localhost` for local development)
  - `port`: PostgreSQL port (default is `5432`)
  - `database_name`: Name of your database

- **SECRET_KEY**: A secure random string used for JWT token encryption. You can generate one using:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

- **ALGORITHM**: JWT algorithm to use (default is `HS256`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/adilet33/Fastapi-alembic.git
cd Fastapi-alembic
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database:
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE your_database_name;
```

5. Create a `.env` file with your configuration (see Environment Variables section above)

## Database Migrations

This project uses Alembic for database migrations.

### Run migrations

To apply all pending migrations to your database:

```bash
alembic upgrade head
```

### Create a new migration

If you make changes to the models, create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Downgrade migrations

To rollback the last migration:

```bash
alembic downgrade -1
```

To rollback to a specific revision:

```bash
alembic downgrade <revision_id>
```

### View migration history

```bash
alembic history
```

## Running the Application

### Development Mode

Run the application with auto-reload enabled:

```bash
uvicorn app.main:app --reload
```

Or specify host and port:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

For production, run without the `--reload` flag:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
Fastapi-alembic/
├── alembic/                 # Alembic migrations directory
│   ├── versions/           # Migration files
│   └── env.py             # Alembic environment configuration
├── app/
│   ├── database/          # Database connection and configuration
│   ├── models/            # SQLAlchemy models
│   ├── routes/            # API route handlers
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── repository/        # Database operations
│   ├── exceptions/        # Custom exceptions
│   ├── config.py          # Application configuration
│   └── main.py           # FastAPI application entry point
├── alembic.ini            # Alembic configuration
├── requirements.txt       # Python dependencies
└── .env                  # Environment variables (create this)
```

## Available Endpoints

- `GET /` - Hello world endpoint
- Authentication endpoints (under `/auth`)
- Task management endpoints (under `/task`)

For complete API documentation, visit the Swagger UI at `/docs` after starting the application.

## Development

### Code Style

This project follows PEP 8 style guidelines. Consider using tools like:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

### Testing

(Add testing instructions here when tests are implemented)

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check your `DATABASE_URL` in `.env` file
- Ensure the database exists and credentials are correct

### Migration Issues

- If migrations fail, check the database connection
- Ensure you're in the correct directory with `alembic.ini`
- Try running `alembic current` to see the current revision

### Import Errors

- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## License

(Add license information here)

## Contributing

(Add contribution guidelines here)
