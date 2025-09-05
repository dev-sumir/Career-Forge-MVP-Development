# career_forge/api/main.py

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles # <-- NEW IMPORT
from .endpoints import profile
import os

# Initialize the main FastAPI application
app = FastAPI(
    title="Career Forge: MVP Development",
    description="The API for the Career Forge AI Analysis Engine.",
    version="1.0.0",
    # Hide the default /docs and /redoc URLs from the public
    docs_url=None, 
    redoc_url=None
)

# --- KEY CHANGE IS HERE ---
# First, we define our API routes. They must come before the static files mount.
app.include_router(profile.router, prefix="/api/v1", tags=["Analysis"])

# Second, we mount the 'public' directory to the root path.
# This tells FastAPI to serve files like index.html, style.css, and script.js.
# The `html=True` part makes it automatically serve index.html for the root URL.
app.mount("/", StaticFiles(directory="frontend/public", html=True), name="static")