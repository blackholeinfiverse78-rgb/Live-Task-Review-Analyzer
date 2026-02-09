"""
Task Review AI - Production Maintenance Mode
Updated on: 2026-02-05
Version: 1.1.1
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .api import task_submit, task_review, next_task
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("task_review_system")

app = FastAPI(
    title="Task Review AI - Production Demo",
    description="Deterministic Engineering Task Analysis System (Locked)",
    version="1.1.0"
)

# Security: CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restricted for production, but allowed for demo flexibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Invalid Input Data",
            "errors": [f"{e['loc'][-1]}: {e['msg']}" for e in exc.errors()]
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.critical(f"FATAL: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "System encountered an error. Please contact the demo team."}
    )

app.include_router(task_submit.router, prefix="/api/v1/task", tags=["PROD"])
app.include_router(task_review.router, prefix="/api/v1/task", tags=["PROD"])
app.include_router(next_task.router, prefix="/api/v1/task", tags=["PROD"])

@app.get("/")
async def root():
    return {
        "message": "Task Review AI Backend is Online",
        "documentation": "/docs",
        "health": "/health",
        "version": "1.1.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
