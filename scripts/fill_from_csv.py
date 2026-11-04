"""Fill the blank report templates with one expert's answers from a Tally CSV export.

The CSV has one column per question, in form order, plus one true/false column per option for checkbox
questions ("<title> (<option>)"). Question titles repeat across sections ("Size"), so columns are matched
to form questions by walking both in order.

Usage:
  python3 scripts/fill_from_csv.py --form form.json --csv submissions.csv --email expert@example.com \
      --templates tasks/patient007/environment/report_template --out <dir>
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_tally import SECTIONS, condition_met, field_key, option_slug  # noqa: E402
from tally_form import parse_questions  # noqa: E402


def split_multi(value, options):
    """Split a joined multi-select cell back into option labels (labels themselves may contain ', ')."""
    if value in options:
        return [value]
    parts, out, buf = value.split(", "), [], ""
    for p in parts:
        buf = f"{buf}, {p}" if buf else p
        if buf in options:
            out.append(buf)
            buf = ""
    if buf:
        raise ValueError(f"cannot split {value!r} into options {options}")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--form", required=True, type=Path)
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--email", required=True)
    ap.add_argument("--templates", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    questions = parse_questions(json.loads(args.form.read_text())["context"]["ledger"])
    rows = list(csv.reader(args.csv.open(encoding="utf-8-sig")))
    header = [h.strip() for h in rows[0]]
    matches = [r for r in rows[1:] if r[header.index("Your email:")].strip().lower() == args.email.lower()]
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one submission from {args.email}, found {len(matches)}")
    row = matches[0]

    # Walk form questions and CSV columns in step.
    col = header.index("Your email:") + 1
    raw = {}
    for q in questions:
        if not q["section"]:
            continue
        # Tally de-duplicates repeated titles in the export: "Size", "Size (2)", "Size (3)", ...
        name = header[col]
        if name != q["title"] and not re.fullmatch(re.escape(q["title"]) + r" \(\d+\)", name):
            raise SystemExit(f"column {col}: expected {q['title']!r}, found {name!r}")
        if q["kind"] == "checkboxes":
            opt_cols = header[col + 1: col + 1 + len(q["options"])]
            expected = [f"{name} ({o})" for o in q["options"]]
            if [c.strip() for c in opt_cols] != expected:
                raise SystemExit(f"option columns for {q['title']!r} do not match the form")
            ticked = [o for o, v in zip(q["options"], row[col + 1: col + 1 + len(q["options"])]) if v == "true"]
            raw[q["uuid"]] = ticked
            col += 1 + len(q["options"])
        else:
            raw[q["uuid"]] = row[col].strip()
            col += 1
    if col != len(header):
        raise SystemExit(f"{len(header) - col} unexpected trailing CSV columns: {header[col:]}")

    args.out.mkdir(parents=True, exist_ok=True)
    by_section = {}
    for q in questions:
        if q["section"]:
            by_section.setdefault(SECTIONS[q["section"]], []).append(q)
    for skey, qs in by_section.items():
        t = json.loads((args.templates / f"{skey}.json").read_text())
        filled, skipped = {}, set()
        for q in qs:
            key = field_key(skey, q["title"])
            f = t["fields"][key]
            v = raw[q["uuid"]]
            shown = condition_met(f, filled, skipped)
            if not shown:
                if v:
                    raise SystemExit(f"{skey}.{key}: answered although its only_if condition is not met")
                f["answer"] = None
                skipped.add(key)
                continue
            if f["type"] == "text":
                f["answer"] = v or None
            else:
                labels = v if isinstance(v, list) else (split_multi(v, q["options"]) if v else [])
                slugs = [f["options"][q["options"].index(lbl)] for lbl in labels]
                if f["type"] == "single":
                    if len(slugs) > 1:
                        raise SystemExit(f"{skey}.{key}: expert accepted several answers {slugs}; pick one")
                    f["answer"] = slugs[0] if slugs else None
                else:
                    f["answer"] = slugs
                assert all(option_slug(lbl) == s for lbl, s in zip(labels, slugs))
            filled[key] = f["answer"]
        (args.out / f"{skey}.json").write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(by_section)} sections for {args.email} to {args.out}")


if __name__ == "__main__":
    main()
