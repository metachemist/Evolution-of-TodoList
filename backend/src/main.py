import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import AsyncGenerator
from src.database import get_db_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.utils.helpers import create_error_response
from fastapi.responses import JSONResponse

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for FastAPI application.
    Used for startup and shutdown events.
    """
    # Startup
    print("Starting up the application...")
    
    # Yield control to the application
    yield
    
    # Shutdown
    print("Shutting down the application...")


# Create FastAPI app with lifespan and metadata
app = FastAPI(
    title="Todo API",
    description="Multi-User Todo REST API with FastAPI, SQLModel, and Neon PostgreSQL",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for consistent responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler to ensure consistent error responses.
    """
    error_response = create_error_response(
        code="INTERNAL_ERROR",
        message="An internal server error occurred",
        details={
            "type": type(exc).__name__,
            "message": str(exc)
        } if hasattr(exc, '__str__') else {}
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    HTTP exception handler for consistent error responses.
    """
    error_response = create_error_response(
        code="HTTP_ERROR",
        message=exc.detail,
        details={
            "status_code": exc.status_code
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Todo API"}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "message": "API is running"}


# Include routers
def include_routers():
    """
    Function to include all routers to avoid circular imports.
    """
    from src.routes.tasks import router as tasks_router
    from src.routes.auth import router as auth_router
    app.include_router(tasks_router, prefix="/api/{user_id}", tags=["tasks"])
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


# Call the function to include routers
include_routers()