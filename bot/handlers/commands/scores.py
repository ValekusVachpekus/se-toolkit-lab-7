"""Handler for /scores command."""

from __future__ import annotations


def handle_scores(lab_id: str | None = None) -> str:
    """Handle /scores command — get scores for a lab.
    
    Args:
        lab_id: The lab identifier (e.g., "lab-04")
    
    Returns:
        Formatted scores response
    
    TODO: Implement actual backend API call in Task 2.
    For now, returns placeholder.
    """
    if lab_id is None:
        return "Please specify a lab ID. Usage: /scores lab-04"
    return f"""Scores for {lab_id}:
- Task 1: 80%
- Task 2: 75%
- Task 3: 90%

(placeholder — will fetch from API in Task 2)"""
