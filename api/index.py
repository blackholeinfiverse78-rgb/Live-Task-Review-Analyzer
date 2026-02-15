import sys
import os

# 1. Add root to path so 'app.main' can be found
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 2. Import the FastAPI instance
# Vercel automatically detects 'app' and treats it as a FastAPI/Flask instance
try:
    from app.main import app
except ImportError as e:
    print(f"CRITICAL IMPORT ERROR: {e}")
    from fastapi import FastAPI
    app = FastAPI()
    @app.get("/health")
    async def health():
        return {"status": "error", "detail": str(e)}

# DO NOT define 'handler = app' here. 
# Defining 'handler' as an instance causes the 'issubclass' crash in Vercel's runtime.
