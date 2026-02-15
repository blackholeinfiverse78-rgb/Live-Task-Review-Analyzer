import sys
import os

# Ensure the project root is in the path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from app.main import app
except ImportError as e:
    print(f"Import Error: {e}")
    # Fallback/Diagnostic app
    from fastapi import FastAPI
    app = FastAPI()
    @app.get("/health")
    async def health():
        return {"status": "error", "message": str(e), "path": sys.path, "root": ROOT_DIR}

# Vercel looks for 'app' by default
handler = app
