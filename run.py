"""
NeuralPhish AI - Application Server Launcher
Runs the FastAPI application which serves both the API endpoints and the built React frontend.
"""
import os
import sys
from pathlib import Path
import uvicorn

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    reload = os.environ.get("RELOAD", "false").lower() in ("true", "1", "yes")

    print(f"==================================================")
    print(f"  NeuralPhish AI Server Starting")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Documentation: http://localhost:{port}/docs")
    print(f"  Frontend: http://localhost:{port}/")
    print(f"==================================================")

    uvicorn.run(
        "backend.api.main:app",
        host=host,
        port=port,
        reload=reload
    )

if __name__ == "__main__":
    main()
