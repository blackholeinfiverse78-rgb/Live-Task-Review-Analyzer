from fastapi import APIRouter, HTTPException, Form, File, UploadFile, Request, Depends
from typing import Optional
import logging
from ..models.schemas import Task, ReviewOutput, TaskCreate
from ..models.storage import task_storage

from ..services.review_orchestrator import ReviewOrchestrator
from ..core.dependencies import get_review_orchestrator

router = APIRouter()
logger = logging.getLogger("task_review_system")

@router.post("/review", response_model=ReviewOutput)
async def review_task(
    request: Request,
    task_id: Optional[str] = Form(None),
    payload: Optional[str] = Form(None),
    github_url: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    pdf_file: Optional[UploadFile] = File(None),
    orchestrator: ReviewOrchestrator = Depends(get_review_orchestrator)
):
    try:
        target_task = None
        
        # 1. Handle JSON Backward Compatibility
        content_type = request.headers.get("content-type", "")
        if "application/json" in content_type:
            try:
                body = await request.json()
                task_id = body.get("task_id")
                raw_payload = body.get("payload")
                if raw_payload:
                    p = TaskCreate(**raw_payload)
                    # For JSON ad-hoc, we route directly to process_submission (legacy path)
                    # We create a transient task
                    import uuid
                    from datetime import datetime
                    target_task = Task(
                        task_id="adhoc-" + str(uuid.uuid4())[:8],
                        task_title=p.task_title,
                        task_description=p.task_description,
                        submitted_by=p.submitted_by,
                        timestamp=datetime.now()
                    )
                    orchestration_res = orchestrator.process_submission(target_task)
                    return orchestration_res.review
            except Exception as e:
                logger.error(f"JSON parsing failed: {str(e)}")
                raise HTTPException(status_code=422, detail="Invalid JSON body")

        # 2. Handle Task ID (from Form)
        if task_id:
            entry = task_storage.get(task_id)
            if not entry:
                raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
            
            target_task = entry["task"] if isinstance(entry, dict) else entry
            orchestration_res = orchestrator.process_submission(target_task)
            return orchestration_res.review

        # 3. Handle Ad-hoc Form Payload
        if payload:
            import json
            import uuid
            from datetime import datetime
            try:
                p_dict = json.loads(payload)
                p = TaskCreate(**p_dict)
                target_task = Task(
                    task_id="adhoc-" + str(uuid.uuid4())[:8],
                    task_title=p.task_title,
                    task_description=p.task_description,
                    submitted_by=p.submitted_by,
                    timestamp=datetime.now()
                )
                orchestration_res = orchestrator.process_submission(target_task)
                return orchestration_res.review
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid payload format in form")

        # 4. Handle Extended Review (GitHub / PDF / Description)
        if github_url or pdf_file or description:
            # We must have a description if github is present (validation handled in orchestrator or schemas)
            orchestration_res = orchestrator.orchestrate_review(
                description=description,
                github_url=github_url,
                pdf_file=pdf_file
            )
            return orchestration_res.review

        raise HTTPException(status_code=400, detail="Insufficient input provided.")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Review execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Review process failed: {str(e)}")
