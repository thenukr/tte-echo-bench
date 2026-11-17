#!/bin/bash
# Reward 1 iff the agent wrote one answer row with the same 610 columns as the header.
python3 - <<'PY'
import csv
rows = list(csv.reader(open("/app/findings_form.csv", encoding="utf-8-sig")))
ok = len(rows) >= 2 and len(rows[1]) == len(rows[0]) == 610 and any(c.strip() for c in rows[1])
print("rows:", len(rows), "cols:", [len(r) for r in rows], "ok:", ok)
open("/logs/verifier/reward.txt", "w").write("1" if ok else "0")
PY
