# TaskFlow API

TaskFlow API is a secure task management backend built with FastAPI. It supports account creation, JWT-based login, and user-scoped task management so each user can only access their own tasks.

This project is designed as a resume-ready backend portfolio piece: it includes authentication, input validation, database models, automated tests, Docker support, and Render deployment configuration.

## Features

- User registration and login
- JWT access tokens with configurable expiry
- Bcrypt password hashing
- Protected task CRUD endpoints
- User-level data isolation
- Pydantic request validation
- SQLAlchemy ORM models
- SQLite for local development
- PostgreSQL-ready deployment configuration
- Interactive OpenAPI docs at `/docs`
- Test coverage for auth, task CRUD, and access control

## Tech Stack

| Layer | Technology |
| --- | --- |
| API framework | FastAPI |
| Database ORM | SQLAlchemy |
| Local database | SQLite |
| Production database | PostgreSQL |
| Validation | Pydantic v2 |
| Authentication | JWT with python-jose |
| Password hashing | passlib + bcrypt |
| Testing | pytest + FastAPI TestClient |
| Deployment | Render, Docker |

## Project Structure

```text
taskflow-api/
├── app/
│   ├── config.py              # Environment-based settings
│   ├── database.py            # SQLAlchemy engine and DB sessions
│   ├── auth.py                # Password hashing and JWT helpers
│   ├── main.py                # FastAPI app setup
│   ├── models/
│   │   ├── models.py          # SQLAlchemy User and Task models
│   │   └── schemas.py         # Pydantic request/response schemas
│   └── routers/
│       ├── auth_router.py     # Register and login endpoints
│       ├── tasks_router.py    # Task CRUD endpoints
│       └── users_router.py    # Current-user profile endpoint
├── tests/
│   └── test_api.py            # API behavior tests
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── Procfile
├── requirements.txt
└── .env.example
```

## API Endpoints

| Method | Endpoint | Auth Required | Description |
| --- | --- | --- | --- |
| GET | `/` | No | Root health message |
| GET | `/health` | No | Health check |
| POST | `/auth/register` | No | Create a new user |
| POST | `/auth/login` | No | Login and receive a JWT |
| GET | `/users/me` | Yes | Get current user profile |
| POST | `/tasks/` | Yes | Create a task |
| GET | `/tasks/` | Yes | List current user's tasks |
| GET | `/tasks/{task_id}` | Yes | Get one owned task |
| PATCH | `/tasks/{task_id}` | Yes | Update one owned task |
| DELETE | `/tasks/{task_id}` | Yes | Delete one owned task |

## Local Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate it:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create your environment file:

```bash
copy .env.example .env
```

5. Run the API:

```bash
uvicorn app.main:app --reload
```

Open:

- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## Running Tests

```bash
pytest
```

## Docker Setup

Run the API with PostgreSQL:

```bash
docker compose up --build
```

The API will be available at:

```text
http://127.0.0.1:8000/docs
```

## Render Deployment

This repo includes `render.yaml`, so the simplest deployment path is Render Blueprint deployment.

1. Push the project to GitHub.
2. In Render, create a new Blueprint from the repository.
3. Render will create:
   - a Python web service named `taskflow-api`
   - a PostgreSQL database named `taskflow-db`
   - generated `SECRET_KEY`
   - production `DATABASE_URL`
4. After deploy, open:

```text
https://your-render-service.onrender.com/docs
```

If deploying manually instead of using the blueprint:

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Required environment variables:

```text
ENVIRONMENT=production
DATABASE_URL=your_postgres_database_url
SECRET_KEY=your_long_random_secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Resume Description

**TaskFlow API - Secure Task Management Backend**

Built a production-ready FastAPI backend with JWT authentication, bcrypt password hashing, SQLAlchemy data models, protected user-scoped CRUD endpoints, automated API tests, Docker support, and Render deployment configuration.

## Suggested Resume Bullet

- Built TaskFlow API, a secure FastAPI task management backend with JWT auth, bcrypt password hashing, SQLAlchemy ORM models, protected user-scoped CRUD operations, pytest coverage, Docker support, and PostgreSQL-ready cloud deployment.
