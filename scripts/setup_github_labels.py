#!/usr/bin/env python3
"""
Codealytica Editflow AI - GitHub Labels Synchronization Script
Defines and synchronizes the standard label taxonomy across the repository.
"""

import json
import subprocess
import sys

LABELS = [
    # Types
    {"name": "bug", "color": "d73a4a", "description": "Something isn't working as expected"},
    {"name": "feature", "color": "a2eeef", "description": "New capability or architectural addition"},
    {"name": "enhancement", "color": "008672", "description": "Improvement to an existing feature"},
    {"name": "documentation", "color": "0075ca", "description": "Documentation updates, fixes, or additions"},
    {"name": "refactor", "color": "cfd3d7", "description": "Code change that neither fixes a bug nor adds a feature"},
    {"name": "performance", "color": "f9d0c4", "description": "Code change that improves processing speed or memory usage"},
    {"name": "security", "color": "b60205", "description": "Security vulnerability, advisory, or secret protection"},
    {"name": "maintenance", "color": "e4e669", "description": "Routine repository, dependency, or CI/CD maintenance"},

    # Priorities
    {"name": "priority: critical", "color": "b60205", "description": "Blocks release or production pipeline; urgent attention"},
    {"name": "priority: high", "color": "d93f0b", "description": "High-impact issue or major scheduled deliverable"},
    {"name": "priority: medium", "color": "fbca04", "description": "Normal priority bug or enhancement"},
    {"name": "priority: low", "color": "0e8a16", "description": "Minor issue or non-urgent optimization"},

    # Areas
    {"name": "area: editorial", "color": "1d76db", "description": "Editorial Intelligence Engine (cuts, pauses, repetition)"},
    {"name": "area: multilingual", "color": "5319e7", "description": "Multilingual localisation, translation, and dubbing"},
    {"name": "area: audio", "color": "0052cc", "description": "Audio mastering, filtergraphs, and loudness compliance"},
    {"name": "area: video", "color": "006b75", "description": "Video encoding, splicing, and frame processing"},
    {"name": "area: transcription", "color": "c2e0c6", "description": "faster-whisper and speech-to-text pipeline"},
    {"name": "area: youtube", "color": "e11d21", "description": "YouTube Data API v3 integration and publishing"},
    {"name": "area: github-actions", "color": "6f42c1", "description": "GitHub Actions workflows, CI/CD, and automation"},
    {"name": "area: configuration", "color": "bfdadc", "description": "JSON configurations, schemas, and environment variables"},
    {"name": "area: documentation", "color": "c5def5", "description": "Markdown documentation and guides"},
    {"name": "area: testing", "color": "bfd4f2", "description": "Unit tests, integration suites, and test mocks"},

    # Status
    {"name": "status: needs-triage", "color": "ededed", "description": "Awaiting initial review and classification"},
    {"name": "status: confirmed", "color": "c2e0c6", "description": "Issue reproduced or feature accepted for work"},
    {"name": "status: in-progress", "color": "fef2c0", "description": "Actively being worked on by an assigned engineer"},
    {"name": "status: blocked", "color": "e99695", "description": "Blocked by external dependency or upstream review"},
    {"name": "status: needs-review", "color": "d4c5f9", "description": "Pull request submitted and awaiting code review"},

    # Contributor
    {"name": "good first issue", "color": "7057ff", "description": "Good for newcomers to the project"},
    {"name": "help wanted", "color": "008672", "description": "Extra attention or community contribution needed"},
]

def main():
    print(f"Codealytica Editflow AI - {len(LABELS)} Standard Labels Defined.")
    print("Exporting label configuration to .github/labels.json...")
    with open(".github/labels.json", "w", encoding="utf-8") as f:
        json.dump(LABELS, f, indent=2)
    print("Labels definition successfully written to .github/labels.json.")

if __name__ == "__main__":
    main()
