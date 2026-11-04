#!/bin/bash
# Oracle: a mechanical summary built from the structured findings (lists every significant-or-higher acuity
# field in the headline). It only smoke-tests the task plumbing; it is not a reference summary.
set -euo pipefail
python3 - <<'PY'
import json
from pathlib import Path

rank = {"critical": 0, "urgent": 1, "significant": 2}
flagged = []
for f in sorted(Path("/app/findings").glob("*.json")):
    d = json.loads(f.read_text())
    for key, field in d["fields"].items():
        if key.endswith("acuity") and field["answer"] in rank:
            flagged.append((rank[field["answer"]], f"{d['title']}: {field['question'].split(':')[0]} ({field['answer']})"))
flagged.sort()
headline = "; ".join(t for _, t in flagged) if flagged else "No significant findings."
Path("/app/output").mkdir(exist_ok=True)
Path("/app/output/summary.md").write_text(
    f"**{headline}**\n\n1. See the structured findings for the remaining results.\n")
PY
