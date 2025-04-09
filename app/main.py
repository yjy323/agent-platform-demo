"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router

app = FastAPI(
    title="AI Co-Pilot",
    description="AI Co-Pilot API server",
    version="0.1.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(chat_router, tags=["chat"])


# Serve index.html at root
@app.get("/", response_class=HTMLResponse)  # type: ignore[misc]
async def root() -> str:
    """Serve the index.html file."""
    with open("app/static/index.html", "r") as f:
        return f.read()
