"""Handler for /labs command."""

from __future__ import annotations


def handle_labs() -> str:
    """Handle /labs command — list available labs.
    
    TODO: Implement actual backend API call in Task 2.
    For now, returns placeholder.
    """
    return """Available labs:
- lab-01: Introduction
- lab-02: Setup
- lab-03: Testing
- lab-04: Deployment

(placeholder — will fetch from API in Task 2)"""
