from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import profile
from pathlib import Path

# Initialize the main FastAPI application
app = FastAPI(
    title="Career Forge: MVP Development",
    description="The API for the Career Forge AI Analysis Engine.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes are all under /api/v1
app.include_router(profile.router, prefix="/api/v1", tags=["Analysis"])

# Build a reliable, absolute path to the frontend file
FRONTEND_FILE_PATH = Path(__file__).resolve().parent.parent.parent / "frontend" / "public" / "index.html"

@app.get("/", response_class=FileResponse, include_in_schema=False)
def read_root():
    """Serves the main frontend application."""
    if not FRONTEND_FILE_PATH.is_file():
        raise HTTPException(status_code=404, detail="Frontend file not found at: " + str(FRONTEND_FILE_PATH))
    return FileResponse(FRONTEND_FILE_PATH)
# frontend file path is returned