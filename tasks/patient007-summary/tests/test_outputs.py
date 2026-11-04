"""Checks for the patient007 summary task.

The agent's output is restored from the agent container at /app/output (see `artifacts` in task.toml).
These checks only cover the output format. Grading the summary's clinical content is not implemented yet.
"""
from pathlib import Path

SUMMARY = Path("/app/output/summary.md")


def test_summary_exists():
    assert SUMMARY.exists(), "missing /app/output/summary.md"


def test_summary_has_headline_and_impression():
    lines = [ln.strip() for ln in SUMMARY.read_text().splitlines() if ln.strip()]
    assert len(lines) >= 2, "expected a headline line followed by an impression"
    assert len(lines[0]) >= 10, "headline is too short"
