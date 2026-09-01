from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import api_router
from app.exceptions.handlers import register_exception_handlers

app = FastAPI(
    title="FastAPI MSSQL Project",
    description="FastAPI project with MSSQL, authentication, and role-based access",
    version="1.0.0",
)


register_exception_handlers(app)

# Include routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI MSSQL Project"}


origins = [
    "http://localhost:5173",  # Vite
    "http://localhost:4173",  # CRA (if used)
    "http://analytics.local:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
