from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="A2A Assistant API",
    description="API for Assistant-to-Assistant interaction using Gemini and OpenAI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://167.172.160.167:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Welcome to A2A Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "/api/a2a": "POST - Interact with A2A assistants"
        }
    } 