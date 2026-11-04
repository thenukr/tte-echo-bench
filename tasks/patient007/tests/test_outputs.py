"""Validate the agent's structured TTE report against the blank templates.

The agent's report is restored from the agent container at /app/report (see `artifacts` in task.toml).
These checks cover form validity only: every file and field present, answers drawn from the allowed
options, and only_if logic respected. Scoring against /tests/expert_answers is not implemented yet.
"""
import json
from pathlib import Path

import pytest

REPORT = Path("/app/report")
TEMPLATES = Path("/tests/templates")
SECTIONS = sorted(p.stem for p in TEMPLATES.glob("*.json"))


def load(path: Path):
    return json.loads(path.read_text())


def condition_met(field, filled, skipped):
    def clause(cond):
        for key, want in cond.items():
            if key in skipped:
                return False
            want = want if isinstance(want, list) else [want]
            got = filled.get(key)
            got = got if isinstance(got, list) else ([got] if got else [])
            if not any(w in got for w in want):
                return False
        return True

    if "only_if" in field:
        return clause(field["only_if"])
    if "only_if_any" in field:
        return any(clause(c) for c in field["only_if_any"])
    return True


def test_sections_present():
    assert SECTIONS, "no templates found"
    missing = [s for s in SECTIONS if not (REPORT / f"{s}.json").exists()]
    assert not missing, f"missing report files: {missing}"


@pytest.mark.parametrize("section", SECTIONS)
def test_section_valid(section):
    template = load(TEMPLATES / f"{section}.json")
    report = load(REPORT / f"{section}.json")
    assert report.get("section") == section
    assert set(report.get("fields", {})) == set(template["fields"]), "fields were added or removed"

    errors, filled, skipped = [], {}, set()
    for key, tf in template["fields"].items():
        ans = report["fields"][key].get("answer")
        shown = condition_met(tf, filled, skipped)
        if not shown:
            if ans not in (None, []):
                errors.append(f"{key}: should be null (only_if not met), got {ans!r}")
            skipped.add(key)
            continue
        blank = ans is None or ans == [] or ans == ""
        if blank:
            if not tf.get("optional"):
                errors.append(f"{key}: required answer missing")
        elif tf["type"] == "single":
            if not isinstance(ans, str) or ans not in tf["options"]:
                errors.append(f"{key}: {ans!r} is not one of {tf['options']}")
        elif tf["type"] == "multi":
            if not isinstance(ans, list) or len(set(ans)) != len(ans) or not set(ans) <= set(tf["options"]):
                errors.append(f"{key}: {ans!r} must be a list of distinct options from {tf['options']}")
        elif tf["type"] == "text":
            if not isinstance(ans, str):
                errors.append(f"{key}: expected a string, got {ans!r}")
        filled[key] = ans
    assert not errors, "\n".join(errors)
