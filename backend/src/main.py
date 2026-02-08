from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.db import create_db_and_tables
from src.routes.auth import router as auth_router
from src.routes.tasks import router as tasks_router
from src.mcp.server import router as mcp_router
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables on startup
    # Skip table creation if running tests to avoid async issues
    if not os.getenv("TESTING"):
        await create_db_and_tables()
    yield
    # Clean up on shutdown if needed


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"], # Add both ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tasks_router)
app.include_router(mcp_router)  # Include MCP tools router


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Evolution Backend!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)