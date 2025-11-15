"""
Application entry point
Run with: python run.py
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,  # Set to False in production
        log_level="info"
    )
