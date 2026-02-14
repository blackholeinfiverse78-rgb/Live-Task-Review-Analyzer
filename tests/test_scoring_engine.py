import pytest
from app.services.review_engine import ReviewEngine
from app.models.schemas import Task
from datetime import datetime
import textwrap

def test_deterministic_scoring_full():
    engine = ReviewEngine()
    
    # Combined description simulating PDF, Repo, and Description
    long_pdf_text = "Content " * 600 # 600 words
    description_content = textwrap.dedent(f"""\
        This is a high quality project description that explains the overall goals and objectives clearly. 
        It meets the length requirements easily because it is deliberately made to be very long and detailed.
        We want to ensure that it exceeds the 200 character threshold for maximum scoring in this category.
        Adding more substance to the description to make sure it captures all technical nuances of the proposed system architecture and implementation plan.
        
        --- GitHub Repository Metrics ---
        {{
            "has_readme": true,
            "has_tests": true,
            "commit_count": 25,
            "file_count": 30
        }}
        
        --- Extracted PDF Content ---
        # Executive Summary
        Objective: Implement a secure system.
        {long_pdf_text}
    """)
    
    task = Task(
        task_id="test-score-1",
        task_title="High Quality Submission",
        task_description=description_content,
        submitted_by="Tester",
        timestamp=datetime.now()
    )
    
    result = engine.review_task(task)
    
    # PDF: 30 (len) + 10 (h1) = 40
    # Repo: 10(readme) + 10(tests) + 10(commits) + 10(files) = 40
    # Desc: 10(len) + 10(keywords) = 20
    # Total: 100
    
    assert result.score == 100
    assert result.status == "pass"

def test_deterministic_scoring_minimal():
    engine = ReviewEngine()
    
    # Minimal input
    description_content = "Too short."
    
    task = Task(
        task_id="test-score-2",
        task_title="Bad Submission",
        task_description=description_content,
        submitted_by="Tester",
        timestamp=datetime.now()
    )
    
    result = engine.review_task(task)
    
    # PDF: 0
    # Repo: 0
    # Desc: 0 (too short)
    # Total: 0
    
    assert result.score == 0
    assert result.status == "fail"
    assert "No PDF content provided." in result.failure_reasons
    assert "No repository metrics provided." in result.failure_reasons
