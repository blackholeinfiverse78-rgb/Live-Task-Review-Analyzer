import sys
import os

# Ensure the root directory is in the python path
# This allows 'from app.main import app' to work
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    # Try importing the actual app
    from app.main import app
except Exception as e:
    # Diagnostic fallback app if the real app fails to load
    from fastapi import FastAPI
    import traceback
    
    app = FastAPI(title="Diagnostic Fallback")
    
    @app.get("/health")
    @app.get("/api/v1/task/health")
    async def health_diagnostic():
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc(),
            "sys_path": sys.path,
            "cwd": os.getcwd()
        }
    
    @app.get("/api/{rest_of_path:path}")
    async def api_fallback(rest_of_path: str):
        return {"error": "Main app failed to load", "detail": str(e)}

# Vercel looks for 'app' or 'handler'
handler = app
