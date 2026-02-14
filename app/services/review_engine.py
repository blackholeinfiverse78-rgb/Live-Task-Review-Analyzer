"""
Task Review AI - Modular Engine v2.1
Updated on: 2026-02-05
Logic: Modular Deterministic Rule Evaluators
"""
from ..models.schemas import Task, ReviewOutput, Analysis, Meta
from ..core.interfaces.review_engine_interface import ReviewEngineInterface
import logging
import time

logger = logging.getLogger("task_review_system")

# Evaluation Settings
DETERMINISTIC_MODE = True
FIXED_EVAL_TIME = 120

import json
import re

class ReviewEngine(ReviewEngineInterface):
    def evaluate(self, task: dict) -> dict:
        """
        Adapter method to satisfy ReviewEngineInterface.
        """
        task_obj = Task(**task)
        result = self.review_task(task_obj)
        return result.model_dump()

    @staticmethod
    def _parse_context(description: str) -> dict:
        """Extracts structured components from the combined description string."""
        context = {
            "description": "",
            "repo_metrics": {},
            "pdf_text": ""
        }
        
        # Split by known markers (flexible whitespace)
        # Using [ \t]* around newlines and markers
        marker_pattern = r"(?:\r?\n)+[ \t]*--- (GitHub Repository Metrics|Extracted PDF Content) ---[ \t]*(?:\r?\n)+"
        parts = re.split(marker_pattern, description)
        
        # parts[0] is the main description
        context["description"] = parts[0].strip()
        
        # Iterate through markers and content
        for i in range(1, len(parts), 2):
            marker = parts[i]
            content = parts[i+1].strip() if i+1 < len(parts) else ""
            
            if marker == "GitHub Repository Metrics":
                try:
                    context["repo_metrics"] = json.loads(content)
                except Exception as e:
                    logger.warning(f"Failed to parse repo metrics from context: {e}")
                    context["repo_metrics"] = {}
            elif marker == "Extracted PDF Content":
                context["pdf_text"] = content
        
        logger.debug(f"Parsed context: Desc Length={len(context['description'])}, "
                     f"Repo Metrics Keys={list(context['repo_metrics'].keys())}, "
                     f"PDF Text Length={len(context['pdf_text'])}")
                
        return context

    @staticmethod
    def _score_pdf(text: str) -> tuple[int, list]:
        """PDF Scoring (40 points max)"""
        if not text:
            return 0, ["No PDF content provided."]
        
        score = 0
        reasons = []
        words = text.split()
        word_count = len(words)
        logger.info(f"PDF Analysis: Word count = {word_count}")
        
        # 1. Word Count (30 pts)
        if word_count >= 500:
            score += 30
        elif word_count >= 100:
            score += 20
        elif word_count >= 20:
            score += 10
        else:
            reasons.append("PDF content too brief.")

        # 2. Structured Headings Detection (10 pts)
        # Look for lines starting with # or lines that are all caps and > 5 chars
        has_headings = any(
            line.strip().startswith('#') or 
            (line.strip().isupper() and len(line.strip()) > 5) 
            for line in text.split('\n')
        )
        if has_headings:
            score += 10
        else:
            reasons.append("Missing structured headings in PDF.")
            
        return score, reasons

    @staticmethod
    def _score_repo(metrics: dict) -> tuple[int, list]:
        """Repo Scoring (40 points max)"""
        if not metrics:
            return 0, ["No repository metrics provided."]
        
        score = 0
        reasons = []
        
        # README (10 pts)
        if metrics.get("has_readme"):
            score += 10
        else:
            reasons.append("Missing README file.")
            
        # Tests (10 pts)
        if metrics.get("has_tests"):
            score += 10
        else:
            reasons.append("Missing tests directory.")
            
        # Commits (10 pts)
        if metrics.get("commit_count", 0) > 10:
            score += 10
        else:
            reasons.append("Low commit history (< 10 commits).")
            
        # Structure (10 pts)
        if metrics.get("file_count", 0) > 15:
            score += 10
        else:
            reasons.append("Sparse repository structure.")
            
        return score, reasons

    @staticmethod
    def _score_description(text: str) -> tuple[int, list]:
        """Description Scoring (20 points max)"""
        if not text or len(text) < 10:
            return 0, ["Description too short."]
        
        score = 0
        reasons = []
        
        # 1. Length Threshold (10 pts)
        if len(text) >= 200:
            score += 10
        elif len(text) >= 50:
            score += 5
        else:
            reasons.append("Description needs more detail.")
            
        # 2. Objective Keywords (10 pts)
        description_lower = text.lower()
        if any(k in description_lower for k in ["objective", "goal", "purpose", "requirement"]):
            score += 10
        else:
            reasons.append("Missing clear objectives/requirements.")
            
        return score, reasons

    @classmethod
    def review_task(cls, task: Task) -> ReviewOutput:
        """
        Pure deterministic review processor. Same Input -> Same Output.
        """
        start_time = time.time()
        
        # Parse context from combined description
        context = cls._parse_context(task.task_description)
        
        pdf_score, pdf_reasons = cls._score_pdf(context["pdf_text"])
        repo_score, repo_reasons = cls._score_repo(context["repo_metrics"])
        desc_score, desc_reasons = cls._score_description(context["description"])
        
        final_score = pdf_score + repo_score + desc_score
        logger.info(f"Score Breakdown: PDF={pdf_score}/40, Repo={repo_score}/40, Desc={desc_score}/20 | Total={final_score}/100")
        
        failure_reasons = pdf_reasons + repo_reasons + desc_reasons
        
        # Filter failure reasons to only keep the most critical ones if list is too long
        failure_reasons = [r for r in failure_reasons if r]
        
        # Calculate Readiness
        readiness = int(final_score * 0.9) if final_score < 95 else final_score
        
        # Status Mapping
        if final_score >= 80:
            status = "pass"
        elif final_score >= 50:
            status = "borderline"
        else:
            status = "fail"

        # Analysis Normalization (0-100)
        analysis = Analysis(
            technical_quality=int((repo_score / 40) * 100) if repo_score > 0 else 0,
            clarity=int((desc_score / 20) * 100) if desc_score > 0 else 0,
            discipline_signals=int((pdf_score / 40) * 100) if pdf_score > 0 else 0
        )
        
        # Meta calculation (deterministic eval time)
        meta = Meta(
            evaluation_time_ms=FIXED_EVAL_TIME,
            mode="rule"
        )

        return ReviewOutput(
            score=final_score,
            readiness_percent=readiness,
            status=status,
            failure_reasons=failure_reasons[:5], # Top 5 reasons
            improvement_hints=[
                "Ensure PDF contains structured headings.",
                "Maintain a commit history > 10.",
                "Define clear objectives in your description."
            ] if final_score < 90 else [],
            analysis=analysis,
            meta=meta
        )
