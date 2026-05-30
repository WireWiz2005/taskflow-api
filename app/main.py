from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.routers import auth_router, tasks_router, users_router

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="""
A secure REST API for managing personal tasks with JWT authentication.

## Features
- Register a new account
- Login and receive a JWT token
- Create, read, update, and delete your own tasks
- Access only the task records owned by your account
    """,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(tasks_router.router)
app.include_router(users_router.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "TaskFlow API is running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "environment": settings.environment}
